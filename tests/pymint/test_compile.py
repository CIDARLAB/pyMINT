import json

from pymint.mintdevice import MINTDevice


def ordered(obj):
    """Sort a dictionary object.

    Args:
        obj ([type]): [description]

    Returns:
        [type]: [description]
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def test_bank_test1():
    mint_file = "tests/mint_files/bank_test1.mint"
    mint_device = MINTDevice.from_mint_file(mint_file)
    # Convert it to Parchmint
    parchmint_device = mint_device.to_parchmint()
    # Write the Parchmint to a file
    with open(mint_file.replace(".mint", ".json"), "r") as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        assert parchmint_device == device_json


def test_node_test1():
    mint_file = "tests/mint_files/node_test1.mint"
    mint_device = MINTDevice.from_mint_file(mint_file)
    # Convert it to Parchmint
    parchmint_device = mint_device.to_parchmint()
    # Write the Parchmint to a file
    with open(mint_file.replace(".mint", ".json"), "r") as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        assert parchmint_device == device_json


def test_node_test2():
    mint_file = "tests/mint_files/node_test2.mint"
    mint_device = MINTDevice.from_mint_file(mint_file)
    # Convert it to Parchmint
    parchmint_device = mint_device.to_parchmint()
    # Write the Parchmint to a file
    with open(mint_file.replace(".mint", ".json"), "r") as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        assert parchmint_device == device_json


def test_mirror_test1():
    mint_file = "tests/mint_files/mirror_test1.mint"
    mint_device = MINTDevice.from_mint_file(mint_file)
    # Convert it to Parchmint
    parchmint_device = mint_device.to_parchmint()
    # Write the Parchmint to a file
    with open(mint_file.replace(".mint", ".json"), "r") as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        assert parchmint_device == device_json


def test_mirror_test2():
    mint_file = "tests/mint_files/mirror_test2.mint"
    mint_device = MINTDevice.from_mint_file(mint_file)
    # Convert it to Parchmint
    parchmint_device = mint_device.to_parchmint()
    # Write the Parchmint to a file
    with open(mint_file.replace(".mint", ".json"), "r") as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        assert ordered(parchmint_device) == ordered(device_json)


def test_mirror_test3():
    mint_file = "tests/mint_files/mirror_test3.mint"
    mint_device = MINTDevice.from_mint_file(mint_file)
    # Convert it to Parchmint
    parchmint_device = mint_device.to_parchmint()
    # Write the Parchmint to a file
    with open(mint_file.replace(".mint", ".json"), "r") as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        assert ordered(parchmint_device) == ordered(device_json)


def test_mirror_test4():
    mint_file = "tests/mint_files/mirror_test4.mint"
    mint_device = MINTDevice.from_mint_file(mint_file)
    # Convert it to Parchmint
    parchmint_device = mint_device.to_parchmint()
    # Write the Parchmint to a file
    with open(mint_file.replace(".mint", ".json"), "r") as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        assert ordered(parchmint_device) == ordered(device_json)


def test_grid2():
    mint_file = "tests/mint_files/grid_03.mint"
    mint_device = MINTDevice.from_mint_file(mint_file)
    # Convert it to Parchmint
    parchmint_device = mint_device.to_parchmint()
    # Write the Parchmint to a file
    with open(mint_file.replace(".mint", ".json"), "r") as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        assert ordered(parchmint_device) == ordered(device_json)


def test_valve_test1():
    mint_file = "tests/mint_files/valve_test1.mint"
    mint_device = MINTDevice.from_mint_file(mint_file)
    # Convert it to Parchmint
    parchmint_device = mint_device.to_parchmint()
    # Write the Parchmint to a file
    with open(mint_file.replace(".mint", ".json"), "r") as data_file:
        text = data_file.read()
        device_json = json.loads(text)
        assert ordered(parchmint_device) == ordered(device_json)



# def test_full_flow():

#     # Load each of the .mint files in in the tests/mint_files directory
#     mint_files = glob.glob("tests/mint_files/*.mint")
#     for mint_file in mint_files:
#         # Load the mint file
#         mint_device = MINTDevice.from_mint_file(mint_file)
#         # Convert it to Parchmint
#         parchmint_device = mint_device.to_parchmint()
#         # Write the Parchmint to a file
#         with open(mint_file.replace(".mint", ".json"), "r") as data_file:
#             text = data_file.read()
#             device_json = json.loads(text)
#             assert parchmint_device == device_json

#         # TODO - Now check if two json objects are equal
#         pass
