"""MINT channel-type flag vs JSON ``crossSection``.

MINT: ``RoundedChannel=True`` / ``False`` on a ``CHANNEL`` statement.
JSON / 3DuF: ``crossSection`` 1 = rounded stadium, 0 = square ends.

The MINT grammar only accepts lowercase ``param_element`` keys and boolean
``YES`` / ``NO``, so handwritten ``RoundedChannel=True`` is rewritten to
``roundedChannel=YES`` before parse. After parse, fluigi maps that back to
JSON ``crossSection``. Legacy MINT ``crossSection=1`` is still accepted.
"""
from __future__ import annotations

import re
from typing import Any, Optional

_TRUE = {"true", "yes", "1", "1.0"}
_FALSE = {"false", "no", "0", "0.0"}

_ROUNDED_RE = re.compile(
    r"(?i)(^|[\s;])RoundedChannel\s*=\s*(True|False|YES|NO|1(?:\.0)?|0(?:\.0)?)"
)
_CROSS_RE = re.compile(r"(^|[\s;])crossSection\s*=\s*(-?\d+(?:\.\d+)?)")


def is_rounded_value(raw: Any) -> bool:
    if isinstance(raw, bool):
        return raw
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        return float(raw) >= 0.5
    return str(raw).strip().lower() in _TRUE


def normalize_mint_channel_type_tokens(text: str) -> str:
    """Rewrite user-facing RoundedChannel / legacy crossSection for mint.g4."""

    def rounded_sub(match: re.Match) -> str:
        yes = match.group(2).strip().lower() in _TRUE
        return "{}roundedChannel={}".format(match.group(1), "YES" if yes else "NO")

    text = _ROUNDED_RE.sub(rounded_sub, text)

    def cross_sub(match: re.Match) -> str:
        yes = float(match.group(2)) >= 0.5
        return "{}roundedChannel={}".format(match.group(1), "YES" if yes else "NO")

    return _CROSS_RE.sub(cross_sub, text)


def apply_mint_channel_type_to_json_params(params) -> None:
    """Replace MINT ``roundedChannel`` with JSON ``crossSection``. Keep explicit crossSection."""
    data = getattr(params, "data", None)
    if not isinstance(data, dict):
        return
    flag = None
    for key in ("roundedChannel", "RoundedChannel"):
        if key in data:
            flag = data.pop(key)
            break
    if flag is None:
        return
    if hasattr(params, "set_param"):
        params.set_param("crossSection", 1 if is_rounded_value(flag) else 0)
    else:
        data["crossSection"] = 1 if is_rounded_value(flag) else 0


def connection_explicit_rounded(connection) -> Optional[bool]:
    """True/False if MINT/JSON named a channel type; None if omitted."""
    params = getattr(connection, "params", None)
    data = getattr(params, "data", {}) if params is not None else {}
    if not isinstance(data, dict):
        data = {}
    for key in ("RoundedChannel", "roundedChannel"):
        if key in data:
            return is_rounded_value(data[key])
    if params is not None and hasattr(params, "exists") and params.exists("crossSection"):
        try:
            return float(params.get_param("crossSection")) >= 0.5
        except (TypeError, ValueError, AttributeError):
            if "crossSection" in data:
                return is_rounded_value(data["crossSection"])
    entity = str(getattr(connection, "entity", "") or "").upper()
    if "ROUND" in entity:
        return True
    return None


def connection_is_rounded(connection) -> bool:
    explicit = connection_explicit_rounded(connection)
    if explicit is not None:
        return explicit
    return False


def mint_rounded_channel_token(rounded: bool) -> str:
    return "RoundedChannel={}".format("True" if rounded else "False")
