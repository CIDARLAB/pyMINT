from typing import List

from parchmint import Component

from pymint.constraints.layoutconstraint import LayoutConstraint, OperationType


class ArrayConstraint(LayoutConstraint):
    """Array Constraint represents a 1D / 2D array with fixed spacings
    in both dimensions
    """

    def __init__(
        self,
        components: List[Component],
        xdim: int = 1,
        ydim: int = 1,
        horizontal_spacing: float = 0,
        vertical_spacing: float = 0,
    ) -> None:
        """Creates an instance of the array Constraints

        Args:
            components (List[Component]): List of components that need be covered
            by the constraint
            xdim (int, optional): X dimension of the array. Defaults to 1.
            ydim (int, optional): Y dimension of the array. Defaults to 1.
            horizontal_spacing (float, optional): horizontal spacing between the
            components (x-dimension). Defaults to None.
            vertical_spacing (float, optional): vertical spacing between the components
            (y-dimension). Defaults to None.
        """
        super().__init__(OperationType.ALIGNMENT_OPERATION)
        self._type = "ARRAY_CONSTRAINT"
        self._components.extend(components)
        self.horizontal_spacing = horizontal_spacing
        self.vertical_spacing = vertical_spacing

        if xdim is None:
            self.xdim = len(self._components)
        else:
            self.xdim = xdim

        if ydim is None or ydim == 1:
            self.ydim = 1
        else:
            self.ydim = ydim

    @property
    def horizontal_spacing(self) -> float:
        """Gets the horizontal spacing between the components

        Raises:
            KeyError: If the horizontal spacing is not set

        Returns:
            float: The horizontal spacing
        """
        if self._params.exists("horizontalSpacing"):
            return self._params.get_param("horizontalSpacing")
        else:
            raise KeyError("Horizontal spacing is not set in the constraint")

    @horizontal_spacing.setter
    def horizontal_spacing(self, value: float) -> None:
        """sets the horizontal spacing

        Args:
            value (float): The horizontal spacing
        """
        self._params.set_param("horizontalSpacing", value)

    @property
    def vertical_spacing(self) -> float:
        """Gets the vertical spacing between the components

        Raises:
            KeyError: If the vertical spacing is not set

        Returns:
            float: The vertical spacing
        """
        if self._params.exists("verticalSpacing"):
            return self._params.get_param("verticalSpacing")
        else:
            raise KeyError("Vertical spacing is not set in the constraint")

    @vertical_spacing.setter
    def vertical_spacing(self, value: float) -> None:
        """Sets the vertical spacing

        Args:
            value (float): The vertical spacing
        """
        self._params.set_param("verticalSpacing", value)

    @property
    def xdim(self) -> int:
        """Returns the x size of the array

        Returns:
            int: size
        """
        if self._params.exists("xdim"):
            return self._params.get_param("xdim")
        else:
            raise KeyError("is1D not set in the constraint")

    @xdim.setter
    def xdim(self, value: int) -> None:
        """Sets the x dimension of the array

        Args:
            value (int): x dimension
        """
        self._params.set_param("xdim", value)

    @property
    def ydim(self) -> int:
        """Returns the y size of the array

        Returns:
            int: size
        """
        if self._params.exists("ydim"):
            return self._params.get_param("ydim")
        else:
            raise KeyError("ydim not set in the constraint")

    @ydim.setter
    def ydim(self, value: int) -> None:
        """Sets the y dimension of the array

        Args:
            value (int): y dimension
        """
        self._params.set_param("ydim", value)

    @property
    def dim(self) -> int:
        """Returns the size of the array

        Returns:
            int: size
        """
        if self._params.exists("xdim"):
            return self._params.get_param("xdim")
        else:
            raise KeyError("xdim not set in the constraint")

    @dim.setter
    def dim(self, value: int) -> None:
        """Sets the size of the array

        Args:
            value (int): size
        """
        self._params.set_param("xdim", value)
