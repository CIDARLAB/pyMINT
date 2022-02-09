from typing import List

import networkx as nx

from pymint.constraints.layoutconstraint import LayoutConstraint, OperationType
from pymint.mintcomponent import MINTComponent
from pymint.mintdevice import MINTDevice


class OrthogonalConstraint(LayoutConstraint):
    """Layout constraint used to represent an orthogonal layout
    requirement for a sub-netlist

    """

    def __init__(self, components: List[MINTComponent]) -> None:
        """Creates an orthogonal constraint

        Args:
            components (List[MINTComponent]): components covered by the constraint
        """
        super().__init__(OperationType.ALIGNMENT_OPERATION)
        self._components.extend(components)
        self._type = "ORTHOGONAL_CONSTRAINT"

    def generate_constraints(
        self,
        orthogonal_driving_components: List[MINTComponent],
        device: MINTDevice,
    ) -> None:
        """Generates the constraints for the orthogonal constraint

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
            """Does a DFS traversal based on the node

            (to be used as a recursive function)

            Args:
                root_node (str): node from which we need to do the traversal
            """
            neighbors = list(nx.neighbors(G, root_node))
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
