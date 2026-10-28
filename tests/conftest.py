from datetime import datetime as dt

import polars as pl
import pytest


@pytest.fixture
def good_trips() -> pl.DataFrame:
    """Three hand-made trips that should pass the Trips schema."""
    return pl.DataFrame(
        {
            "pickup": [
                dt(2026, 8, 1, 8),
                dt(2026, 8, 1, 9, 30),
                dt(2026, 8, 2, 23, 50),
            ],
            "dropoff": [
                dt(2026, 8, 1, 8, 20),
                dt(2026, 8, 1, 9, 45),
                dt(2026, 8, 3, 0, 10),
            ],
            "passenger_count": [1, None, 2],
            "trip_distance": [3.1, 1.2, 0.0],
            "PULocationID": [132, 237, 161],
            "DOLocationID": [236, 161, 48],
            "payment_type": [1, 2, 0],
            "fare_amount": [18.4, 9.3, 12.0],
            "tip_amount": [4.0, 0.0, 0.0],
            "total_amount": [27.4, 14.3, 17.0],
            "duration_min": [20, 15, 20],
        },
        schema_overrides={"PULocationID": pl.Int32, "DOLocationID": pl.Int32},
    )
