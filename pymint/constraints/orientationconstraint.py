from pymint.constraints.constraint import LayoutConstraint
from typing import Dict
from pymint.mintcomponent import MINTComponent
from enum import Enum


class ComponentOrientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class OrientationConstraint(LayoutConstraint):
    def __init__(self) -> None:
        """Creates an instance of the orientation constraint"""
        super().__init__()
        self.__orientation_map: Dict[MINTComponent, ComponentOrientation] = dict()

    def add_component(
        self, component: MINTComponent, orientation: ComponentOrientation
    ) -> None:
        """Adds a component onto the constraint

        Args:
            component (MINTComponent): component covered by the constraint
            orientation (ComponentOrientation): orientation to set
        """
        super().add_component(component)
        self.__orientation_map[component] = orientation

    @property
    def orientation_map(self) -> Dict[MINTComponent, ComponentOrientation]:
        """Retuns the map of all the components and their corresponding orientation

        Returns:
            Dict[MINTComponent, ComponentOrientation]: dict mapping the components and thier orientations
        """
        return self.__orientation_map
