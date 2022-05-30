from pymint.constraints.rotationconstraint import RotationConstraint
from pymint.mintcomponent import MINTComponent
from pymint.mintlayer import MINTLayer, MINTLayerType


def test_to_parchmint_v1_x(rotation_constraint_json):
    mlayer = MINTLayer("f", "f", "0", MINTLayerType.FLOW)

    mc_source = MINTComponent("source", "TEST", {"test-key": "test-value"}, [mlayer])
    rotation_constraint = RotationConstraint(mc_source, 90)
    assert rotation_constraint.to_parchmint_v1_x() == rotation_constraint_json
