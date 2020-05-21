from enum import Enum
from pyMINT.mintconnection import MINTConnection
from ..mintcomponent import MINTComponent
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
        self.__components = []
        self.__connections = []
        self.__type: OperationType

    def add_component(self, component: MINTComponent):
        self.__components.append(component)
    
    def add_connection(self, connection: MINTConnection):
        self.__connections.append(connection)

    def get_components(self)->List[MINTComponent]:
        return self.__components

    def contains_component(self, component:MINTComponent) -> bool:
        #TODO: Check if the constraint contains the components, return true / false
        return component in self.__components