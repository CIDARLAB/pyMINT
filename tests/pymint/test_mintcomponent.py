from pymint import MINTComponent


def test_to_MINT(params_dict, layer):
    """
    Test that the MINTComponent class can be converted to a MINT
    """
    component = MINTComponent("c1", "TEST", params_dict, [layer])
    params_string = ""
    for param in params_dict:
        params_string += param + "=" + str(params_dict[param]) + " "
    assert component.to_MINT() == "TEST c1 {};".format(params_string)
