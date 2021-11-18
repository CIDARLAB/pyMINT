from pymint.constraints.mirrorconstraint import MirrorConstraint
from pymint.mintcomponent import MINTComponent
from pymint.mintlayer import MINTLayer, MINTLayerType


def test_to_parchmint_v1_x(mirror_constraint_json):

    mlayer = MINTLayer("f", "f", "0", MINTLayerType.FLOW)
    mc1 = MINTComponent("c1", "TEST", {"test-key": "test-value"}, [mlayer])
    mc2 = MINTComponent("c2", "TEST", {"test-key": "test-value"}, [mlayer])
    mc3 = MINTComponent("c3", "TEST", {"test-key": "test-value"}, [mlayer])
    mc4 = MINTComponent("c4", "TEST", {"test-key": "test-value"}, [mlayer])

    mc_source = MINTComponent("source", "TEST", {"test-key": "test-value"}, [mlayer])

    mirror_constraint = MirrorConstraint(mc_source, 2)
    mirror_constraint.mirror_groups = [[mc1, mc2], [mc3, mc4]]

    assert mirror_constraint_json == mirror_constraint.to_parchmint_v1_x()
