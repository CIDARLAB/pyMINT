from mint.minttarget import MINTTarget
from .mintlayer import MINTLayer, MINTLayerType
from pyparchmint.device import Device
from .mintcomponent import MINTComponent
from .mintconnection import MINTConnection
from typing import List

class MINTDevice(Device):

    def __init__(self, name:str) -> None:
        super().__init__()
        self.name = name

    def addComponent(self, name: str, technology: str, params: dict, layer:str):
        component = MINTComponent(name, technology, params, layer)
        super().addComponent(component)
    
    def addConnection(self, name:str, technology:str, params: dict , source:MINTTarget, sinks:List[MINTTarget], layer:str):
        connection = MINTConnection(name, technology, params, source, sinks, layer)
        super().addConnection(connection)

    def addLayer(self, name, group, layer_type:MINTLayerType):
            layer = MINTLayer(name, group, layer_type)
            super().addLayer(layer)

    def getComponent(self, id:str) -> MINTComponent:
        return super().getComponent(id)

    def getConnection(self, id:str) -> MINTConnection:
        return super().getConnection(id)

    def toMINT(self):

        #TODO: Eventually I need to modify the MINT generation to account for all the layout constraints

        full_layer_text = ""
        #Loop Over all the layers
        for layer in self.layers:
            componenttext = "\n".join([item.toMINT() for item in self.components if item.layer == layer.ID])
            connectiontext = "\n".join([item.toMINT() for item in self.connections if item.layer == layer.ID])
   
            full_layer_text += layer.toMINT("{}\n\n{}".format(componenttext, connectiontext)) +"\n\n"
            

        full = "DEVICE {}\n\n{}".format(self.name, full_layer_text)
        return full