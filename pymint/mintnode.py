from parchmint import Component, Layer, Port


class MINTNode:
    """NODE object that is considered a waypoint in the design
    however this is modelled as a component in Parchmint v1.

    simplifies the creation process and generate all of the
    required MINT.

    """

    def __init__(self, name: str, layer: Layer) -> None:
        """Creates a new NODE object

        Args:
            name (str): name of the node
            layer (str, optional): [description].
        """
        self._component = Component(
            name=name,
            ID=name,
            layers=[layer],
            ports_list=[Port(label="1", layer="FLOW", x=0, y=0)],
            xspan=0,
            yspan=0,
            entity="NODE",
        )

    @property
    def component(self) -> Component:
        """Returns the component object

        Returns:
            Component: component object
        """
        return self._component
