from pymint.constraints.orthogonalconstraint import OrthogonalConstraint
from pymint.mintcomponent import MINTComponent
from pymint.mintlayer import MINTLayer, MINTLayerType


def test_to_parchmint_v1_x(orthogonal_constraint_json):
    mlayer = MINTLayer("f", "f", "0", MINTLayerType.FLOW)
    mc1 = MINTComponent("c1", "TEST", {"test-key": "test-value"}, [mlayer])
    mc2 = MINTComponent("c2", "TEST", {"test-key": "test-value"}, [mlayer])
    mc3 = MINTComponent("c3", "TEST", {"test-key": "test-value"}, [mlayer])
    mc4 = MINTComponent("c4", "TEST", {"test-key": "test-value"}, [mlayer])
    mc_source = MINTComponent("source", "TEST", {"test-key": "test-value"}, [mlayer])

    orthogonal_constraint = OrthogonalConstraint([mc_source, mc1, mc2, mc3, mc4])
    assert orthogonal_constraint.to_parchmint_v1_x() == orthogonal_constraint_json
