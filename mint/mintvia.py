from .mintparams import MINTParams
from .mintcomponent import MINTComponent

class MINTVia(MINTComponent):

    def __init__(self, name:str) -> None:
        super().__init__(name, 'VIA', {},layer='')