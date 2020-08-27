from mint.mintcomponent import MINTComponent
from mint.constraints.constraint import LayoutConstraint


class LengthConstraint(LayoutConstraint):
    def __init__(self, component: MINTComponent, length:float) -> None:
        super().__init__()
        self._components.append(component)
        self.__length = length

