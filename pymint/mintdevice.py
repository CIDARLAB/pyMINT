from __future__ import annotations
from pymint.mintvia import MINTVia
from pymint.mintterminal import MINTTerminal
from pymint.constraints.constraint import LayoutConstraint
from pymint.minttarget import MINTTarget
from pymint.mintlayer import MINTLayer, MINTLayerType
from parchmint.device import Device
from pymint.mintcomponent import MINTComponent
from pymint.mintconnection import MINTConnection
from typing import List
import sys


class MINTDevice(Device):
    def __init__(self, name: str, json=None) -> None:
        """Creates a MINT device

        A MINT device has the extra bells and whistles necessary for genrating
        structured MINT. Pass the ParchMINT JSON to the `json` arg if you want
        to initialize from a JSON file.

        Args:
            name (str): name of the device
            json (str, optional): JSON string. Defaults to None.
        """
        super(MINTDevice, self).__init__(json=json)

        self.name = name
        self._layout_constraints = []
        self._terminals = []
        self._vias = []

    def create_mint_component(
        self, name: str, technology: str, params: dict, layer_ids: List[str]
    ) -> MINTComponent:
        """Creates a new component and adds it to the device

        Args:
            name (str): name
            technology (str): MINT string
            params (dict): params dictionary
            layer_ids (List[str]): list of layer ids

        Returns:
            MINTComponent: the newly created component
        """
        # Retrieve the correct layer:
        layers = []
        for layer_id in layer_ids:
            layers.append(super().get_layer(layer_id))
        component = MINTComponent(name, technology, params, layers)
        super().add_component(component)
        return component

    def create_mint_connection(
        self,
        name: str,
        technology: str,
        params: dict,
        source: MINTTarget,
        sinks: List[MINTTarget],
        layer_id: str,
    ) -> MINTConnection:
        """Creates a new MINT connection and adds it to the device

        Args:
            name (str): name of the connection
            technology (str): MINT string
            params (dict): dictionary of the paraeters
            source (MINTTarget): object defining where the connection starts
            sinks (List[MINTTarget]): list of objects defining where the connection ends
            layer_id (str): layer id of the connection

        Raises:
            Exception: Throws an exception if layer with the given id is not found

        Returns:
            MINTConnection: Returns the newly created connection
        """
        layer = super().get_layer(layer_id)
        if layer is None:
            raise Exception("Cannot create new MINT connection with invalid layer")
        assert layer is not None
        connection = MINTConnection(name, technology, params, source, sinks, layer)
        super().add_connection(connection)
        return connection

    def create_mint_layer(
        self, id: str, name_postfix: str, group, layer_type: MINTLayerType
    ) -> MINTLayer:
        """[summary]

        Args:
            id (str): [description]
            name_postfix (str): [description]
            group ([type]): [description]
            layer_type (MINTLayerType): [description]

        Returns:
            MINTLayer: [description]
        """
        name = "{}_{}".format(str(MINTLayerType.FLOW), name_postfix)
        layer = MINTLayer(id, name, group, layer_type)
        super().add_layer(layer)
        return layer

    def get_constraints(self) -> List[LayoutConstraint]:
        """Returns the layout constraints of the device. Currently does not support the constraints

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
        # TODO: Eventually I need to modify the MINT generation to account for all the layout constraints

        full_layer_text = ""
        # Loop Over all the layers
        for layer in self.layers:
            componenttext = "\n".join(
                [item.to_MINT() for item in self.components if item.layers[0] == layer]
            )
            connectiontext = "\n".join(
                [item.to_MINT() for item in self.connections if item.layer == layer]
            )

            full_layer_text += (
                layer.to_MINT("{}\n\n{}".format(componenttext, connectiontext)) + "\n\n"
            )

        full = "DEVICE {}\n\n{}".format(self.name, full_layer_text)
        return full

    def map_valve(self, valve: MINTComponent, connection: MINTConnection) -> None:
        """Maps the valve to a connection in the device

        Args:
            valve (MINTComponent): valve component
            connection (MINTConnection): connection on which the valve is mapped
        """
        self._valve_map[valve] = connection

    def add_terminal(self, name: str, pin_number: int, layer_id: str) -> MINTTerminal:
        """Creates and adds a terminal to the device with an associated pin number

        Args:
            name (str): name of the pin
            pin_number (int): pin number of the terminal
            layer (str): layerid associated with the terminal

        Returns:
            MINTTerminal: The newly created terminal
        """
        layer = self.get_layer(layer_id)
        ret = MINTTerminal(name, pin_number, layer)
        self._terminals.append(ret)
        self.components.append(ret)
        return ret

    def add_via(self, name: str, width: int, layers: List[MINTLayer]) -> MINTVia:
        """Creates and adds a via to the device

        Args:
            name (str): name of the via
            width (int): width of the via
            layers (List[MINTLayer]): layers associated with the via

        Returns:
            MINTVia: The newly created via
        """
        ret = MINTVia(name, width, layers)
        self._vias.append(ret)
        self.components.append(ret)
        return ret

    def to_parchmint_v1(self) -> dict:
        """Returns the Parchmint Version 1.0 in the form of a dictionary

        Returns:
            dict: dictionary representing the json datastructure
        """
        ret = dict()
        ret["name"] = self.name
        ret["components"] = [c.to_parchmint_v1() for c in self.components]
        ret["connections"] = [c.to_parchmint_v1() for c in self.connections]
        ret["params"] = self.params.to_parchmint_v1()
        ret["layers"] = [layer.to_parchmint_v1() for layer in self.layers]
        ret["version"] = 1

        return ret

    @staticmethod
    def from_mint_file(filepath: str, skip_constraints: bool = False) -> MINTDevice:
        """Compiles the MINT file at the given path

        Args:
            filepath (str): absolute filepath of the mint file
            skip_constraints (bool, optional): flag to accept / skip constraint parsing. Defaults to False.

        Returns:
            MINTDevice: The parsed device from the MINT file
        """
        from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream
        from pymint.constraints.constraintlistener import ConstraintListener
        from pymint.mintErrorListener import MINTErrorListener
        from pymint.antlrgen.mintLexer import mintLexer
        from pymint.antlrgen.mintParser import mintParser
        from pymint.mintcompiler import MINTCompiler
        import io

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

        assert listener.current_device is not None
        current_device = listener.current_device

        if skip_constraints is not True:
            print("Computing Constraints")
            constraint_listener = ConstraintListener(listener.current_device)

            walker.walk(constraint_listener, tree)

            current_device = listener.current_device

        return current_device
