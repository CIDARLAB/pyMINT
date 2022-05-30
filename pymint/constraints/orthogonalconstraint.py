from typing import List

import networkx as nx
from parchmint import Component

from pymint import MINTDevice
from pymint.constraints.layoutconstraint import LayoutConstraint, OperationType


class OrthogonalConstraint(LayoutConstraint):
    """Layout constraint used to represent an orthogonal layout
    requirement for a sub-netlist

    """

    def __init__(self, components: List[Component]) -> None:
        """Creates an orthogonal constraint

        Args:
            components (List[Component]): components covered by the constraint
        """
        super().__init__(OperationType.ALIGNMENT_OPERATION)
        self._components.extend(components)
        self._type = "ORTHOGONAL_CONSTRAINT"

    @staticmethod
    def generate_constraints(
        orthogonal_driving_components: List[Component],
        device: MINTDevice,
    ) -> None:
        """Generates the orthogonal constraints for the device

        Args:
            orthogonal_driving_components (List[Union[MINTComponent, Component]]): components that are driving the orthogonal constraint
            device (MINTDevice): device to generate the constraints for
        """
        # TODO - Implement this
        orthogonal_component_groups = []

        # Go through the orthogonal driving components and find the groups by performing traversals
        for orthogonal_driving_component in orthogonal_driving_components:
            # Check to see if the component is in any of the groups
            found_group = False
            for group in orthogonal_component_groups:
                if orthogonal_driving_component in group:
                    found_group = True
                    break

            # Skip if the component is already in a group
            if found_group:
                continue

            component_group = OrthogonalConstraint.traverse_node_component_neighbours(
                orthogonal_driving_component, device
            )
            orthogonal_component_groups.append(component_group)

        # Create the orthogonal components
        for component_group in orthogonal_component_groups:
            # TODO - Implement this
            constraint = OrthogonalConstraint(component_group)
            device.add_constraint(constraint)

    @staticmethod
    def traverse_node_component_neighbours(
        component: Component, mint_device: MINTDevice
    ) -> List[Component]:
        """Traverses the node networks to find the components covered by the constraint

        Args:
            component (Component): starting component
            device (MINTDevice): current device

        Returns:
            List[Component]: list of components covered by the constraint
        """
        current_device = mint_device
        graph = mint_device.device.graph.copy().to_undirected()
        nodes = []
        nodes.append(component)

        def dfs_traverse_nodes(root_node: str):
            """Does a DFS traversal based on the node

            (to be used as a recursive function)

            Args:
                root_node (str): node from which we need to do the traversal
            """
            neighbors = list(nx.neighbors(graph, root_node))
            for neighbor in neighbors:
                component = current_device.device.get_component(neighbor)
                if component in nodes:
                    continue
                if component.entity == "NODE":
                    nodes.append(component)
                    dfs_traverse_nodes(neighbor)
                else:
                    nodes.append(component)

        dfs_traverse_nodes(component.ID)

        return nodes
