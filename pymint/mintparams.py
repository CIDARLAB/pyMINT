from parchmint.params import Params


class MINTParams(Params):
    def __init__(self, pairs: dict) -> None:
        """[summary]

        Args:
            pairs (dict): [description]
        """
        super(MINTParams, self).__init__(None)
        for key in pairs.keys():
            self.data[key] = pairs[key]

    def to_MINT(self) -> str:
        """Returns the MINT string for the set params, it skips the connection/constriant/position params

        Returns:
            str: MINT string
        """
        skip_list = ["paths", "wayPoints", "position"]
        ret = ""
        for key in self.data.keys():
            if key in skip_list:
                continue
            ret += "{}={} ".format(key, self.data[key])
        return ret
