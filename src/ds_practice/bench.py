"""Tiny timing harness: run a function several times, keep the best."""

import time
from collections.abc import Callable

import polars as pl


def best_of(fn: Callable[[], object], repeats: int = 5) -> float:
    """Return the fastest wall-clock time (seconds) over `repeats` runs."""
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        times.append(time.perf_counter() - start)
    return min(times)


def bench_table(
    cases: dict[str, Callable[[], object]], repeats: int = 5
) -> pl.DataFrame:
    """Time each named case and return a tidy table, fastest first."""
    rows = [{"case": n, "best_s": best_of(fn, repeats)} for n, fn in cases.items()]
    return (
        pl.DataFrame(rows)
        .with_columns(vs_fastest=pl.col("best_s") / pl.col("best_s").min())
        .sort("best_s")
    )
