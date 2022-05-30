from parchmint import Component, Layer, Params

from pymint.constraints.positionconstraint import PositionConstraint
from pymint.mintlayer import MINTLayerType


def test_to_parchmint_v1_x(position_constraint_json):
    mlayer = Layer(
        layer_id="f", name="f", group="0", layer_type=str(MINTLayerType.FLOW)
    )

    mc_source = Component(
        ID="source",
        entity="TEST",
        params=Params({"test-key": "test-value"}),
        layers=[mlayer],
    )

    position_constraint = PositionConstraint(mc_source, 500, 500, 500)

    assert position_constraint.to_parchmint_v1_x() == position_constraint_json
