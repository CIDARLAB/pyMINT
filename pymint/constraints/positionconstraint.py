from parchmint.component import Component

from pymint.constraints.layoutconstraint import LayoutConstraint, OperationType


class PositionConstraint(LayoutConstraint):
    """Layout constraint that fixes the location"""

    def __init__(
        self,
        component: Component,
        xpos: float,
        ypos: float,
        zpos: float,
    ) -> None:
        """Returns the position constrinant

        Args:
            component (Component): component covered by the constraint
            ypos (float): y position value
            zpos (float): z position value
            xpos (float): x position value
        """
        super().__init__(OperationType.EXPLICIT_OPERATION)
        self.add_component(component)
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        self._type = "POSITION_CONSTRAINT"

    def get_component(self) -> Component:
        """Returns the component constrained by the component

        Raises:
            Exception: if the component is not covered by the constraint

        Returns:
            Component: returns the component covered by the constraint
        """
        ret = self._components[0]
        if ret is None:
            raise Exception("No component set for PositionConstraint")

        return ret

    @property
    def xpos(self) -> float:
        """Returns the x position of the component

        Returns:
            float: x coordinate of the component if set else returns None
        """
        if self._params.exists("xpos"):
            return self._params.get_param("xpos")
        else:
            raise KeyError("xpos not set in the constraint")

    @xpos.setter
    def xpos(self, value: float) -> None:
        """Sets the x position of the component

        Args:
            value (float): x coordinate of the component
        """
        self._params.set_param("xpos", value)

    @property
    def ypos(self) -> float:
        """Returns the y position of the component

        Returns:
            float: y coordinate of the component if set else returns None
        """
        if self._params.exists("ypos"):
            return self._params.get_param("ypos")
        else:
            raise KeyError("ypos not set in the constraint")

    @ypos.setter
    def ypos(self, value: float) -> None:
        """Sets the y position of the component

        Args:
            value (float): y coordinate of the component
        """
        self._params.set_param("ypos", value)

    @property
    def zpos(self) -> float:
        """Returns the z position of the component

        Returns:
            float: z coordinate of the component if set else returns None
        """
        if self._params.exists("zpos"):
            return self._params.get_param("zpos")
        else:
            raise KeyError("zpos not set in the constraint")

    @zpos.setter
    def zpos(self, value: float) -> None:
        """Sets the z position of the component

        Args:
            value (float): z coordinate of the component
        """
        self._params.set_param("zpos", value)
