from pymint.mintparams import MINTParams
from pymint.mintcomponent import MINTComponent

class MINTTerminal(MINTComponent):

    def __init__(self, name, port_number, layer:str = '0') -> None:
        super().__init__(name, 'TERMINAL', {}, layer)
        self.__port_number = port_number
    