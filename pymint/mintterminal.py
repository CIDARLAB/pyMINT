from parchmint import Component, Layer, Port


class MINTTerminal:
    """Class for representing the MINT terminal, its modelled as a
    Parchmint Component while giving helpful methods to model the design

    """

    def __init__(self, name: str, port_number: int, layer: Layer) -> None:
        # super(MINTTerminal, self).__init__(name, "TERMINAL", {}, [layer])
        self._component = Component(
            ID=name,
            name=name,
            layers=[layer],
            ports_list=[Port(label="1", layer="FLOW", x=0, y=0)],
            entity="TERMINAL",
        )
        self.__port_number = port_number

    @property
    def port_number(self) -> int:
        """Returns the port number of the terminal (at a device level)

        Returns:
            int: port value
        """
        return self.__port_number

    @property
    def component(self) -> Component:
        """Returns the component object

        Returns:
            Component: component object
        """
        return self._component
