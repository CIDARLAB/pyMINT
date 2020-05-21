from pyMINT.mintcomponent import MINTComponent
from .constraint import LayoutConstraint


class LengthConstraint(LayoutConstraint):
    def __init__(self, component: MINTComponent, length:float) -> None:
        super().__init__()
        self.__components.append(component)
        self.__length = length

