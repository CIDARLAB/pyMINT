from pymint.constraints.lengthconstraint import LengthConstraint
from pymint.mintconnection import MINTConnection
from pymint.mintlayer import MINTLayer, MINTLayerType
from pymint.minttarget import MINTTarget


def test_to_parchmint_v1_x(length_constraint_json):
    mlayer = MINTLayer("f", "f", "0", MINTLayerType.FLOW)

    mcon1 = MINTConnection(
        "mcon1",
        "TEST_CHANNEL",
        {"test-key": "test-value"},
        MINTTarget("mc1", "0"),
        [MINTTarget("mc2", "0")],
        mlayer,
    )

    length_constriant = LengthConstraint(mcon1, 5000)

    assert length_constriant.to_parchmint_v1_x() == length_constraint_json
