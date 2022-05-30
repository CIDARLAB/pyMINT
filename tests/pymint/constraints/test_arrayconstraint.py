from parchmint import Component, Layer, Params

from pymint.constraints.arrayconstraint import ArrayConstraint
from pymint.mintlayer import MINTLayerType


def test_to_parchmint_v1_x(array_constraint_json):
    mlayer = Layer(
        layer_id="f", name="f", group="0", layer_type=str(MINTLayerType.FLOW)
    )
    mc1 = Component(
        ID="c1",
        entity="TEST",
        params=Params({"test-key": "test-value"}),
        layers=[mlayer],
    )
    mc2 = Component(
        ID="c2",
        entity="TEST",
        params=Params({"test-key": "test-value"}),
        layers=[mlayer],
    )
    mc3 = Component(
        ID="c3",
        entity="TEST",
        params=Params({"test-key": "test-value"}),
        layers=[mlayer],
    )
    mc4 = Component(
        ID="c4",
        entity="TEST",
        params=Params({"test-key": "test-value"}),
        layers=[mlayer],
    )

    array_constraint = ArrayConstraint(
        [
            mc1,
            mc2,
            mc3,
            mc4,
        ],
        2,
        1,
        500,
        500,
    )

    assert array_constraint.to_parchmint_v1_x() == array_constraint_json
