from typing import List

from parchmint import Component, Layer, Params, Port


class MINTVia:
    """Class to represent MINT Vias that are modelled as a Parchmint component.
    The class has helpful methods for adding and modifying the vias

    """

    def __init__(self, name: str, layers: List[Layer], width: float = 0) -> None:
        """Creates a new instance of a Via

        Args:
            name (str): name/ID of the via
            layers (List[MINTLayer]): List of layer objects where the via is present
        """
        self._component: Component = Component(
            name=name,
            ID=name,
            entity="VIA",
            layers=layers,
            params=Params(),
            xspan=0,
            yspan=0,
            ports_list=[Port(label="1", layer="FLOW", x=0, y=0)],
        )

        self._component.params.set_param("width", width)

    @property
    def width(self) -> float:
        """Returns the width of the via

        Returns:
            float: width of the via
        """
        return self._component.params.get_param("width")

    @width.setter
    def width(self, width: float) -> None:
        """Sets the width of the via

        Args:
            width (float): width of the via
        """
        self._component.params.set_param("width", width)

    @property
    def component(self) -> Component:
        """Returns the component object

        Returns:
            Component: component object
        """
        return self._component
