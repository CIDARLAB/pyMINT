from __future__ import annotations

import sys
from typing import Dict, List, Optional

from parchmint import Component, Connection, Layer, Params, Target
from parchmint.device import Device, ValveType

from pymint.constraints.layoutconstraint import LayoutConstraint
from pymint.mintlayer import MINTLayerType
from pymint.mintprotocol import MINTProtocol
from pymint.mintterminal import MINTTerminal
from pymint.mintvia import MINTVia
from pymint.mintwriter import (
    to_component_MINT,
    to_connection_MINT,
    to_layer_MINT,
    to_valve_MINT,
    to_via_MINT,
)


class MINTDevice(MINTProtocol):
    """Device class abstracting parchmint Device object adding additional
    methods for generating MINT

    """

    def __init__(self, name: str, device_ref: Optional[Device] = None) -> None:
        """Creates a MINT device

        A MINT device has the extra bells and whistles necessary for genrating
        structured MINT. Pass the ParchMINT JSON to the `json` arg if you want
        to initialize from a JSON file.

        Args:
            name (str): name of the device
            json (str, optional): JSON string. Defaults to None.
        """
        super().__init__()

        self._device = Device() if device_ref is None else device_ref
        self._device.name = name
        self._layout_constraints: List[LayoutConstraint] = []
        self._terminals: List[MINTTerminal] = []
        self._vias: List[MINTVia] = []

    @property
    def device(self) -> Device:
        """Returns the underlying parchmint device

        Returns:
            Device: underlying parchmint device
        """
        return self._device

    def create_mint_component(
        self, name: str, technology: str, params: Dict, layer_ids: List[str]
    ) -> Component:
        """Creates a new component and adds it to the device

        Args:
            name (str): name
            technology (str): MINT string
            params (Dict): params dictionary
            layer_ids (List[str]): list of layer ids

        Returns:
            Component: the newly created component
        """
        # Retrieve the correct layer:
        layers = []
        for layer_id in layer_ids:
            layers.append(self._device.get_layer(layer_id))
        component = Component(
            name=name, ID=name, layers=layers, params=Params(params), entity=technology
        )
        self._device.add_component(component)
        return component

    def create_mint_connection(
        self,
        name: str,
        technology: str,
        params: Dict,
        source: Target,
        sinks: List[Target],
        layer_id: str,
    ) -> Connection:
        """Creates a new MINT connection and adds it to the device

        Args:
            name (str): name of the connection
            technology (str): MINT string
            params (Dict): dictionary of the paraeters
            source (Target): object defining where the connection starts
            sinks (List[Target]): list of objects defining where the connection ends
            layer_id (str): layer id of the connection

        Raises:
            Exception: Throws an exception if layer with the given id is not found

        Returns:
            Connection: Returns the newly created connection
        """
        layer = self.device.get_layer(layer_id)
        if layer is None:
            raise Exception("Cannot create new MINT connection with invalid layer")
        if layer is None:
            raise Exception("Layer is None")
        connection = Connection(
            name=name,
            ID=name,
            entity=technology,
            source=source,
            sinks=sinks,
            params=Params(params),
            layer=layer,
        )
        self._device.add_connection(connection)
        return connection

    def create_mint_layer(
        self, ID: str, name_postfix: str, group, layer_type: MINTLayerType
    ) -> Layer:
        """[summary]

        Args:
            id (str): id of the mint layer
            name_postfix (str): postfix to add to the layer name
            group ([type]): group the layer belongs to
            layer_type (MINTLayerType): layer type of the layer

        Returns:
            Layer: [description]
        """
        name = "{}_{}".format(str(MINTLayerType.FLOW), name_postfix)
        layer = Layer()
        layer.ID = ID
        layer.name = name
        layer.group = group
        layer.layer_type = str(layer_type)
        self._device.add_layer(layer)
        return layer

    def create_valve(
        self,
        name: str,
        technology: str,
        params: Dict,
        layer_ids: List[str],
        connection: Connection,
        valve_type: ValveType = ValveType.NORMALLY_OPEN,
    ) -> Component:
        """Creates a new valve and adds it to the device

        Args:
            name (str): name of the valve
            technology (str): MINT string
            params (Dict): dictionary of the paraeters
            layer_ids (List[str]): list of layer ids
            connection (Connection): connection to attach the valve to
            valve_type (ValveType, optional): valve type of the valve .
            Defaults to ValveType.NORMALLY_OPEN.

        Raises:
            Exception: [description]

        Returns:
            Component: [description]
        """
        valve = self.create_mint_component(name, technology, params, layer_ids)
        if connection not in self.device.connections:
            raise Exception("Connection {} not found".format(connection.ID))
        self.device.map_valve(valve, connection, valve_type)
        return valve

    def get_constraints(self) -> List[LayoutConstraint]:
        """Returns the layout constraints of the device. Currently does not support the
        constraints

        Returns:
            List[LayoutConstraint]: List of layout constriants objects
        """
        return self._layout_constraints

    def add_constraint(self, constraint: LayoutConstraint) -> None:
        """Adds a layout constriant to the device

        Args:
            constraint (LayoutConstraint): new constraint we want to add
        """
        self._layout_constraints.append(constraint)

    def to_MINT(self) -> str:
        """Returns the MINT string of the device

        Returns:
            str: MINT string
        """
        # TODO: Eventually I need to modify the MINT generation to account for all the
        # layout constraints

        # Generate a valve list for the device
        valve_list = self.device.valves
        via_list = [via.component for via in self._vias]
        full_layer_text = ""

        # Generate Via Text
        via_text = "\n".join([to_via_MINT(via) for via in self._vias])

        # Loop Over all the layers
        for layer in self.device.layers:
            componenttext = "\n".join(
                [
                    to_component_MINT(item)
                    for item in self.device.components
                    if item.layers[0] == layer
                    and item not in valve_list
                    and item not in via_list
                ]
            )

            valvetext = ""
            if layer.layer_type is str(MINTLayerType.CONTROL):
                valvetext = "\n".join(
                    [
                        to_valve_MINT(item, self.device.get_valve_connection(item))
                        for item in valve_list
                        if layer in item.layers
                    ]
                )

            connectiontext = "\n".join(
                [
                    to_connection_MINT(item)
                    for item in self.device.connections
                    if item.layer == layer
                ]
            )

            full_layer_text += to_layer_MINT(
                layer,
                "{}\n\n{}\n\n{}".format(componenttext, valvetext, connectiontext)
                + "\n\n",
            )

        full = "DEVICE {}\n\n{}\n\n{}".format(
            self.device.name, via_text, full_layer_text
        )
        return full

    def add_terminal(self, name: str, pin_number: int, layer_id: str) -> MINTTerminal:
        """Creates and adds a terminal to the device with an associated pin number

        Args:
            name (str): name of the pin
            pin_number (int): pin number of the terminal
            layer (str): layerid associated with the terminal

        Returns:
            MINTTerminal: The newly created terminal
        """
        layer = self.device.get_layer(layer_id)
        ret = MINTTerminal(name, pin_number, layer)
        self._terminals.append(ret)
        self.device.components.append(ret.component)
        return ret

    def add_via(self, name: str, layers: List[Layer]) -> MINTVia:
        """Creates and adds a via to the device

        Args:
            name (str): name of the via
            width (int): width of the via
            layers (List[Layer]): layers associated with the via

        Returns:
            MINTVia: The newly created via
        """
        ret = MINTVia(name, layers)
        self._vias.append(ret)
        self.device.components.append(ret.component)
        return ret

    def to_parchmint(self):
        """Returns the Parchmint string of the device

        Returns:
            str: Parchmint string
        """
        ret = self.device.to_parchmint_v1_2()
        ret["layoutConstraints"] = [
            constraint.to_parchmint_v1_x() for constraint in self._layout_constraints
        ]
        return ret

    @staticmethod
    def from_mint_file(filepath: str, skip_constraints: bool = False) -> MINTDevice:
        """Compiles the MINT file at the given path

        Args:
            filepath (str): absolute filepath of the mint file
            skip_constraints (bool, optional): flag to accept / skip constraint parsing.
            Defaults to False.

        Returns:
            MINTDevice: The parsed device from the MINT file
        """
        import io

        from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker

        from pymint.antlrgen.mintLexer import mintLexer
        from pymint.antlrgen.mintParser import mintParser
        from pymint.constraints.constraintlistener import ConstraintListener
        from pymint.mintcompiler import MINTCompiler
        from pymint.mintErrorListener import MINTErrorListener

        finput = FileStream(filepath)

        lexer = mintLexer(finput)

        stream = CommonTokenStream(lexer)

        parser = mintParser(stream)

        # Connect the Error Listener
        parse_output = io.StringIO()
        parse_output.write("MINT SYNTAX ERRORS:\n")

        error_listener = MINTErrorListener(parse_output)
        parser.addErrorListener(error_listener)

        tree = parser.netlist()

        if error_listener.pass_through is False:
            print("STOPPED: Syntax Error(s) Found")
            sys.exit(0)

        walker = ParseTreeWalker()

        listener = MINTCompiler()

        walker.walk(listener, tree)

        if listener.current_device is None:
            raise AssertionError
        current_device = listener.current_device

        if skip_constraints is not True:
            print("Computing Constraints")
            constraint_listener = ConstraintListener(listener.current_device)

            walker.walk(constraint_listener, tree)

            current_device = listener.current_device

        return current_device
