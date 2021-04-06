from __future__ import annotations
from pymint.mintparams import MINTParams
from parchmint.connection import Connection
from pymint.minttarget import MINTTarget
from typing import List
from pymint import MINTLayer


class MINTConnection(Connection):
    def __init__(
        self,
        name: str,
        technology: str,
        params: dict,
        source: MINTTarget,
        sinks: List[MINTTarget],
        layer: MINTLayer = None,
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
        super(MINTConnection, self).__init__()
        self.name = name
        self.ID = name
        self.entity = technology
        self.params: MINTParams = MINTParams(params)
        self.source: MINTTarget = source
        self.sinks: List[MINTTarget] = sinks
        self.layer = layer

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
            self.source.to_MINT(),
            " ".join([item.to_MINT() for item in self.sinks]),
            self.params.to_MINT(),
        )
        return ret
