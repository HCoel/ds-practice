import pytest

from ds_practice.stats import trimmed_mean


@pytest.mark.parametrize(
    ("values", "proportion", "expected"),
    [
        ([1, 2, 3, 4, 5], 0.0, 3.0),
        ([1, 2, 3, 4, 100], 0.2, 3.0),  # the outlier gets trimmed
        ([7, 7, 7, 7, 7], 0.2, 7.0),  # all-equal: trimming changes nothing
        ([42], 0.0, 42.0),  # single value: mean is itself
    ],
)
def test_trimmed_mean(values, proportion, expected):
    assert trimmed_mean(values, proportion) == pytest.approx(expected)


def test_empty_raises():
    with pytest.raises(ValueError, match="empty"):
        trimmed_mean([])


def test_bad_proportion_raises():
    with pytest.raises(ValueError):
        trimmed_mean([1, 2, 3], 0.5)
