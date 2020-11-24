from pymint.mintcomponent import MINTComponent
from pymint.constraints.constraint import LayoutConstraint


class LengthConstraint(LayoutConstraint):
    def __init__(self, component: MINTComponent, length:float) -> None:
        super().__init__()
        self._components.append(component)
        self.__length = length

    @property
    def component(self) -> MINTComponent:
        return self._components[0]
    
    @property
    def length(self) -> float:
        return self.__length
