import polars as pl

from ds_practice.ingest import clean_trips
from ds_practice.schemas import Trips


def test_clean_trips_removes_bad_rows(good_trips):
    good_trips_neg = good_trips.with_columns(pl.col("fare_amount") * -1)
    dirty = pl.concat([good_trips, good_trips_neg])

    result = clean_trips(dirty.lazy()).collect()
    assert len(result) == 3
    Trips.validate(result)
