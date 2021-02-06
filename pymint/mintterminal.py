from pymint.mintparams import MINTParams
from pymint.mintcomponent import MINTComponent


class MINTTerminal(MINTComponent):
    def __init__(self, name: str, port_number: int, layer: str = "0") -> None:
        super().__init__(name, "TERMINAL", {}, layer)
        self.__port_number = port_number

    @property
    def port_number(self) -> int:
        """Returns the port number of the terminal (at a device level)

        Returns:
            int: port value 
        """
        return self.__port_number

    def to_MINT(self) -> str:
        return "TERMINAL {} {}".format(self.name, self.__port_number)
