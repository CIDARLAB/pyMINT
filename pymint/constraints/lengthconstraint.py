from pymint.mintcomponent import MINTComponent
from pymint.constraints.constraint import LayoutConstraint


class LengthConstraint(LayoutConstraint):
    def __init__(self, component: MINTComponent, length: float) -> None:
        """Creates a length constraint

        Args:
            component (MINTComponent): component covered by the constraint
            length (float): length of the connection that needs to be fixed
        """
        super().__init__()
        self._components.append(component)
        self.__length = length

    @property
    def component(self) -> MINTComponent:
        """Returns the component covered by the constraint

        Returns:
            MINTComponent: constrained component
        """
        return self._components[0]

    @property
    def length(self) -> float:
        """Returns the length fixed by the constraint

        Returns:
            float: length constrained
        """
        return self.__length
