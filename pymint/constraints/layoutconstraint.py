from enum import Enum
from typing import Dict, List, Union

from parchmint.component import Component
from parchmint.connection import Connection

from pymint.mintcomponent import MINTComponent
from pymint.mintconnection import MINTConnection
from pymint.mintparams import MINTParams


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
        self._components: List[Union[MINTComponent, Component]] = []
        self._connections: List[Union[MINTConnection, Connection]] = []
        self._id: str = ""
        self._type: str = ""
        self._operation_type: OperationType = operation_type
        self._params: MINTParams = MINTParams({})

        self._relationship_map = {}

    def add_component(self, component: MINTComponent):
        """Adds a component to be covered by the layout constraint

        Args:
            component (MINTComponent): Component to be constrained
        """
        self._components.append(component)

    def add_connection(self, connection: MINTConnection):
        """Adds a connection to be covered by the layout constraint

        Args:
            connection (MINTConnection): Connection to be constrained
        """
        self._connections.append(connection)

    def get_components(self) -> List[Union[MINTComponent, Component]]:
        """Returns components covered by the constraint

        Returns:
            List[MINTComponent]: Constrained components
        """
        return self._components

    def get_connections(self) -> List[Union[MINTConnection, Connection]]:
        """Returns the connections covered byt he constraint

        Returns:
            List[MINTConnection]: Constrained connections
        """
        return self._connections

    def contains_component(self, component: MINTComponent) -> bool:
        """Checks if the constraint covers the component

        Args:
            component (MINTComponent): component to check

        Returns:
            bool: true if component is present
        """
        return component in self._components

    def contains_connection(self, connection: MINTConnection) -> bool:
        """Checks if the constraint covers the connection

        Args:
            connection (MINTConnection): connection to check

        Returns:
            bool: true if connection is present
        """
        return connection in self._connections

    def convert_objects_to_json_dict(self):
        ret = {}
        for key in self._relationship_map.keys():
            value = self._relationship_map[key]
            if isinstance(key, MINTComponent) or isinstance(key, MINTConnection):
                save_key = key.ID
            elif isinstance(key, str) or isinstance(key, int):
                save_key = key
            else:
                raise Exception(
                    "Unsupported type for key in relationship map: {}".format(type(key))
                )

            if isinstance(value, MINTComponent) or isinstance(value, MINTConnection):
                save_value = value.ID
            elif isinstance(key, str) or isinstance(key, int):
                save_value = value.ID
            elif isinstance(value, list):
                if isinstance(value[0], MINTComponent) or isinstance(
                    value[0], MINTConnection
                ):
                    save_value = [v.ID for v in value]
                elif isinstance(value[0], str) or isinstance(value[0], int):
                    save_value = [v for v in value]
                else:
                    raise Exception(
                        "Unsupported type for value in relationship map: {}".format(
                            type(value[0])
                        )
                    )
            else:
                raise Exception(
                    "Unsupported type for value in relationship map: {}".format(
                        type(value)
                    )
                )

            ret[save_key] = save_value
        return ret

    def to_parchmint_v1_x(self):
        """Returns the constraint in the Parchmint v1.x format

        Returns:
            Dict: constraint in Parchmint v1.x format
        """
        ret = {}
        ret["id"] = self._id
        ret["type"] = self._type
        ret["operation_type"] = self._operation_type.name
        ret["components"] = [c.ID for c in self._components]
        ret["connections"] = [c.ID for c in self._connections]
        ret["params"] = self._params.to_parchmint_v1()
        ret["relationships"] = self.convert_objects_to_json_dict()

        return ret
