from core.field_constants import qualified_emergence, relational_condition


GRID = (0.0, 0.1, 0.5, 0.9, 1.0)


def test_product_never_exceeds_any_constitutive_dependency():
    for r in GRID:
        for b in GRID:
            for n in GRID:
                assert relational_condition(r, b, n) <= min(r, b, n)


def test_relational_condition_is_monotonic_in_each_dependency():
    for b in GRID:
        for n in GRID:
            values = [relational_condition(r, b, n) for r in GRID]
            assert values == sorted(values)


def test_qualified_emergence_is_bounded_by_condition_and_raw_emergence():
    for r in GRID:
        for b in GRID:
            for n in GRID:
                for emergence in GRID:
                    value = qualified_emergence(r, b, n, emergence)
                    assert value <= relational_condition(r, b, n)
                    assert value <= emergence
