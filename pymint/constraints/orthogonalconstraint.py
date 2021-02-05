from pymint.mintdevice import MINTDevice
from pymint.mintcomponent import MINTComponent
from pymint.constraints.constraint import LayoutConstraint
from typing import List
import networkx as nx


class OrthogonalConstraint(LayoutConstraint):
    def __init__(self, components: List[MINTComponent]) -> None:
        """Creates an orthogonal constraint

        Args:
            components (List[MINTComponent]): components covered by the constraint
        """
        super().__init__()
        self._components.extend(components)

    @staticmethod
    def traverse_node_component_neighbours(
        component: MINTComponent, device: MINTDevice
    ) -> List[MINTComponent]:
        """Traverses the node networks to find the components covered by the constraint

        Args:
            component (MINTComponent): starting component
            device (MINTDevice): current device

        Returns:
            List[MINTComponent]: list of components covered by the constraint
        """
        current_device = device
        G = device.G
        nodes = []
        nodes.append(component)

        def dfs_traverse_nodes(root_node: str):
            neighbors = list(nx.neighbors(G, root_node))
            pass
            for neighbor in neighbors:
                component = current_device.get_component(neighbor)
                if component in nodes:
                    continue
                if component.entity == "NODE":
                    nodes.append(component)
                    dfs_traverse_nodes(neighbor)
                else:
                    nodes.append(component)

        dfs_traverse_nodes(component.ID)

        return nodes
