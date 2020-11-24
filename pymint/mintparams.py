from parchmint.params import Params


class MINTParams(Params):

    def __init__(self, pairs: dict) -> None:
        super().__init__(None)
        for key in pairs.keys():
            self.data[key] = pairs[key]

    def to_MINT(self):
        ret = ''
        for key in self.data.keys():
            ret += "{}={} ".format(key, self.data[key])
        return ret
    
