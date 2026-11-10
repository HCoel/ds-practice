"""Land BuiltGrid PostHog events as a tidy table: one row per user-event."""

from pathlib import Path

import polars as pl

from ds_practice.posthog import read_sql, run_hogql
from ds_practice.schemas import Events

ROOT = Path(__file__).parents[2]
SQL = ROOT / "sql" / "events_28d.sql"


def to_frame(resp: dict) -> pl.DataFrame:
    """PostHog /query/ response -> typed DataFrame, one row per event."""
    return pl.DataFrame(
        resp["results"], schema=resp["columns"], orient="row", infer_schema_length=None
    ).with_columns(
        pl.col("ts").str.to_datetime(time_unit="us", time_zone="UTC"),
        pl.col("org_id").cast(pl.Int64),
        pl.col("plan").cast(pl.String),
    )


def extract_events(out: Path = ROOT / "data" / "events_28d.parquet") -> pl.DataFrame:
    resp = run_hogql(read_sql(SQL), name="ds-practice wk04 events")
    df = Events.validate(to_frame(resp), lazy=True)
    df.write_parquet(out)
    return df
