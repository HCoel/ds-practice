"""Load NYC yellow-taxi trips as a tidy, validated table."""

from pathlib import Path

import polars as pl

from ds_practice.schemas import Trips


def load_trips(path: str | Path) -> pl.DataFrame:
    """scan -> clean -> collect -> validate. Raises SchemaErrors listing all issues."""
    df = clean_trips(scan_trips(path)).collect()
    return Trips.validate(df, lazy=True)


KEEP = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "PULocationID",
    "DOLocationID",
    "payment_type",
    "fare_amount",
    "tip_amount",
    "total_amount",
]


def scan_trips(path: str | Path) -> pl.LazyFrame:
    """Lazily scan one TLC file, keep the columns we use, add duration."""
    return (
        pl.scan_parquet(path)
        .select(KEEP)
        .rename({"tpep_pickup_datetime": "pickup", "tpep_dropoff_datetime": "dropoff"})
        .with_columns(
            duration_min=(pl.col("dropoff") - pl.col("pickup")).dt.total_minutes()
        )
    )


def clean_trips(lf: pl.LazyFrame) -> pl.LazyFrame:
    """Drop rows with KNOWN, expected TLC quirks. Validation catches the rest."""
    return lf.filter(
        (pl.col("fare_amount") >= 0),
        (pl.col("tip_amount") >= 0),
        (pl.col("total_amount") >= 0),
        (pl.col("duration_min") > 0),
    )
