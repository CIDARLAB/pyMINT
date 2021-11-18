from enum import Enum
from typing import Dict

from pymint.constraints.layoutconstraint import LayoutConstraint, OperationType
from pymint.mintcomponent import MINTComponent


class ComponentOrientation(Enum):
    """Enum ot represent component's relative orientation"""

    HORIZONTAL = 0
    VERTICAL = 1

    def __str__(self) -> str:
        if self == ComponentOrientation.HORIZONTAL:
            return "HORIZONTAL"
        elif self == ComponentOrientation.VERTICAL:
            return "VERTICAL"
        else:
            raise Exception("Could not generate MINT Layer string")

    def __eq__(self, o: object) -> bool:
        if o.__class__ is ComponentOrientation:
            return super().__eq__(o)
        elif o.__class__ is str:
            if self is ComponentOrientation.HORIZONTAL and o == "HORIZONTAL":
                return True
            elif self is ComponentOrientation.HORIZONTAL and o == "VERTICAL":
                return True
            else:
                return False
        else:
            return False


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

    def to_parchmint_v1_x(self):
        ret = super().to_parchmint_v1_x()
        ret["type"] = "ORIENTATION CONSTRAINT"
        return ret
