from pymint.constraints.positionconstraint import PositionConstraint
from pymint.mintcomponent import MINTComponent
from pymint.mintlayer import MINTLayer, MINTLayerType


def test_to_parchmint_v1_x(position_constraint_json):
    mlayer = MINTLayer("f", "f", "0", MINTLayerType.FLOW)

    mc_source = MINTComponent("source", "TEST", {"test-key": "test-value"}, [mlayer])

    position_constraint = PositionConstraint(mc_source, 500, 500, 500)

    assert position_constraint.to_parchmint_v1_x() == position_constraint_json
