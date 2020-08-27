from .mintvia import MINTVia
from .mintterminal import MINTTerminal
from .constraints.constraint import LayoutConstraint
from .minttarget import MINTTarget
from .mintlayer import MINTLayer, MINTLayerType
from parchmint.device import Device
from .mintcomponent import MINTComponent
from mint.mintconnection import MINTConnection
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
        super().addComponent(component)
        return component
    
    def addConnection(self, name:str, technology:str, params: dict , source:MINTTarget, sinks:List[MINTTarget], layer:str) -> MINTConnection:
        connection = MINTConnection(name, technology, params, source, sinks, layer)
        super().addConnection(connection)
        return connection

    def addLayer(self, name, group, layer_type:MINTLayerType) -> MINTLayer:
        layer = MINTLayer(name, group, layer_type)
        super().addLayer(layer)
        return layer

    def getComponent(self, id:str) -> Optional[MINTComponent]:
        return super().getComponent(id)

    def getConnection(self, id:str) -> Optional[MINTConnection]:
        return super().getConnection(id)

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

    