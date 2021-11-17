from typing import List, Union

from parchmint.connection import Connection

from pymint.constraints.layoutconstraint import LayoutConstraint
from pymint.mintconnection import MINTConnection


class LengthConstraint(LayoutConstraint):
    """Layout Constriant that will be used for specifying a fixed length
    for a connection

    """

    def __init__(self, connection: MINTConnection, length: float) -> None:
        """Creates a length constraint

        Args:
            component (MINTComponent): component covered by the constraint
            length (float): length of the connection that needs to be fixed
        """
        super().__init__()
        self._connections = []
        self._connections.append(connection)
        self.length = length

    @property
    def connections(self) -> List[Union[MINTConnection, Connection]]:
        """Returns the component covered by the constraint

        Returns:
            MINTComponent: constrained component
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
