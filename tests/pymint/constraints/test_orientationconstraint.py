from pymint.constraints.orientationconstraint import (
    ComponentOrientation,
    OrientationConstraint,
)
from pymint.mintcomponent import MINTComponent
from pymint.mintlayer import MINTLayer, MINTLayerType


def test_to_parchmint_v1_x(orientation_constraint_json):
    mlayer = MINTLayer("f", "f", "0", MINTLayerType.FLOW)
    mc1 = MINTComponent("c1", "TEST", {"test-key": "test-value"}, [mlayer])
    mc2 = MINTComponent("c2", "TEST", {"test-key": "test-value"}, [mlayer])
    mc3 = MINTComponent("c3", "TEST", {"test-key": "test-value"}, [mlayer])
    mc4 = MINTComponent("c4", "TEST", {"test-key": "test-value"}, [mlayer])

    orientation_constraint = OrientationConstraint()
    orientation_constraint.add_component_orientation_pair(
        mc1, ComponentOrientation.HORIZONTAL
    )
    orientation_constraint.add_component_orientation_pair(
        mc2, ComponentOrientation.VERTICAL
    )
    orientation_constraint.add_component_orientation_pair(
        mc3, ComponentOrientation.HORIZONTAL
    )
    orientation_constraint.add_component_orientation_pair(
        mc4, ComponentOrientation.VERTICAL
    )

    assert orientation_constraint.to_parchmint_v1_x() == orientation_constraint_json
