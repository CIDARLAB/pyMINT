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
