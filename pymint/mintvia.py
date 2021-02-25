from typing import List
from pymint.mintlayer import MINTLayer
from pymint.mintcomponent import MINTComponent


class MINTVia(MINTComponent):
    def __init__(self, name: str, width: int, layers: List[MINTLayer]) -> None:
        super(MINTVia, self).__init__(name, "VIA", {"width": width}, layers)

    def to_MINT(self) -> str:
        """Returns the MINT string of the via

        Returns:
            str: returns the via
        """
        return "VIA {}".format(self.name)
