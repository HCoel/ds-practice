import pandera.polars as pa
import polars as pl


class Trips(pa.DataFrameModel):
    """Contract for one cleaned trip row."""

    pickup: pl.Datetime = pa.Field(nullable=False)
    dropoff: pl.Datetime = pa.Field(nullable=False)
    passenger_count: pl.Int64 = pa.Field(ge=0, le=9, nullable=True)
    trip_distance: pl.Float64 = pa.Field(ge=0)
    fare_amount: pl.Float64 = pa.Field(ge=0)
    tip_amount: pl.Float64 = pa.Field(ge=0)
    PULocationID: pl.Int32 = pa.Field(ge=1, le=265, nullable=False)
    DOLocationID: pl.Int32 = pa.Field(ge=1, le=265, nullable=False)
    payment_type: pl.Int64 = pa.Field(isin=[0, 1, 2, 3, 4, 5, 6])
    total_amount: float
    duration_min: pl.Int64

    @pa.dataframe_check
    def dropoff_after_pickup(self, data):
        return data.lazyframe.select(pl.col("dropoff") >= pl.col("pickup"))

    class Config:
        strict = True  # an unexpected column is an error
        coerce = False  # a wrong dtype is an error, not silently cast


HOSTS = ["app.builtgrid.com", "builtgrid.com"]


class Events(pa.DataFrameModel):
    """Contract for one user-facing BuiltGrid event."""

    event_id: str = pa.Field(unique=True)
    ts: pl.Datetime(time_zone="UTC") = pa.Field(nullable=False)
    person_id: str
    # TODO 1: event matches ^(\$pageview|billing\.[a-z_]+)$   (hint: str_matches=)
    event: str = pa.Field(str_matches="^(\$pageview|billing\.[a-z_]+)$")
    # TODO 2: org_id: pl.Int64, nullable, > 0
    org_id: pl.Int64 = pa.Field(gt=0, nullable=True)
    # TODO 3: plan: str, nullable
    plan: str = pa.Field(nullable=True)
    # TODO 4: host must be in HOSTS; pathname starts with "/"
    host: str = pa.Field(isin=HOSTS)
    pathname: str = pa.Field(str_startswith="/")

    # TODO 5: @pa.dataframe_check billing_has_org: every billing.* row has an org_id
    #   hint: NOT starts_with("billing.") OR org_id is not null, same shape as last week
    @pa.dataframe_check
    def billing_has_org(self, data):
        return data.lazyframe.select(
            (pl.col("event").str.starts_with("billing.").not_())
            | (pl.col("org_id").is_not_null())
        )

    class Config:
        strict = True
        coerce = False
