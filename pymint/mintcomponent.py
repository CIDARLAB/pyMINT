from __future__ import annotations
from pymint.mintparams import MINTParams
from parchmint.component import Component
from pymint import MINTLayer


class MINTComponent(Component):
    def __init__(
        self, name: str, technology: str, params: dict, layer: MINTLayer = None
    ) -> None:
        super().__init__()
        self.name = name
        self.ID = name
        self.entity = technology
        self.params = MINTParams(params)
        if layer is None:
            raise Exception("Cannot have no layer information")
        self.layers.append(layer)

    def overwrite_id(self, id: str) -> None:
        self.ID = id

    def to_MINT(self) -> str:
        ret = "{} {} {};".format(self.entity, self.name, self.params.to_MINT())
        return ret

    def __hash__(self) -> int:
        return hash((self.ID, self.entity))
