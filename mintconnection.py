from .mintparams import MINTParams
from pyparchmint.connection import Connection
from .minttarget import MINTTarget

class MINTConnection(Connection):

    def __init__(self, name: str, technology: str, params:dict, source: MINTTarget, sinks: [MINTTarget], layer:str = '0') -> None:
        
        self.name = name
        self.ID = name
        self.entity = technology
        self.params = MINTParams(params)
        self.source = source
        self.sinks = sinks
        self.layer = layer


    def toMINT(self) -> str:
        ret = "{} {} from {} to {} {} ;".format(self.entity, self.name, self.source.toMINT(), " ".join([item.toMINT() for item in self.sinks]), self.params.toMINT())
        return ret