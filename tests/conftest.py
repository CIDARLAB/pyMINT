import io
from typing import Dict

import pytest
from antlr4 import CommonTokenStream, InputStream
from parchmint import Layer
from parchmint.device import Device

from pymint.antlrgen.mintLexer import mintLexer
from pymint.antlrgen.mintParser import mintParser
from pymint.mintErrorListener import MINTErrorListener


@pytest.fixture
def params_dict() -> Dict:
    ret = {
        "channelWidth": 1000,
        "rotation": 25,
        "direction": "UP",
    }
    return ret


@pytest.fixture
def layer(layer_dict) -> Layer:
    return Layer(layer_dict)


@pytest.fixture
def device(layer) -> Device:
    device = Device()
    device.add_layer(layer)
    return device


@pytest.fixture
def layer_dict(params_dict) -> Dict:
    ret = {
        "name": "flow_1",
        "id": "FLOW_1",
        "type": "FLOW",
        "group": "",
        "params": params_dict,
    }
    return ret


@pytest.fixture
def device_dict(component_dict, connection_dict, feature_dict, layer_dict, valve1_dict, valve2_dict) -> Dict:
    ret = {
        "name": "dev1",
        "params": {
            "x-span": 100000,
            "y-span": 50000,
        },
        "components": [
            component_dict,
            valve1_dict,
            valve2_dict,
        ],
        "connections": [connection_dict],
        "features": [feature_dict],
        "layers": [layer_dict],
        "valveMap": {
            "valve1": "con1",
            "valve2": "con1",
        },
        "valveTypeMap": {
            "valve1": "NORMALLY_OPEN",
            "valve2": "NORMALLY_CLOSED",
        },
        "version": "1.2",
    }
    return ret


@pytest.fixture
def array_constraint_json():
    ret = {
        "type": "ARRAY_CONSTRAINT",
        "operation_type": "ALIGNMENT_OPERATION",
        "components": ["c1", "c2", "c3", "c4"],
        "connections": [],
        "params": {
            "horizontalSpacing": 500,
            "verticalSpacing": 500,
            "xdim": 2,
            "ydim": 1,
        },
        "relationships": {},
    }
    return ret


@pytest.fixture
def length_constraint_json():
    ret = {
        "type": "LENGTH_CONSTRAINT",
        "operation_type": "CUTSOM_OPERATION",
        "components": [],
        "connections": ["mcon1"],
        "params": {"length": 5000},
        "relationships": {},
    }
    return ret


@pytest.fixture
def mirror_constraint_json():
    ret = {
        "type": "MIRROR_CONSTRAINT",
        "operation_type": "SYMMETRY_OPERATION",
        "components": ["c1", "c2", "c3", "c4"],
        "connections": [],
        "params": {},
        "relationships": {
            "source": "source",
            "mirror_count": 2,
            "mirror_groups": [["c1", "c2"], ["c3", "c4"]],
        },
    }
    return ret


@pytest.fixture
def orientation_constraint_json():
    ret = {
        "type": "ORIENTATION_CONSTRAINT",
        "operation_type": "RELATIVE_OPERATIONS",
        "components": ["c1", "c2", "c3", "c4"],
        "connections": [],
        "params": {},
        "relationships": {
            "c1": "HORIZONTAL",
            "c2": "VERTICAL",
            "c3": "HORIZONTAL",
            "c4": "VERTICAL",
        },
    }
    return ret


@pytest.fixture
def position_constraint_json():
    ret = {
        "type": "POSITION_CONSTRAINT",
        "operation_type": "EXPLICIT_OPERATION",
        "components": ["source"],
        "connections": [],
        "params": {"xpos": 500, "ypos": 500, "zpos": 500},
        "relationships": {},
    }
    return ret


@pytest.fixture
def rotation_constraint_json():
    ret = {
        "type": "ROTATION_CONSTRAINT",
        "operation_type": "EXPLICIT_OPERATION",
        "components": ["source"],
        "connections": [],
        "params": {"rotation": 90},
        "relationships": {},
    }
    return ret


@pytest.fixture
def orthogonal_constraint_json():
    ret = {
        "type": "ORTHOGONAL_CONSTRAINT",
        "operation_type": "ALIGNMENT_OPERATION",
        "components": ["source", "c1", "c2", "c3", "c4"],
        "connections": [],
        "params": {},
        "relationships": {},
    }
    return ret


def generate_lisp_tree(source_code: str) -> str:
    """Generates a lisp style tree from a MINT source code string

    Args:
        source_code (str): Source code that you want to parse

    Raises:
        Exception: Incase errors are thrown or the mint syntax is invalid

    Returns:
        str: Lisp style tree
    """

    istream = InputStream(source_code)

    lexer = mintLexer(istream)

    stream = CommonTokenStream(lexer)

    parser = mintParser(stream)

    syntax_errors = parser.getNumberOfSyntaxErrors()
    if syntax_errors > 0:
        raise Exception("Could not parse the MINT SYNTAX")
    # Connect the Error Listener
    parse_output = io.StringIO()
    parse_output.write("MINT SYNTAX ERRORS:\n")

    error_listener = MINTErrorListener(parse_output)
    parser.addErrorListener(error_listener)

    tree = parser.netlist()

    lisp_string = tree.toStringTree(recog=parser)

    return " ".join(lisp_string.split())
