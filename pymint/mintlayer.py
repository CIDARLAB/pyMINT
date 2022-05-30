from enum import Enum


class MINTLayerType(Enum):
    """Enum that represents all the differnt types of layers"""

    FLOW = 1
    CONTROL = 2
    INTEGRATION = 3

    def __str__(self) -> str:
        if self == MINTLayerType.FLOW:
            return "FLOW"
        elif self == MINTLayerType.CONTROL:
            return "CONTROL"
        elif self == MINTLayerType.INTEGRATION:
            return "INTEGRATION"
        else:
            raise Exception("Could not generate MINT Layer string")

    def __eq__(self, obj: object) -> bool:
        if obj.__class__ is MINTLayerType:
            return super().__eq__(obj)
        elif obj.__class__ is str:
            if self is MINTLayerType.FLOW and obj == "FLOW":
                return True
            elif self is MINTLayerType.CONTROL and obj == "CONTROL":
                return True
            elif self is MINTLayerType.INTEGRATION and obj == "INTEGRATION":
                return True
            else:
                return False
        else:
            return False
