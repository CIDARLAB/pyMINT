from typing import Optional, Union

<<<<<<< HEAD
from parchmint.component import Component

from pymint.constraints.layoutconstraint import LayoutConstraint, OperationType
from pymint.mintcomponent import MINTComponent
=======
from pymint.constraints.constraint import LayoutConstraint
from parchmint import Component
>>>>>>> Updated Dependencies


class PositionConstraint(LayoutConstraint):
    """Layout constraint that fixes the location"""

    def __init__(
        self,
        component: Component,
        xpos: Optional[int],
        ypos: Optional[int],
        zpos: Optional[int],
    ) -> None:
        """Returns the position constrinant

        Args:
            component (Component): component covered by the constraint
            xpos (Optional[int]): x position value
            ypos (Optional[int]): y position value
            zpos (Optional[int]): z position value
        """
        super().__init__(OperationType.EXPLICIT_OPERATION)
        self.add_component(component)
        self.xpos = xpos
        self.ypos = ypos
        self.zpos = zpos
        self._type = "POSITION_CONSTRAINT"

<<<<<<< HEAD
    def get_component(self) -> Union[MINTComponent, Component]:
=======
    def get_component(self) -> Component:
>>>>>>> Updated Dependencies
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
    def xpos(self) -> Optional[int]:
        """Returns the x position of the component

        Returns:
            Optional[int]: x coordinate of the component if set else returns None
        """
        if self._params.exists("xpos"):
            return self._params.get_param("xpos")
        else:
            raise KeyError("xpos not set in the constraint")

    @xpos.setter
    def xpos(self, value: Optional[int]) -> None:
        """Sets the x position of the component

        Args:
            value (Optional[int]): x coordinate of the component
        """
        self._params.set_param("xpos", value)

    @property
    def ypos(self) -> Optional[int]:
        """Returns the y position of the component

        Returns:
            Optional[int]: y coordinate of the component if set else returns None
        """
        if self._params.exists("ypos"):
            return self._params.get_param("ypos")
        else:
            raise KeyError("ypos not set in the constraint")

    @ypos.setter
    def ypos(self, value: Optional[int]) -> None:
        """Sets the y position of the component

        Args:
            value (Optional[int]): y coordinate of the component
        """
        self._params.set_param("ypos", value)

    @property
    def zpos(self) -> Optional[int]:
        """Returns the z position of the component

        Returns:
            Optional[int]: z coordinate of the component if set else returns None
        """
        if self._params.exists("zpos"):
            return self._params.get_param("zpos")
        else:
            raise KeyError("zpos not set in the constraint")

    @zpos.setter
    def zpos(self, value: Optional[int]) -> None:
        """Sets the z position of the component

        Args:
            value (Optional[int]): z coordinate of the component
        """
        self._params.set_param("zpos", value)
