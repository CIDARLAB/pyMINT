from mintdevice import MINTDevice
from antlr.mintListener import mintListener
from antlr.mintParser import mintParser

class MINTCompiler(mintListener):

    def __init__(self):
        super().__init__()
        self.currentdevice = None

    def enterNetlist(self, ctx: mintParser.NetlistContext):
        self.currentdevice = MINTDevice("DEFAULT_NAME")

    
    def enterHeader(self, ctx: mintParser.HeaderContext):
        self.currentdevice.name = ctx.device_name



