default: check

fmt:
    uv run ruff format .
    uv run ruff check . --fix

lint:
    uv run ruff check .
    uv run ruff format --check .

test:
    uv run pytest -q

check: lint test