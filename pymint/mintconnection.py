from pymint.mintparams import MINTParams
from parchmint.connection import Connection
from pymint.minttarget import MINTTarget
from typing import List

class MINTConnection(Connection):

    def __init__(self, name: str, technology: str, params:dict, source: MINTTarget, sinks: List[MINTTarget], layer:str = '0') -> None:
        
        self.name = name
        self.ID = name
        self.entity = technology
        self.params = MINTParams(params)
        self.source: MINTTarget = source
        self.sinks: List[MINTTarget] = sinks
        self.layer = layer

    def overwrite_id(self, id: str) -> None:
        self.ID = id

    def toMINT(self) -> str:
        ret = "{} {} from {} to {} {} ;".format(self.entity, self.name, self.source.toMINT(), " ".join([item.toMINT() for item in self.sinks]), self.params.toMINT())
        return ret