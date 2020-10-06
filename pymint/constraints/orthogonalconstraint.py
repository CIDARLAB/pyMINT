from pymint.mintdevice import MINTDevice
from parchmint.device import Device
from pymint.mintcomponent import MINTComponent
from pymint.constraints.constraint import LayoutConstraint
from typing import List
import networkx as nx

class OrthogonalConstraint(LayoutConstraint):
    

    def __init__(self, components:List[MINTComponent]) -> None:
        super().__init__()
        self._components.extend(components)

    @staticmethod
    def traverse_node_component_neighbours(component: MINTComponent, device: MINTDevice) -> List[MINTComponent]:
        current_device = device
        ret = []
        G = device.G
        nodes = []
        nodes.append(component)

        def dfs_traverse_nodes(root_node:str):
            neighbors = list(nx.neighbors(G, root_node))
            pass
            for neighbor in neighbors:
                component = current_device.getComponent(neighbor)
                if component in nodes:
                    continue
                if component.entity == 'NODE':
                    nodes.append(component)
                    dfs_traverse_nodes(neighbor)
                else:
                    nodes.append(component)
        
        dfs_traverse_nodes(component.ID)

        return nodes
