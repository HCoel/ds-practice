from datetime import UTC, datetime

import pandera.polars as pa
import polars as pl
import pytest

from ds_practice.events import to_frame
from ds_practice.schemas import Events


def test_to_frame_types(fake_resp):
    df = to_frame(fake_resp)
    # TODO 5: shape (3, 8), ts → Datetime[us, UTC], org_id → Int64
    assert df.shape == (3, 8)
    assert df.schema["ts"] == pl.Datetime("us", "UTC")
    assert df.schema["org_id"] == pl.Int64
    # TODO 6: first ts = 4 Oct 2026 20:54:04.394 UTC (Melbourne UTC+11 → subtract 11h)
    assert df["ts"][0] == datetime(2026, 10, 4, 20, 54, 4, 394000, tzinfo=UTC)


def test_pageviews_only_still_types(fake_resp):
    fake_resp["results"] = fake_resp["results"][:1]
    # TODO 7: assert org_id is still Int64. Without TODO 3, what dtype would it be?
    df = to_frame(fake_resp)
    assert df.schema["org_id"] == pl.Int64


def test_good_events_pass(fake_resp):
    Events.validate(to_frame(fake_resp))


CORRUPTIONS = {
    "duplicate_id": lambda df: pl.concat([df, df.head(1)]),
    # TODO 6: "billing_without_org": set org_id to pl.lit(None, pl.Int64)
    "billing_without_org": lambda df: df.with_columns(
        pl.lit(None, pl.Int64).alias("org_id")
    ),
    # TODO 7: "unknown_host": host = "localhost"
    "unknown_host": lambda df: df.with_columns(pl.lit("localhost").alias("host")),
    # TODO 8: "server_event": event = "Billing Webhook"
    "server_event": lambda df: df.with_columns(
        pl.lit("Billing Webhook").alias("event")
    ),
}


@pytest.mark.parametrize("name", CORRUPTIONS)
def test_corruption_is_caught(fake_resp, name):
    bad = CORRUPTIONS[name](to_frame(fake_resp))
    # TODO 9: assert Events.validate(bad) raises pa.errors.SchemaError
    with pytest.raises(pa.errors.SchemaError):
        Events.validate(bad)
