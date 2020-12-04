from __future__ import annotations
from typing import List
from pymint.mintparams import MINTParams
from parchmint.component import Component
from pymint import MINTLayer


class MINTComponent(Component):
    def __init__(
        self, name: str, technology: str, params: dict, layers: List[MINTLayer] = None
    ) -> None:
        super().__init__()
        self.name = name
        self.ID = name
        self.entity = technology
        self.params = MINTParams(params)
        if layers is None:
            raise Exception("Cannot have no layer information")
        for layer in layers:
            self.layers.append(layer)

    def overwrite_id(self, id: str) -> None:
        self.ID = id

    @property
    def component_spacing(self) -> int:
        return self.params.get_param("component_spacing")

    @component_spacing.setter
    def connection_spacing(self, value: int) -> None:
        self.params.set_param("component_spacing", value)

    def to_MINT(self) -> str:
        ret = "{} {} {};".format(self.entity, self.name, self.params.to_MINT())
        return ret

    def __hash__(self) -> int:
        return hash((self.ID, self.entity))
