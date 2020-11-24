from pymint.constraints.constraint import LayoutConstraint
from typing import Dict, overload
from pymint.mintcomponent import MINTComponent
from parchmint.component import Component
from enum import Enum

class ComponentOrientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class OrientationConstraint(LayoutConstraint):
    def __init__(self) -> None:
        super().__init__()
        self.__orientation_map: Dict[MINTComponent, ComponentOrientation] = dict()

    def add_component(self, component:MINTComponent, orientation:ComponentOrientation )->None:
        super().add_component(component)
        self.__orientation_map[component] = orientation

    @property
    def orientation_map(self) -> Dict[MINTComponent, ComponentOrientation]:
        return self.__orientation_map
