from enum import Enum
from typing import Dict

from pymint.constraints.layoutconstraint import LayoutConstraint, OperationType
from pymint.mintcomponent import MINTComponent


class ComponentOrientation(Enum):
    """Enum ot represent component's relative orientation"""

    HORIZONTAL = 0
    VERTICAL = 1


class OrientationConstraint(LayoutConstraint):
    """Layout constraint that setups relative orientations for a
    number of components inside a single layer

    """

    def __init__(self) -> None:
        """Creates an instance of the orientation constraint"""
        super().__init__(OperationType.RELATIVE_OPERATIONS)

    def add_component_orientation_pair(
        self, component: MINTComponent, orientation: ComponentOrientation
    ) -> None:
        """Adds a component onto the constraint

        Args:
            component (MINTComponent): component covered by the constraint
            orientation (ComponentOrientation): orientation to set
        """
        super().add_component(component)
        self._relationship_map[component] = orientation

    @property
    def orientation_map(self) -> Dict[MINTComponent, ComponentOrientation]:
        """Retuns the map of all the components and their corresponding orientation

        Returns:
            Dict[MINTComponent, ComponentOrientation]: dict mapping the components and
             their orientations
        """
        return self._relationship_map
