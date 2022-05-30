from parchmint import Connection, Layer, Params, Target

from pymint.constraints.lengthconstraint import LengthConstraint
from pymint.mintlayer import MINTLayerType


def test_to_parchmint_v1_x(length_constraint_json):
    mlayer = Layer(
        layer_id="f", name="f", group="0", layer_type=str(MINTLayerType.FLOW)
    )

    mcon1 = Connection(
        ID="mcon1",
        entity="CHANNEL",
        params=Params({"test-key": "test-value"}),
        source=Target("mc1", "0"),
        sinks=[Target("mc2", "0")],
        layer=mlayer,
    )

    length_constriant = LengthConstraint(mcon1, 5000)

    assert length_constriant.to_parchmint_v1_x() == length_constraint_json
