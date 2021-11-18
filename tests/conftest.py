import pytest
from parchmint import Layer
from parchmint.device import Device


@pytest.fixture
def params_dict():
    ret = {
        "channelWidth": 1000,
        "rotation": 25,
        "direction": "UP",
    }
    return ret


@pytest.fixture
def layer(layer_dict):
    return Layer(layer_dict)


@pytest.fixture
def device(layer):
    device = Device()
    device.add_layer(layer)
    return device


@pytest.fixture
def layer_dict(params_dict):
    ret = {
        "name": "flow_1",
        "id": "FLOW_1",
        "type": "FLOW",
        "group": "",
        "params": params_dict,
    }
    return ret


@pytest.fixture
def device_dict(
    component_dict, connection_dict, feature_dict, layer_dict, valve1_dict, valve2_dict
):
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
        "id": "",
        "type": "ARRAY CONSTRAINT",
        "operation_type": "ALIGNMENT_OPERATION",
        "components": ["c1", "c2", "c3", "c4"],
        "connections": [],
        "params": {
            "is1D": True,
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
        "id": "",
        "type": "LENGTH CONSTRAINT",
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
        "id": "",
        "type": "MIRROR CONSTRAINT",
        "operation_type": "SYMMETRY_OPERATION",
        "components": [],
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
        "id": "",
        "type": "ORIENTATION CONSTRAINT",
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
        "id": "",
        "type": "POSITION CONSTRAINT",
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
        "id": "",
        "type": "ROTATION CONSTRAINT",
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
        "id": "",
        "type": "ORTHOGONAL CONSTRAINT",
        "operation_type": "ALIGNMENT_OPERATION",
        "components": ["source", "c1", "c2", "c3", "c4"],
        "connections": [],
        "params": {},
        "relationships": {},
    }
    return ret
