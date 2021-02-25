from pymint.mintlayer import MINTLayer
from pymint.mintcomponent import MINTComponent


class MINTNode(MINTComponent):
    def __init__(self, name: str, layer: MINTLayer) -> None:
        """Creates a new NODE object

        Args:
            name (str): name of the node
            layer (str, optional): [description].
        """
        super(MINTNode, self).__init__(name, "NODE", dict(), [layer])

    def to_MINT(self) -> str:
        """Returns the MINT for the NODE

        Returns:
            str: [description]
        """
        ret = "NODE {};".format(self.name)
        return ret
