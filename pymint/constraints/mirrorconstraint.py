from typing import List

from pymint.constraints.layoutconstraint import LayoutConstraint, OperationType
from pymint.mintcomponent import MINTComponent
from pymint.mintdevice import MINTDevice


class MirrorConstraint(LayoutConstraint):
    """Layout constraint when two differnt sub-netlists need to have
    the same layout
    """

    def __init__(self, source_component: MINTComponent, mirror_count=None):
        """Create a new instance of the mirror constraint

        Args:
            source_component (MINTComponent): source for the mirror component to search
            for mirror groups
            mirror_count ([type], optional): number of mirror groups. Defaults to None.
        """
        super().__init__(OperationType.SYMMETRY_OPERATION)
        self._relationship_map["source"] = source_component
        self._relationship_map["mirror_count"] = mirror_count
        self._relationship_map["mirror_groups"] = []

    def add_group(self, components: List[MINTComponent]) -> None:
        """Adds the passed componets to a new group

        Args:
            components (List[MINTComponent]): List of components that need to be in a
            mirror group
        """
        # self.__mirror_groups.append(components)
        self._relationship_map["mirror_groups"].append(components)

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

    def find_mirror_candidates(self, device: MINTDevice) -> None:
        """Traverses the device on the mirror groups

        Args:
            device (MINTDevice): device to traverse

        Raises:
            Exception: if component is not part of any group
        """
        forward_traverse = True
        # TODO -
        # Step 1 - Go through all the outgoing components and create create mirror
        # groups
        G = device.G
        mirror_groups = []

        outgoing_edges = list(G.out_edges(self.mirror_source.ID))
        incoming_edges = list(G.in_edges(self.mirror_source.ID))
        edges_to_use = None
        if len(outgoing_edges) == self.mirror_count:
            forward_traverse = True
            edges_to_use = outgoing_edges
        elif len(incoming_edges) == self.mirror_count:
            forward_traverse = False
            edges_to_use = incoming_edges
        else:
            # Reverse Case Considtion
            if len(incoming_edges) == self.mirror_count:
                forward_traverse = True
                edges_to_use = outgoing_edges
            elif len(outgoing_edges) == self.mirror_count:
                forward_traverse = False
                edges_to_use = incoming_edges
            else:
                raise Exception(
                    "Unable to compute mirror group for source: {}, please check if"
                    " outgoing and incoming channels are declared correctly".format(
                        self.mirror_source
                    )
                )

        sources = []

        for i in range(self.mirror_count):
            if forward_traverse is True:
                component = device.get_component(edges_to_use[i][1])
            else:
                component = device.get_component(edges_to_use[i][0])
            mirror_groups.append([component])
            sources.append(component.ID)

        if forward_traverse is True:
            self.step_forward(sources, mirror_groups, device)
        else:
            self.step_reverse(sources, mirror_groups, device)

        # Step 2 - Save teh mirror groups into our constraint object
        self.__mirror_groups = mirror_groups

    def step_forward(
        self,
        sources: List[str],
        mirror_groups: List[List[MINTComponent]],
        device: MINTDevice,
    ) -> bool:
        """Steps in the forward direction

        Args:
            sources (List[str]): [description]
            mirror_groups (List[List[MINTComponent]]): [description]
            device (MINTDevice): [description]

        Raises:
            Exception: [description]

        Returns:
            bool: [description]
        """
        G = device.G
        outgoing_edges = []
        for source in sources:
            outgoing_edges.extend(list(G.out_edges(source)))

        sink_ids = []
        for edge in list(outgoing_edges):
            sink_ids.append(edge[1])

        # If there is a only 1 common sink, or less than the mirror count, then we
        # gotto kill the mirror groupings
        if len(sink_ids) < self.mirror_count:
            return False

        # Check if all the types of the components are the same
        entities = []
        components = []
        for id in sink_ids:
            component = device.get_component(id)
            entities.append(component.entity)
            components.append(component)

        # If all the entities are the same, include them into the mirror groups
        entity_0 = entities[0]
        fail_flag = False
        for i, unused_element in enumerate(sink_ids):
            entity_i = entities[i]
            if entity_i != entity_0:
                fail_flag = True

        if fail_flag is True:
            return False

        # Since it works, we add everything to the mirror groups, for each of the
        # components see which group the predecessor is in and place it in the
        # corresponding group, if its not in any of the groups something
        # went wrong in the alg
        for component in components:
            assing_group_found_flag = False
            for edge in list(G.in_edges(component.ID)):
                predecessor_component = device.get_component(edge[0])
                for group in mirror_groups:
                    if predecessor_component in group:
                        group.append(component)
                        assing_group_found_flag = True
                        break

            if assing_group_found_flag is False:
                raise Exception(
                    "Could not find the mirror group for component: {}".format(
                        component.ID
                    )
                )

        next_sources = [c.ID for c in components]
        # self.step_forward(next_sources, mirror_groups, device)

        return True

    def step_reverse(
        self,
        sources: List[str],
        mirror_groups: List[List[MINTComponent]],
        device: MINTDevice,
    ) -> bool:
        """Takes a step in reverse


        Args:
            sources (List[str]): [description]
            mirror_groups (List[List[MINTComponent]]): [description]
            device (MINTDevice): [description]

        Raises:
            Exception: [description]

        Returns:
            bool: [description]
        """
        G = device.G
        incoming_edges = []
        for source in sources:
            incoming_edges.extend(list(G.in_edges(source)))

        sink_ids = []
        for edge in list(incoming_edges):
            sink_ids.append(edge[0])

        # If there is a only 1 common sink, or less than the mirror count, then we
        # gotto kill the mirror groupings
        if len(sink_ids) < self.mirror_count:
            return False

        # Check if all the types of the components are the same
        entities = []
        components = []
        for id in sink_ids:
            component = device.get_component(id)
            entities.append(component.entity)
            components.append(component)

        # If all the entities are the same, include them into the mirror groups
        entity_0 = entities[0]
        fail_flag = False
        for i, unused_element in enumerate(sink_ids):
            entity_i = entities[i]
            if entity_i != entity_0:
                fail_flag = True

        if fail_flag is True:
            return False

        # Since it works, we add everything to the mirror groups, for each of the
        # components see which group the predecessor is in and place it in the
        # corresponding group, if its not in any of the groups something
        # went wrong in the alg
        for component in components:
            assing_group_found_flag = False
            for edge in list(G.in_edges(component.ID)):
                predecessor_component = device.get_component(edge[0])
                for group in mirror_groups:
                    if predecessor_component in group:
                        group.append(component)
                        assing_group_found_flag = True
                        break

            if assing_group_found_flag is False:
                raise Exception(
                    "Could not find the mirror group for component: {}".format(
                        component.ID
                    )
                )

        next_sources = [c.ID for c in components]
        # self.step_forward(next_sources, mirror_groups, device)

        return True

    def to_parchmint_v1_x(self):
        ret = super().to_parchmint_v1_x()
        ret["type"] = "MIRROR CONSTRAINT"
        return ret
