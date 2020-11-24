from pymint.constraints.constraint import LayoutConstraint
from pymint import MINTComponent


class RotationConstraint(LayoutConstraint):
    def __init__(self, component: MINTComponent, rotation: float) -> None:
        super().__init__()
        self._components.append(component)
        self.__rotation = rotation
    
    @property
    def component(self) -> MINTComponent:
        return self._components[0]

    @property
    def rotation(self) -> float:
        return self.__rotation
