from pymint.constraints.constraint import LayoutConstraint
from pymint.mintcomponent import MINTComponent
from typing import List


class ArrayConstraint(LayoutConstraint):
    def __init__(self, components: List[MINTComponent], xdim=None, ydim=1, horizontal_spacing = None, vertical_spacing= None) -> None:
        super().__init__()
        self._components.extend(components)
        self.__is1D = False

        if xdim is None:
            self.__xdim = len(self._components)
        else:
            self.__xdim = xdim
        
        if ydim is None:
            self.__is1D = True
        else:
            self.__ydim = ydim

    @property
    def is1D(self) -> bool:
        return self.__is1D

    @property
    def xdim(self) -> int:
        return self.__xdim
    
    @property
    def ydim(self) -> int:
        return self.__ydim

    @property
    def dim(self) -> int:
        return self.__xdim

    