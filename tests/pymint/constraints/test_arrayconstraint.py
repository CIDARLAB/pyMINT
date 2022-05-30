from pymint.constraints.arrayconstraint import ArrayConstraint
from pymint.mintcomponent import MINTComponent
from pymint.mintlayer import MINTLayer, MINTLayerType


def test_to_parchmint_v1_x(array_constraint_json):
    mlayer = MINTLayer("f", "f", "0", MINTLayerType.FLOW)
    mc1 = MINTComponent("c1", "TEST", {"test-key": "test-value"}, [mlayer])
    mc2 = MINTComponent("c2", "TEST", {"test-key": "test-value"}, [mlayer])
    mc3 = MINTComponent("c3", "TEST", {"test-key": "test-value"}, [mlayer])
    mc4 = MINTComponent("c4", "TEST", {"test-key": "test-value"}, [mlayer])

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
