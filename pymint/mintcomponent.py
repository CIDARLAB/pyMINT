from pymint.mintparams import MINTParams
from parchmint.component import Component

class MINTComponent(Component):

    def __init__(self, name:str , technology:str, params:dict, layer:str = '0') -> None:
        super().__init__()
        self.name = name
        self.ID = name
        self.entity = technology
        self.params = MINTParams(params)
        self.layers.append(layer)

    def toMINT(self) -> str:
        ret = "{} {} {};".format(self.entity, self.name, self.params.toMINT())
        return ret

    def __hash__(self) -> int:
        return hash((self.ID, self.entity))