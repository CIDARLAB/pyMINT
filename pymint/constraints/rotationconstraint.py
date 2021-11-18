from typing import Union

from parchmint.component import Component

from pymint import MINTComponent
from pymint.constraints.layoutconstraint import LayoutConstraint, OperationType


class RotationConstraint(LayoutConstraint):
    """Layout constraint that fixed the absolute rotation
    of the component

    """

    def __init__(self, component: MINTComponent, rotation: float) -> None:
        """Creates a Rotation constraint

        Args:
            component (MINTComponent): Component to be covered by the constraint
            rotation (float): rotation fixed by the constraint
        """
        super().__init__(OperationType.EXPLICIT_OPERATION)
        self._components.append(component)
        self.rotation = rotation

    @property
    def component(self) -> Union[MINTComponent, Component]:
        """Returns the component covered by the constraint

        Returns:
            MINTComponent: constrianed component
        """
        return self._components[0]

    @property
    def rotation(self) -> float:
        """Returns the rotation fixed by the rotation

        Returns:
            float: rotation value
        """
        if self._params.exists("rotation"):
            return self._params.get_param("rotation")
        else:
            raise KeyError("rotation not set in the constraint")

    @rotation.setter
    def rotation(self, rotation: float) -> None:
        """Sets the rotation fixed by the constraint

        Args:
            rotation (float): rotation value
        """
        self._params.set_param("rotation", rotation)

    def to_parchmint_v1_x(self):
        ret = super().to_parchmint_v1_x()
        ret["type"] = "ROTATION CONSTRAINT"
        return ret
