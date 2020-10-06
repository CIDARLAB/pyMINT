from pymint.constraints.constraint import LayoutConstraint
from pymint.mintcomponent import MINTComponent
from typing import Optional


class PositionConstraint(LayoutConstraint):

    def __init__(self, component: MINTComponent, xpos: Optional[float], ypos: Optional[float], zpos: Optional[float]) -> None:
        super().__init__()
        self.add_component(component)
        self.__xpos = xpos
        self.__ypos = ypos
        self.__zpos = zpos

    def get_component(self) -> MINTComponent:
        ret = self.__components[0]
        if ret is None:
            raise Exception("No component set for PositionConstraint")

        return ret

    @property
    def xpos(self):
        return self.__xpos

    @property
    def ypos(self):
        return self.__ypos

    @property
    def zpos(self):
        return self.__zpos
