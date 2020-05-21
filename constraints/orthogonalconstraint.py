from pyMINT.mintdevice import MINTDevice
from pyparchmint.device import Device
from pyMINT.mintcomponent import MINTComponent
from pyMINT.constraints.constraint import LayoutConstraint
from typing import List
import networkx as nx

class OrthogonalConstraint(LayoutConstraint):
    def __init__(self, components:List[MINTComponent]) -> None:
        super().__init__()
        self.__components = components


    @staticmethod
    def traverse_node_component_neighbours(component: MINTComponent, device: MINTDevice) -> List[MINTComponent]:
        ret = []
        G = device.G
        neighbors = nx.neighbors(G, component.ID)


        return ret
