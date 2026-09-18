from parchmint import Component, Connection, Layer, Params, Target

from pymint.channel_type import (
    connection_explicit_rounded,
    mint_rounded_channel_token,
)
from pymint.mintterminal import MINTTerminal
from pymint.mintvia import MINTVia


_CONNECTION_PARAM_SKIP = (
    "paths",
    "wayPoints",
    "position",
    "start",
    "end",
    "segments",
    "crossSection",
    "roundedChannel",
    "RoundedChannel",
)


def to_params_MINT(params: Params) -> str:
    """Returns the MINT string of a params

    Args:
        params (Params): Params Object

    Returns:
        str: MINT string fragment
    """
    skip_list = ["paths", "wayPoints", "position", "start", "end", "segments"]
    ret = ""
    for key in params.data:
        if key in skip_list:
            continue
        ret += "{}={} ".format(key, params.data[key])
    return ret


def to_connection_params_MINT(connection: Connection) -> str:
    """CHANNEL params for MINT: RoundedChannel=True/False, never JSON crossSection."""
    params = connection.params
    explicit = connection_explicit_rounded(connection)
    ret = ""
    if explicit is not None:
        ret = mint_rounded_channel_token(explicit) + " "
    if params is None:
        return ret
    for key in params.data:
        if key in _CONNECTION_PARAM_SKIP:
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
    # mint.g4 channelStat is `(entity | 'CHANNEL')`. The CHANNEL keyword is a
    # distinct lexer token, so `ROUNDED CHANNEL name from ...` does not parse.
    # Emit CHANNEL plus RoundedChannel=True/False (JSON still uses crossSection).
    entity = connection.entity or "CHANNEL"
    mint_entity = "CHANNEL" if "ROUND" in str(entity).upper() else entity
    ret = "{} {} from {} to {} {} ;".format(
        mint_entity,
        connection.ID,
        to_target_MINT(connection.source) if connection.source is not None else "",
        ", ".join([to_target_MINT(item) for item in connection.sinks]),
        to_connection_params_MINT(connection),
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
    ret = "LAYER {} \n\n{} \n\nEND LAYER\n\n".format(layer.layer_type, content)
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
