from typing import Protocol


class MINTProtocol(Protocol):
    """Protocol for MINT objects"""

    def to_MINT(self) -> str:
        """Returns the MINT string for the object

        Returns:
            str: MINT string
        """
        return ""
