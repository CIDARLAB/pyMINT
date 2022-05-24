from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Union

from parchmint.connection import Connection
from parchmint.layer import Layer
from parchmint.target import Target
from parchmint.params import Params

if TYPE_CHECKING:
    from pymint import MINTLayer

from pymint.mintparams import MINTParams
from pymint.minttarget import MINTTarget


class MINTConnection(Connection):
    """Connection class abstracting parchmint Connection class that adding
    helper methods to generate MINT

    """

    def __init__(
        self,
        name: str,
        technology: str,
        params: Dict,
        source: Target,
        sinks: List[Target],
        layer: MINTLayer,
    ) -> None:
        """Creates a new connection

        Args:
            name (str): name of the connection
            technology (str): MINT string
            params (dict): parameters
            source (MINTTarget): where the connection starts
            sinks (List[MINTTarget]): where the connection ends
            layer (MINTLayer, optional): layer information. Defaults to None.
        """
        self._connection = Connection(
            name=name,
            ID=name,
            entity=technology,
            source=source,
            sinks=sinks,
            layer=layer,
            params=Params(params),
        )

    @property
    def connection(self) -> Connection:
        """Returns the connection

        Returns:
            Connection: the connection
        """
        return self._connection

    def overwrite_id(self, id: str) -> None:
        """Overwites the ID

        Args:
            id (str): New id of the connection
        """
        self.ID = id

    @property
    def connection_spacing(self) -> int:
        """Returns the connection spacing of the component

        Returns:
            int: connection Spacing Value in microns
        """
        return self.params.get_param("channel_spacing")

    @connection_spacing.setter
    def connection_spacing(self, value: int) -> None:
        """Sets the component spacing of the connection

        Args:
            value (int): Value for the connection spacing in microns
        """
        self.params.set_param("channel_spacing", value)

    def to_MINT(self) -> str:
        """Returns the MINT String for the connection

        Returns:
            str: This is the MINT string for the serialization
        """
        ret = "{} {} from {} to {} {} ;".format(
            self.entity,
            self.name,
            self._connection.source.to_MINT(),
            ", ".join([item.to_MINT() for item in self.sinks]),
            self.params.to_MINT(),
        )
        return ret
