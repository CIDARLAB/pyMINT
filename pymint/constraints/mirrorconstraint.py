import queue
from typing import List, Dict
import networkx as nx
from pymint.constraints.layoutconstraint import LayoutConstraint, OperationType
from pymint.mintcomponent import MINTComponent
from pymint.mintdevice import MINTDevice


class MirrorConstraint(LayoutConstraint):
    """Layout constraint when two differnt sub-netlists need to have
    the same layout
    """

    class DistanceDictionaries:
        """Distance dictionaries are the data structures we are using to solve the
        mirror grouping problem. This algoithm creates dictionaries based on the
        distances of each of the components to the `source components`that are the 
        original decendentants of the `mirror driving component`.

        The datastructure essentially looks like this:
        -----                                                                 -----
        | 0 : [source_node]      0: [source_node]      0: [source_node]           |
        | 1 : [node1, node2]     1: [node1, node2]     1: [node1, node2]          |
        | 2 : [node1, node2]     2: [node1, node2]     2: [node1, node2]          |
        | 3 : [node1, node2]  ,  3: [node1, node2]  ,  3: [node1, node2] ,  ...   |
        | 4 : [node1, node2]     4: [node1, node2]     4: [node1, node2]          |
        | 5 : [node1, node2]     5: [node1, node2]     5: [node1, node2]          |
        | 6 : [node1, node2]     6: [node1, node2]     6: [node1, node2]          |
        | 7 : [node1, node2]     7: [node1, node2]     7: [node1, node2]          |
        -----                                                                 -----

        Its a list of dictionaries where the keys are the distances to the source.
        If we trim and prune this entire data structure, we will get the final 
        list of groups that we can export.

        """

        def __init__(
            self, groups_size: int, device: MINTDevice, undirected_netlist
        ) -> None:

            # Initialize the dictionaries (the base data structure) with as many
            # dictionaries as we have groups
            self.dictionaries: List[Dict[int, List[str]]] = [
                {} for x in range(groups_size)
            ]
            self.netlist = undirected_netlist
            self.device = device

        def load_group_dfs_nodes(self, group_index, dfs_nodes: List[str]) -> None:
            """
            Loads the DFS nodes of a group into the dictionary.
            """

            # Find the source node of the group
            source = dfs_nodes[0]
            self.set_source(group_index, source)
            # Find distances of each of the DFS nodes to the source node and save it into
            # the dictionary
            for node in dfs_nodes:
                shortest_path = nx.shortest_path(
                    self.netlist, source=source, target=node
                )
                self.set_group_node(group_index, node, len(shortest_path))

        def set_source(self, group_index: int, node: str):
            self.dictionaries[group_index][0].append(node)

        def set_group_node(self, group_index: int, node: str, distance: int):
            self.dictionaries[group_index][distance].append(node)

        def trim_uneven_distaces(self) -> None:
            # Step 1 - Find the largest distance in each of the dictionaries
            largest_distances = []
            for group_dictionary in self.dictionaries:
                largest_distances.append(max(group_dictionary.keys()))

            # Step 2 - Find the min of these last distances and remove all the distances
            # beyond that from the dictionaries
            min_distance = min(largest_distances)

            self.trim_dictionaries(min_distance + 1)

        def trim_dictionaries(self, limit: int) -> None:
            """Removes all the dictionarie entries that have a distance greater than or
            equal to the limit"""
            for group_dictionary in self.dictionaries:
                for distance_key in group_dictionary.keys():
                    if distance_key >= limit:
                        del group_dictionary[distance_key]

        def prune_non_group_nodes(self) -> None:
            # Step 1 - Go through each group
            # Step 2 - Go through the nodes at each distance
            # Step 3 - Get the shortest path from the source to each node
            # Step 4 - If all the nodes in the shortest path are not in the group, remove
            # the node from the group
            for group_index in range(len(self.dictionaries)):
                group_dictionary = self.dictionaries[group_index]
                source = group_dictionary[0][0]
                for distance in group_dictionary.keys():
                    nodes = group_dictionary[distance]
                    # Get shortest path
                    shortest_path = nx.shortest_path(
                        self.netlist, source=source, target=nodes[0]
                    )
                    # If any of the noes in the shortest_path are not in the group, remove the node
                    for node in shortest_path:
                        if self.is_node_in_group(node=node, group_index=group_index):
                            self.remove_node_from_group(group_index, node)

        def prune_non_matching_nodes(self) -> None:

            # First check if the intersection of every level of types is null or not
            # this will get rid of any levels that don't have the same types of nodes
            ref_group = self.dictionaries[0]
            found_flag = False
            limit = 0
            for distance_key in ref_group.keys():
                ref_component_type_set = set(
                    [
                        self.device.get_component(cid).entity
                        for cid in ref_group[distance_key]
                    ]
                )
                for group_index in range(1, len(self.dictionaries)):
                    group_to_test = self.dictionaries[group_index]
                    type_set_to_test = set(
                        [
                            self.device.get_component(cid).entity
                            for cid in group_to_test[distance_key]
                        ]
                    )
                    if (
                        len(set.intersection(ref_component_type_set, type_set_to_test))
                        == 0
                    ):
                        found_flag = True
                        limit = distance_key
                        break

                if found_flag:
                    break

            # If we find the mismatch, we delete the entire range starting from the limit
            if found_flag:
                self.trim_dictionaries(limit)

            # Now we need to prune the excess components at each distance (This should get
            # rid of excess cross links at distance = 1)

            # Create a dictionary that keeps the list of the component types at each
            # distance. This becomes the reference list that we pull for every group
            # and pop elements from the copy to get the excess components
            ref_group_types = {}
            for distance_key in ref_group.keys():
                nodes = ref_group[distance_key]
                ref_group_types[distance_key] = [
                    self.device.get_component(cid).entity for cid in nodes
                ]

            for test_group_index in range(1, len(self.dictionaries)):
                test_group = self.dictionaries[test_group_index]

                for distance_key in test_group.keys():
                    ref_types_list = ref_group_types[distance_key].copy()
                    test_nodes = test_group[distance_key]
                    # Loop through the test nodes and remove their corresponding types from the ref_types_list
                    for node_index in range(len(test_nodes)):
                        test_node = test_nodes[node_index]
                        ref_types_list.remove(
                            self.device.get_component(test_node).entity
                        )
                        if len(ref_types_list) == 0:
                            # Remove all the remaining nodes and break from the loop
                            for node_to_remove_index in range(
                                node_index + 1, len(test_nodes)
                            ):
                                self.remove_node_from_group(
                                    test_group_index, test_nodes[node_to_remove_index]
                                )
                            break

        def is_node_in_group(self, group_index: int, node: str) -> bool:
            group_dictionary = self.dictionaries[group_index]
            for nodes in group_dictionary.values():
                if node in nodes:
                    return True
            return False

        def remove_node_from_group(self, group_index: int, node: str) -> None:
            group_dictionary = self.dictionaries[group_index]
            for nodes in group_dictionary.values():
                if node in nodes:
                    nodes.remove(node)

        def generate_groups(self) -> List[List[str]]:
            groups = []
            for group_index in range(len(self.dictionaries)):
                group_dictionary = self.dictionaries[group_index]
                nodes = []
                for distance in group_dictionary.keys():
                    nodes.extend(group_dictionary[distance])
                groups.append(nodes)
            return groups

    def __init__(
        self,
        source_component: MINTComponent,
        mirror_count=None,
        mirror_groups: List[List[MINTComponent]] = [],
    ):
        """Create a new instance of the mirror constraint

        Args:
            source_component (MINTComponent): source for the mirror component to search
            for mirror groups
            mirror_count ([type], optional): number of mirror groups. Defaults to None.
        """
        super().__init__(OperationType.SYMMETRY_OPERATION)
        self._type = "MIRROR_CONSTRAINT"
        self._relationship_map["source"] = source_component
        self._relationship_map["mirror_count"] = mirror_count
        self._relationship_map["mirror_groups"] = []

        # Load all the components
        for group in mirror_groups:
            self.add_group(group)

    def add_group(self, components: List[MINTComponent]) -> None:
        """Adds the passed componets to a new group

        Args:
            components (List[MINTComponent]): List of components that need to be in a
            mirror group
        """
        # self.__mirror_groups.append(components)
        self._relationship_map["mirror_groups"].append(components)
        for component in components:
            self.add_component(component)

    @property
    def mirror_count(self) -> int:
        """Number of mirror groups

        Returns:
            int: number of mirror groups
        """
        return self._relationship_map["mirror_count"]

    @mirror_count.setter
    def mirror_count(self, value: int):
        """Set the number of mirror groups

        Args:
            value (int): number of mirror groups
        """
        self._relationship_map["mirror_count"] = value

    @property
    def mirror_source(self) -> MINTComponent:
        """Returns the mirror source component

        Returns:
            MINTComponent: mirror source
        """
        return self._relationship_map["source"]

    @mirror_source.setter
    def mirror_source(self, value: MINTComponent):
        """Sets the mirror source component


        Args:
            value (MINTComponent): Mirror source component
        """
        self._relationship_map["source"] = value

    @property
    def mirror_groups(self) -> List[List[MINTComponent]]:
        """Returns the mirror groups

        Returns:
            List[List[MINTComponent]]: Mirror groups covered by the constraint
        """
        return self._relationship_map["mirror_groups"]

    @mirror_groups.setter
    def mirror_groups(self, value: List[List[MINTComponent]]):
        """Sets the mirror groups

        Args:
            value (List[List[MINTComponent]]): List of lists of components
        """
        self._relationship_map["mirror_groups"] = value

    @staticmethod
    def find_mirror_groups(
        driving_component: MINTComponent, device: MINTDevice, mirror_count: int
    ) -> List[List[MINTComponent]]:
        def find_component_references(groups: List[List[str]]):
            return [[device.get_component(cid) for cid in group] for group in groups]

        groups = []
        print(
            "Finding mirror groups for driving component: {}".format(
                driving_component.ID
            )
        )
        undirected_netlist = device.G.copy().to_undirected()
        # Remove the driving component from the undirected netlist, this way we don't go backwards in the traversals
        undirected_netlist.remove_node(driving_component.ID)

        # Find out if the incoming or the out going edges are the ones we want to
        # traverse by comparing against the number of mirror groups we need to generate
        outgoing_edges = list(device.G.out_edges(driving_component.ID))
        incoming_edges = list(device.G.in_edges(driving_component.ID))

        level_one_components = []
        if len(outgoing_edges) == mirror_count:
            # Check if all the target nodes of outgoing_edges have the same type of
            # components
            level_one_components = [edge[1] for edge in outgoing_edges]

        elif len(incoming_edges) == mirror_count:
            # Check if all the source nodes of incoming_edges have the same type of
            # components
            level_one_components = [edge[0] for edge in incoming_edges]
        else:
            print(
                "Could not find {} mirror groups for driving component: {}".format(
                    mirror_count, driving_component.ID
                )
            )
            return find_component_references(groups)

        # Check all the level 1 components to see if they are the same type of
        # components
        def is_level_valid(level_components: List[str], mirror_count) -> bool:
            level_components_types = []
            for component in level_components:
                component_type = device.get_component(component).entity
                level_components_types.append(component_type)

            level_components_types_0 = level_components_types[0]
            for i, unused_element in enumerate(level_components_types):
                if level_components_types[i] != level_components_types_0:
                    return False
            # If the number of components in the level are not the same, then its not a
            # valid level
            if len(level_components) != mirror_count:
                return False
            return True

        if is_level_valid(level_one_components, mirror_count) is True:
            groups = [[component] for component in level_one_components]
        else:
            print(
                "Could not find {} mirror groups for driving component: {}".format(
                    mirror_count, driving_component.ID
                )
            )
            return find_component_references(groups)

        # Generate the mirror groups using the level Distance Dictionary datastructure.
        # Step 1 - Initialize an instance of the distance dictionaries object
        # Step 2 - Load all the DFS preordered nodes from the each of the sources we find in the currently loaded groups variables
        # Step 3 - Trim the distance dictionary to have min distance of all dfs nodes
        # Step 4 - Run the pruning algorithm (distance + group matching)
        # Step 5 - Run the pruning algorithm (type matching)

        distance_dictionaries = DistanceDictionaries(
            groups_size=len(groups),
            device=device,
            undirected_netlist=undirected_netlist,
        )

        # Find all the dfs orderinging from level_one_components and load them in
        for group_index in range(len(level_one_components)):
            source_node = level_one_components[group_index]
            dfs_nodes = list(nx.dfs_preorder_nodes(undirected_netlist, source_node))
            distance_dictionaries.load_group_dfs_nodes(group_index, dfs_nodes)

        # Trim the distance dictionary to have min distance of all dfs nodes
        distance_dictionaries.trim_uneven_distaces()

        # TODO - Run the pruning algorithm (distance + group matching @distance=1)
        # This is a stupid case that the path algorithm doesn't work for

        # Run the pruning algorithm (distance + group matching)
        distance_dictionaries.prune_non_group_nodes()
        # Run the pruning based on types
        distance_dictionaries.prune_non_matching_nodes()

        # Now search for the next level of compon
        # list(nx.dfs_preorder_nodes(undirected_netlist, source=0))
        return find_component_references(groups)

    @staticmethod
    def generate_constraints(
        mirror_driving_components: List[MINTComponent], device: MINTDevice
    ) -> None:
        """Generate the mirror constraints for the device

        Args:
            mirror_driving_components (List[MINTComponent]): components that are driving the mirror constraint
            device (MINTDevice): device to generate the constraint for
        """
        for mirror_driving_component in mirror_driving_components:
            in_mirror_count = mirror_driving_component.params.get_param("in")
            out_mirror_count = mirror_driving_component.params.get_param("out")

            if in_mirror_count > 1:
                # Find groups for in_mirror_count
                mirror_groups = MirrorConstraint.find_mirror_groups(
                    mirror_driving_component, device, in_mirror_count
                )

                print("In Mirror Groups")
                print(mirror_groups)

                if len(mirror_groups) > 0:
                    # If the number of mirror groups found is great than 0 generate the
                    # mirror constraint
                    mirror_constraint = MirrorConstraint(
                        source_component=mirror_driving_component,
                        mirror_count=len(mirror_groups),
                        mirror_groups=mirror_groups,
                    )

                    device.add_constraint(mirror_constraint)

            if out_mirror_count > 1:
                # Find groups for out_mirror_count
                mirror_groups = MirrorConstraint.find_mirror_groups(
                    mirror_driving_component, device, out_mirror_count
                )
                print("Out Mirror Groups")
                print(mirror_groups)

                if len(mirror_groups) > 0:
                    # If the number of mirror groups found is great than 0 generate the
                    # mirror constraint
                    mirror_constraint = MirrorConstraint(
                        source_component=mirror_driving_component,
                        mirror_count=len(mirror_groups),
                        mirror_groups=mirror_groups,
                    )

                    device.add_constraint(mirror_constraint)
