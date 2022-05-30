from parchmint import Component

from pymint.constraints.layoutconstraint import LayoutConstraint, OperationType


class RotationConstraint(LayoutConstraint):
    """Layout constraint that fixed the absolute rotation
    of the component

    """

    def __init__(self, component: Component, rotation: float) -> None:
        """Creates a Rotation constraint

        Args:
            component (Component): Component to be covered by the constraint
            rotation (float): rotation fixed by the constraint
        """
        super().__init__(OperationType.EXPLICIT_OPERATION)
        self._components.append(component)
        self.rotation = rotation
        self._type = "ROTATION_CONSTRAINT"

    @property
    def component(self) -> Component:
        """Returns the component covered by the constraint

        Returns:
            Component: constrianed component
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
