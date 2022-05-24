from typing import Dict
from parchmint.params import Params


class MINTParams(Params):
    """Params class that abstracts Parchmint Params with
    MINT compatible options

    """

    def __init__(self, pairs: Dict = {}) -> None:
        """Creates a MINTParams object

        Args:
            pairs (Dict): dictionary of key value pairs
        """
        self._params = Params(pairs)

    def to_MINT(self) -> str:
        """Returns the MINT string for the set params, it skips the connection/constriant/position params

        Returns:
            str: MINT string
        """
        skip_list = ["paths", "wayPoints", "position"]
        ret = ""
        for key in self._params.data:
            if key in skip_list:
                continue
            ret += "{}={} ".format(key, self.data[key])
        return ret
