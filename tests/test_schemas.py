import pandera.polars as pa
import polars as pl
import pytest

from ds_practice.schemas import Trips


def test_good_trips_pass(good_trips):
    # TODO 1: validate good_trips. A test with no assert passes if nothing raises.
    Trips.validate(good_trips)


CORRUPTIONS = {
    "negative_fare": pl.col("fare_amount") * -1,
    # TODO 2: "zone_out_of_range": PULocationID = 999
    #         hint: pl.lit(999, dtype=pl.Int32).alias("PULocationID")
    "zone_out_of_range": pl.lit(999, dtype=pl.Int32).alias("PULocationID"),
    # TODO 3: "unknown_payment": payment_type = 9
    "unknown_payment": pl.lit(9, dtype=pl.Int64).alias("payment_type"),
    # TODO 4: "time_travel": dropoff one hour before pickup (pl.duration(hours=1))
    "time_travel": pl.col("dropoff") - pl.duration(hours=1),
    # TODO 5: "fare_as_text": fare_amount cast to pl.String
    "fare_as_text": pl.col("fare_amount").cast(pl.String),
}


@pytest.mark.parametrize("name", CORRUPTIONS)
def test_corruption_is_caught(good_trips, name):
    bad = good_trips.with_columns(CORRUPTIONS[name])
    # TODO 6: assert Trips.validate(bad) raises pa.errors.SchemaError
    with pytest.raises(pa.errors.SchemaError):
        Trips.validate(bad)


# TODO 7: test_missing_column_is_caught: drop "tip_amount",
#         pytest.raises(..., match="not in dataframe")
def test_missing_column_is_caught(good_trips):
    good_trips = good_trips.drop("tip_amount")
    with pytest.raises(pa.errors.SchemaError, match="not in dataframe"):
        Trips.validate(good_trips)


# TODO 8: test_lazy_skips_data_checks: negative fares passed in as .lazy()
#         should NOT raise. Pin last step's surprise with a test.
def test_lazy_skips_data_checks(good_trips):
    bad = good_trips.with_columns(CORRUPTIONS["negative_fare"]).lazy()
    Trips.validate(bad)
