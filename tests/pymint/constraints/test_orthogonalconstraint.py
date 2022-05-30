from pymint.constraints.orthogonalconstraint import OrthogonalConstraint
from parchmint import Component, Layer, Params
from pymint.mintlayer import MINTLayerType


def test_to_parchmint_v1_x(orthogonal_constraint_json):
    mlayer = Layer(layer_id="f", name="f", group="0", layer_type=str(MINTLayerType.FLOW))
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

    mc_source = Component(ID="source", entity="TEST", params=Params({"test-key": "test-value"}), layers=[mlayer])

    orthogonal_constraint = OrthogonalConstraint([mc_source, mc1, mc2, mc3, mc4])
    assert orthogonal_constraint.to_parchmint_v1_x() == orthogonal_constraint_json
