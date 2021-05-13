from typing import List
from pymint.mintlayer import MINTLayer
from pymint.mintcomponent import MINTComponent


class MINTVia(MINTComponent):
    def __init__(self, name: str, layers: List[MINTLayer]) -> None:
        """Creates a new instance of a Via

        Args:
            name (str): name/ID of the via
            layers (List[MINTLayer]): List of layer objects where the via is present
        """
        width = 0
        super(MINTVia, self).__init__(name, "VIA", {"width": width}, layers)

    def set_width(self, width: int) -> None:
        """Sets the width of the via

        Args:
            width (int): via width
        """
        self.params.set_param("width", width)

    def to_MINT(self) -> str:
        """Returns the MINT string of the via

        Returns:
            str: returns the via
        """
        return "VIA {}".format(self.name)
