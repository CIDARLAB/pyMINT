from typing import Optional

from parchmint.target import Target


class MINTTarget(Target):
    """Target class that abstracts Parchmint Target class"""

    def __init__(self, componentstring: str, portstring: Optional[str] = None, target_ref: Optional[Target] = None) -> None:
        super(MINTTarget, self).__init__(None)
        self._target = target_ref if target_ref is not None else Target()
        self._target.component = componentstring
        self._target.port = portstring

    def to_MINT(self) -> str:
        """MINT formatted string of the target  <component_name, port>

        Returns:
            str: MINT string
        """
        ret = "{} {}".format(self._target.component, "" if self._target.port is None else self._target.port)
        return ret
