from antlr4.error.ErrorListener import ErrorListener
from io import StringIO


class MINTErrorListener(ErrorListener):
    def __init__(self, output: StringIO):
        super().__init__()
        self.output = output
        self._symbol = ""
        self.pass_through = True

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.output.write("Line {}:{} - {}".format(line, column, msg))
        self._symbol = offendingSymbol.text
        self.pass_through = False

    @property
    def symbol(self):
        return self._symbol
