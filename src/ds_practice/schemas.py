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
