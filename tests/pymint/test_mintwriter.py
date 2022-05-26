from parchmint import Component, Connection, Layer, Params, Target

from pymint.mintterminal import MINTTerminal
from pymint.mintvia import MINTVia
from pymint.mintwriter import (to_component_MINT, to_connection_MINT,
                               to_target_MINT, to_terminal_MINT, to_via_MINT)


def test_to_component_MINT(params_dict, layer):
    """
    Test that the Component class can be converted to a MINT
    """
    component = Component(
        name="c1", ID="c1", entity="TEST", params=Params(params_dict), layers=[layer]
    )
    params_string = ""
    for param in params_dict:
        params_string += param + "=" + str(params_dict[param]) + " "
    assert to_component_MINT(component) == "TEST c1 {};".format(params_string)


def test_to_connection_MINT(params_dict, layer):
    """
    Test that the Connection class can be converted to a MINT
    """
    connection = Connection(
        ID="ch1",
        entity="TEST",
        params=Params(params_dict),
        layer=layer,
        source=Target(component_id="c1", port="1"),
        sinks=[Target(component_id="c2", port="1")],
    )
    params_string = ""
    for param in params_dict:
        params_string += param + "=" + str(params_dict[param]) + " "
    assert to_connection_MINT(connection) == "TEST ch1 from c1 1 to c2 1 {};".format(
        params_string
    )


def test_to_target_MINT(params_dict, layer):
    """
    Test that the Target class can be converted to a MINT
    """
    target = Target(json_data={"component": "c1", "port": "1"})

    assert to_target_MINT(target) == "c1 1"

    # target2 = Target(json_data={"component": "c1"})

    # assert to_target_MINT(target2) == "c1"

    target3 = Target(component_id="c1", port="1")

    assert to_target_MINT(target3) == "c1 1"


def test_to_layer_MINT(params_dict, layer):
    """
    Test that the Layer class can be converted to a MINT
    """
    layer = Layer("TEST", params_dict)
    params_string = ""
    for param in params_dict:
        params_string += param + "=" + str(params_dict[param]) + " "
    assert layer.to_MINT() == "TEST {};".format(params_string)


def test_to_via_MINT(params_dict, layer):
    """
    Test that the Via class can be converted to a MINT
    """

    via = MINTVia("via1", [layer], 100)

    assert to_via_MINT(via) == "VIA via1 width=100;"


def test_to_terminal_MINT(layer):
    """
    Test that the Terminal class can be converted to a MINT
    """
    terminal = MINTTerminal("t1", 1, layer)

    assert to_terminal_MINT(terminal) == "TERMINAL t1 1;"
