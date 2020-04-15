from pyparchmint.layer import Layer

from enum import Enum

class MINTLayerType(Enum):
    FLOW = 1
    CONTROL = 2
    INTEGRATION = 3

    def __str__(self) -> str:
        if self == MINTLayerType.FLOW:
            return 'FLOW'
        elif self == MINTLayerType.CONTROL:
            return 'CONTROL'
        elif self == MINTLayerType.INTEGRATION:
            return 'INTEGRATION'

class MINTLayer(Layer):

    def __init__(self, id, group, layer_type:MINTLayerType, ) -> None:
        super().__init__()
        self.ID = id
        self.group = group
        self.type = layer_type


    def toMINT(self, content:str) -> str:
        
        ret = "LAYER {} \n\n{} \n\nEND LAYER".format(self.type, content)
        return ret
