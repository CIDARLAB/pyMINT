from pymint.mintvia import MINTVia
from pymint.mintterminal import MINTTerminal
from pymint.constraints.constraint import LayoutConstraint
from pymint.minttarget import MINTTarget
from pymint.mintlayer import MINTLayer, MINTLayerType
from parchmint.device import Device
from pymint.mintcomponent import MINTComponent
from pymint.mintconnection import MINTConnection
from typing import List, Optional

class MINTDevice(Device):

    def __init__(self, name:str) -> None:
        super().__init__()
        self.name = name
        self._layout_constraints = []
        self._valve_map = dict()
        self._terminals = []
        self._vias = []

    def addComponent(self, name: str, technology: str, params: dict, layer:str) -> MINTComponent:
        component = MINTComponent(name, technology, params, layer)
        super().add_component(component)
        return component
    
    def addConnection(self, name:str, technology:str, params: dict , source:MINTTarget, sinks:List[MINTTarget], layer:str) -> MINTConnection:
        connection = MINTConnection(name, technology, params, source, sinks, layer)
        super().add_connection(connection)
        return connection

    def addLayer(self, name, group, layer_type:MINTLayerType) -> MINTLayer:
        layer = MINTLayer(name, group, layer_type)
        super().add_layer(layer)
        return layer

    def getComponent(self, id:str) -> Optional[MINTComponent]:
        return super().get_component(id)

    def getConnection(self, id:str) -> Optional[MINTConnection]:
        return super().get_connection(id)

    def getConstraints(self) -> List[LayoutConstraint]:
        return self._layout_constraints

    def addConstraint(self, constraint: LayoutConstraint)-> None:
        self._layout_constraints.append(constraint)

    def toMINT(self):
        #TODO: Eventually I need to modify the MINT generation to account for all the layout constraints

        full_layer_text = ""
        #Loop Over all the layers
        for layer in self.layers:
            componenttext = "\n".join([item.toMINT() for item in self.components if item.layers[0] == layer.ID])
            connectiontext = "\n".join([item.toMINT() for item in self.connections if item.layer == layer.ID])
   
            full_layer_text += layer.toMINT("{}\n\n{}".format(componenttext, connectiontext)) +"\n\n"
            

        full = "DEVICE {}\n\n{}".format(self.name, full_layer_text)
        return full

    def mapValve(self, valve:MINTComponent, connection:MINTConnection) -> None:
        self._valve_map[valve] = connection

    def addTerminal(self, name:str, pin_number:int, layer:str) -> MINTTerminal:
        ret = MINTTerminal(name, pin_number, layer)
        self._terminals.append(ret)
        return ret

    def addVia(self, name:str) -> MINTVia:
        ret = MINTVia(name)
        self._vias.append(ret)
        self.components.append(ret)
        return ret

    def from_mint_file(filepath):
        from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream
        from pymint.constraints.constraintlistener import ConstraintListener
        from pymint.mintErrorListener import MINTErrorListener
        from pymint.antlr.mintLexer import mintLexer
        from pymint.antlr.mintParser import mintParser
        from pymint.mintcompiler import MINTCompiler
        import io

        finput = FileStream(filepath)

        lexer = mintLexer(finput)

        stream = CommonTokenStream(lexer)

        parser = mintParser(stream)

        #Connect the Error Listener
        parse_output = io.StringIO()
        parse_output.write("MINT SYNTAX ERRORS:\n")

        error_listener = MINTErrorListener(parse_output)
        parser.addErrorListener(error_listener)

        tree = parser.netlist()

        if error_listener.pass_through is False:
            print('STOPPED: Syntax Error(s) Found')
            sys.exit(0)
        
        walker = ParseTreeWalker()

        listener = MINTCompiler()

        walker.walk(listener, tree)

        constraint_listener = ConstraintListener(listener.current_device)

        walker.walk(constraint_listener, tree)


        current_device = listener.current_device

        return current_device
