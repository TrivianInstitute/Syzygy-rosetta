import pytest

from core.field_constants import FieldConstantState, qualified_emergence, relational_condition


def test_rcd_is_the_product_of_constitutive_dependencies():
    assert relational_condition(0.8, 0.5, 0.25) == pytest.approx(0.1)


@pytest.mark.parametrize("scores", [(0.0, 1.0, 1.0), (1.0, 0.0, 1.0), (1.0, 1.0, 0.0)])
def test_no_dependency_can_be_compensated_for(scores):
    assert relational_condition(*scores) == 0.0


def test_emergence_is_downstream_and_relationally_qualified():
    assert qualified_emergence(0.5, 0.5, 0.5, 1.0) == pytest.approx(0.125)
    assert qualified_emergence(1.0, 1.0, 1.0, 0.0) == 0.0


def test_state_is_machine_readable_and_reports_collapsed_dependencies():
    state = FieldConstantState(1.0, 0.0, 0.9, 0.8)
    payload = state.as_dict()
    assert payload["rcd"] == 0.0
    assert payload["qualified_emergence"] == 0.0
    assert payload["collapsed_dependencies"] == ["embodiment"]


def test_context_floors_are_explicit_not_universal():
    state = FieldConstantState(0.8, 0.7, 0.9, 0.6)
    assert state.meets_floors({"reciprocity": 0.75, "embodiment": 0.7})
    assert not state.meets_floors({"non_domination": 0.95})


def test_values_outside_unit_interval_are_rejected():
    with pytest.raises(ValueError):
        FieldConstantState(1.1, 0.5, 0.5, 0.5)
