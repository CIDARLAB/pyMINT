from typing import List
from pymint.mintlayer import MINTLayer
from pymint.mintcomponent import MINTComponent


class MINTVia(MINTComponent):
    def __init__(self, name: str, width: int, layers: List[MINTLayer]) -> None:
        super().__init__(name, "VIA", {"width": width}, layers)

    def to_MINT(self) -> str:
        return "VIA {}".format(self.name)
