from parchmint import Component, Connection, Layer, Params, Target

from pymint.mintterminal import MINTTerminal
from pymint.mintvia import MINTVia


def to_params_MINT(params: Params) -> str:
    """Returns the MINT string of a params

    Args:
        params (Params): Params Object

    Returns:
        str: MINT string fragment
    """
    skip_list = ["paths", "wayPoints", "position"]
    ret = ""
    for key in params.data:
        if key in skip_list:
            continue
        ret += "{}={} ".format(key, params.data[key])
    return ret


def to_component_MINT(component: Component) -> str:
    """Returns the MINT string of a component

    This functions returns the MINT string of a component.

    Args:
        component (Component): Component object

    Returns:
        str: MINT string fragment
    """
    return "{} {} {};".format(
        component.entity, component.ID, to_params_MINT(component.params)
    )


def to_valve_MINT(component: Component, connection: Connection) -> str:
    """Returns the MINT string of a valve

    This functions returns the MINT string of a valve.

    Args:
        component (Component): Component object
        connection (Connection): Connection object

    Returns:
        str: MINT string fragment
    """
    return "{} {} on {} {};".format(
        component.entity, component.ID, connection.ID, to_params_MINT(component.params)
    )


def to_connection_MINT(connection: Connection) -> str:
    """Returns the MINT String for the connection

    Returns:
        str: This is the MINT string for the serialization
    """
    ret = "{} {} from {} to {} {} ;".format(
        connection.entity,
        connection.ID,
        to_target_MINT(connection.source) if connection.source is not None else "",
        ", ".join([to_target_MINT(item) for item in connection.sinks]),
        to_params_MINT(connection.params),
    )
    return ret


def to_target_MINT(target: Target) -> str:
    """MINT formatted string of the target  <component_name, port>

    Returns:
        str: MINT string
    """
    ret = "{} {}".format(
        target.component,
        "" if target.port is None else target.port,
    )
    return ret


def to_layer_MINT(layer: Layer, content: str) -> str:
    """Generates the MINT string for the layer

    Args:
        content (str): MINT content that needs to be wrapped into the layer MINT

    Returns:
        str: Returns the MINT string fragment
    """
    ret = "LAYER {} \n\n{} \n\nEND LAYER".format(layer.layer_type, content)
    return ret


def to_via_MINT(via: MINTVia) -> str:
    """Returns the MINT string of the via

    Args:
        via (MINTVia): via object

    Returns:
        str: returns the via MINT string fragment
    """
    return "VIA {} {};".format(via.component.ID, to_params_MINT(via.component.params))


def to_terminal_MINT(terminal: MINTTerminal) -> str:
    """Returns the MINT string of the terminal

    Args:
        terminal (MINTTerminal): terminal object

    Returns:
        str: returns the via TERMINAL string fragment
    """
    return "TERMINAL {} {};".format(terminal.component.name, terminal.port_number)
