from __future__ import annotations
from pymint.mintvia import MINTVia
from pymint.mintterminal import MINTTerminal
from pymint.constraints.constraint import LayoutConstraint
from pymint.minttarget import MINTTarget
from pymint.mintlayer import MINTLayer, MINTLayerType
from parchmint.device import Device
from pymint.mintcomponent import MINTComponent
from pymint.mintconnection import MINTConnection
from typing import List, Optional
import sys


class MINTDevice(Device):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self._layout_constraints = []
        self._valve_map = dict()
        self._terminals = []
        self._vias = []

    def create_mint_component(
        self, name: str, technology: str, params: dict, layer_ids: List[str]
    ) -> MINTComponent:
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
        layer = super().get_layer(layer_id)
        connection = MINTConnection(name, technology, params, source, sinks, layer)
        super().add_connection(connection)
        return connection

    def create_mint_layer(self, name, group, layer_type: MINTLayerType) -> MINTLayer:
        layer = MINTLayer(name, group, layer_type)
        super().add_layer(layer)
        return layer

    def get_component(self, id: str) -> Optional[MINTComponent]:
        return super().get_component(id)

    def get_connection(self, id: str) -> Optional[MINTConnection]:
        return super().get_connection(id)

    def get_constraints(self) -> List[LayoutConstraint]:
        return self._layout_constraints

    def add_constraint(self, constraint: LayoutConstraint) -> None:
        self._layout_constraints.append(constraint)

    def to_MINT(self):
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
        self._valve_map[valve] = connection

    def add_terminal(self, name: str, pin_number: int, layer: str) -> MINTTerminal:
        ret = MINTTerminal(name, pin_number, layer)
        self._terminals.append(ret)
        return ret

    def add_via(self, name: str, width: int, layers: List[MINTLayer]) -> MINTVia:
        ret = MINTVia(name, width, layers)
        self._vias.append(ret)
        self.components.append(ret)
        return ret

    def to_parchmint_v1(self):
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

        if skip_constraints is not True:
            print("Computing Constraints")
            constraint_listener = ConstraintListener(listener.current_device)

            walker.walk(constraint_listener, tree)

            current_device = listener.current_device

        return current_device
