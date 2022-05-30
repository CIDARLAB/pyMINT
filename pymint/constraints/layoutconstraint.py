from enum import Enum
from typing import List, Union

from parchmint import Params
from parchmint.component import Component
from parchmint.connection import Connection


class OperationType(Enum):
    """Enum that represents all the differnt types of constraints"""

    CUTSOM_OPERATION = 0
    EXPLICIT_OPERATION = 1
    OPTIONAL_OPERATION = 2
    ALIGNMENT_OPERATION = 3
    SYMMETRY_OPERATION = 4
    RELATIVE_OPERATIONS = 5
    PARAMETER_MATCH = 6


class LayoutConstraint:
    """Base layout constraint class over which all the other constriaint
    classes will be based upon

    """

    def __init__(
        self, operation_type: OperationType = OperationType.CUTSOM_OPERATION
    ) -> None:
        """Creates a new instance of the LayoutConstraint"""
        self._components: List[Union[Component, Component]] = []
        self._connections: List[Union[Connection, Connection]] = []
        self._type: str = ""
        self._operation_type: OperationType = operation_type
        self._params: Params = Params({})

        self._relationship_map = {}

    @property
    def type(self) -> str:
        return self._type

    def add_component(self, component: Component):
        """Adds a component to be covered by the layout constraint

        Args:
            component (Component): Component to be constrained
        """
        self._components.append(component)

    def add_connection(self, connection: Connection):
        """Adds a connection to be covered by the layout constraint

        Args:
            connection (Connection): Connection to be constrained
        """
        self._connections.append(connection)

    def get_components(self) -> List[Union[Component, Component]]:
        """Returns components covered by the constraint

        Returns:
            List[Component]: Constrained components
        """
        return self._components

    def get_connections(self) -> List[Union[Connection, Connection]]:
        """Returns the connections covered byt he constraint

        Returns:
            List[Connection]: Constrained connections
        """
        return self._connections

    def contains_component(self, component: Component) -> bool:
        """Checks if the constraint covers the component

        Args:
            component (Component): component to check

        Returns:
            bool: true if component is present
        """
        return component in self._components

    def contains_connection(self, connection: Connection) -> bool:
        """Checks if the constraint covers the connection

        Args:
            connection (Connection): connection to check

        Returns:
            bool: true if connection is present
        """
        return connection in self._connections

    def convert_objects_to_json_dict(self):
        def convert_entry(entry):
            if isinstance(entry, Component) or isinstance(entry, Connection):
                ret = entry.ID
            elif isinstance(entry, str) or isinstance(entry, int):
                ret = entry
            elif isinstance(entry, list):
                ret = []
                for e in entry:
                    ret.append(convert_entry(e))
            elif isinstance(entry, Enum):
                ret = str(entry)
            else:
                raise Exception(
                    "Unsupported type for key in relationship map: {}".format(
                        type(entry)
                    )
                )
            return ret

        ret = {}
        for key in self._relationship_map.keys():
            value = self._relationship_map[key]
            save_key = convert_entry(key)

            save_value = convert_entry(value)

            ret[save_key] = save_value
        return ret

    def to_parchmint_v1_x(self):
        """Returns the constraint in the Parchmint v1.x format

        Returns:
            Dict: constraint in Parchmint v1.x format
        """
        ret = {}
        ret["type"] = self._type
        ret["operation_type"] = self._operation_type.name
        ret["components"] = [c.ID for c in self._components]
        ret["connections"] = [c.ID for c in self._connections]
        ret["params"] = self._params.to_parchmint_v1()
        ret["relationships"] = self.convert_objects_to_json_dict()

        return ret
