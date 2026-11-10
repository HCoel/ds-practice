"""Thin client for PostHog's HogQL query endpoint."""

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()  # finds .env by walking up from this file

HOST = os.getenv(
    "POSTHOG_HOST", "https://us.posthog.com"
)  # private API host, not us.i.
PROJECT_ID = os.getenv("POSTHOG_PROJECT_ID", "160198")


def run_hogql(query: str, name: str = "ds-practice") -> dict:
    """POST a HogQL query and return the parsed JSON response."""
    key = os.environ["POSTHOG_PERSONAL_API_KEY"]
    resp = requests.post(
        f"{HOST}/api/projects/{PROJECT_ID}/query/",
        headers={"Authorization": f"Bearer {key}"},
        json={"query": {"kind": "HogQLQuery", "query": query}, "name": name},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def read_sql(path: str | Path) -> str:
    return Path(path).read_text()
