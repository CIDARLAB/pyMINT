from pymint.mintcomponent import MINTComponent


class MINTNode(MINTComponent):

    def __init__(self, name: str, layer: str = '0') -> None:
        super().__init__(name, "NODE", dict(), layer)


    def toMINT(self) -> str:
        ret = "NODE {};".format(self.name)
        return ret