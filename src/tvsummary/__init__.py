"""tvsummary: summarize TV show records from the TVMaze API."""

from tvsummary.config import API_URL, OUTPUT_PATH, REQUEST_TIMEOUT
from tvsummary.models import ShowRecord
from tvsummary.sources import TVMazeSource
from tvsummary.aggregations import (
    Aggregation,
    AvgRatingByLanguage,
    ShowsPerDecade,
    ShowsPerGenre,
)
from tvsummary.report import build_summary, write_summary

__all__ = [
    "API_URL",
    "OUTPUT_PATH",
    "REQUEST_TIMEOUT",
    "ShowRecord",
    "TVMazeSource",
    "Aggregation",
    "AvgRatingByLanguage",
    "ShowsPerDecade",
    "ShowsPerGenre",
    "build_summary",
    "write_summary",
]
