from typing import Union

from parchmint.layer import Layer


class MINTNode(Component):
    """NODE object that is considered a waypoint in the design
    however this is modelled as a component in Parchmint v1.

    simplifies the creation process and generate all of the
    required MINT.

    """

    def __init__(self, name: str, layer: Layer) -> None:
        """Creates a new NODE object

        Args:
            name (str): name of the node
            layer (str, optional): [description].
        """
        super(MINTNode, self).__init__(name, "NODE", {}, [layer])

    def to_MINT(self) -> str:
        """Returns the MINT for the NODE

        Returns:
            str: [description]
        """
        ret = "NODE {};".format(self.name)
        return ret
