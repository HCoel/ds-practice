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


COLUMNS = ["event_id", "ts", "person_id", "event", "org_id", "plan", "host", "pathname"]


@pytest.fixture
def fake_resp() -> dict:
    """Shape of a PostHog /query/ response. Made-up IDs, no customer data."""
    return {
        "columns": COLUMNS,
        "results": [
            [
                "e-001",
                "2026-10-05T07:54:04.394000+11:00",
                "p-1",
                "$pageview",
                None,
                None,
                "builtgrid.com",
                "/",
            ],
            [
                "e-002",
                "2026-10-19T09:07:08.632000+11:00",
                "p-2",
                "billing.checkout_opened",
                412.0,
                None,
                "app.builtgrid.com",
                "/billing",
            ],
            [
                "e-003",
                "2026-10-29T08:57:39.410000+11:00",
                "p-2",
                "billing.plan_selected",
                412.0,
                "pro",
                "app.builtgrid.com",
                "/billing/plans",
            ],
        ],
    }
