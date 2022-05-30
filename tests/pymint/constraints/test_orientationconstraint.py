from parchmint import Component, Layer, Params

from pymint.constraints.orientationconstraint import (ComponentOrientation,
                                                      OrientationConstraint)
from pymint.mintlayer import MINTLayerType


def test_to_parchmint_v1_x(orientation_constraint_json):
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
