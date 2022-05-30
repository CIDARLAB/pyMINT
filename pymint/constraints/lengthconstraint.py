from typing import List

from parchmint import Connection

from pymint.constraints.layoutconstraint import LayoutConstraint


class LengthConstraint(LayoutConstraint):
    """Layout Constriant that will be used for specifying a fixed length
    for a connection

    """

    def __init__(self, connection: Connection, length: float) -> None:
        """Creates a length constraint

        Args:
            component (Component): component covered by the constraint
            length (float): length of the connection that needs to be fixed
        """
        super().__init__()
        self._type = "LENGTH_CONSTRAINT"
        self._connections = []
        self._connections.append(connection)
        self.length = length

    @property
    def connections(self) -> List[Connection]:
        """Returns the component covered by the constraint

        Returns:
            Component: constrained component
        """
        return self._connections

    @property
    def length(self) -> float:
        """Returns the length fixed by the constraint

        Returns:
            float: length constrained
        """
        if self._params.exists("length"):
            return self._params.get_param("length")
        else:
            raise KeyError("is1D not set in the constraint")

    @length.setter
    def length(self, length: float) -> None:
        """Sets the length fixed by the constraint

        Args:
            length (float): length constrained
        """
        self._params.set_param("length", length)
