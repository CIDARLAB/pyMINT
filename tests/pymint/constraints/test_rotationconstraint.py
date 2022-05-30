from parchmint import Component, Layer, Params

from pymint.constraints.rotationconstraint import RotationConstraint
from pymint.mintlayer import MINTLayerType


def test_to_parchmint_v1_x(rotation_constraint_json):
    mlayer = Layer("f", "f", "0", str(MINTLayerType.FLOW))

    mc_source = Component(
        ID="source",
        entity="TEST",
        params=Params({"test-key": "test-value"}),
        layers=[mlayer],
    )
    rotation_constraint = RotationConstraint(mc_source, 90)
    assert rotation_constraint.to_parchmint_v1_x() == rotation_constraint_json
