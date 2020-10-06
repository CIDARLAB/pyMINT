from pymint.constraints.constraint import LayoutConstraint
from typing import List
from pymint.mintcomponent import MINTComponent

class MirrorConstraint(LayoutConstraint):

    def __init__(self):
        super().__init__()
        self.__mirror_groups: List[List[MINTComponent]] = []

    def add_group(self, components:List[MINTComponent]) -> None:
        self.__mirror_groups.append(components)