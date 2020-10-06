from enum import Enum
from pymint.mintconnection import MINTConnection
from pymint.mintcomponent import MINTComponent
from typing import List

class OperationType(Enum):
    EXPLICIT_OPERATION = 0
    OPTIONAL_OPERATION = 1
    ALIGNMENT_OPERATION = 2
    SYMMETRY_OPERATION = 4
    RELATIVE_OPERATIONS = 5
    PARAMETER_MATCH = 6


class LayoutConstraint(object):

    def __init__(self) -> None:
        self._components = []
        self._connections = []
        self._type: OperationType

    def add_component(self, component: MINTComponent):
        self._components.append(component)
    
    def add_connection(self, connection: MINTConnection):
        self._connections.append(connection)

    def get_components(self)->List[MINTComponent]:
        return self._components

    def contains_component(self, component:MINTComponent) -> bool:
        return component in self._components