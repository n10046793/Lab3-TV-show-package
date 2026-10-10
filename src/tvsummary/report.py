"""Build the summary dictionary and write it to a JSON file."""

import json
from pathlib import Path

from tvsummary.aggregations import (
    AvgRatingByLanguage,
    ShowsPerDecade,
    ShowsPerGenre,
)
from tvsummary.config import API_URL


def most_common_genre(genre_counts):
    """Return the genre with the highest count."""
    top_genre = None
    top_count = 0
    for genre, count in genre_counts.items():
        if count > top_count:
            top_genre = genre
            top_count = count
    return top_genre


def build_summary(records):
    """Combine the aggregations into one dictionary ready to write.

    Each aggregation is asked for its answer through the same
    compute() method; the loop never checks which subclass it holds.
    """
    aggregations = [ShowsPerGenre(), AvgRatingByLanguage(), ShowsPerDecade()]

    results = {}
    for aggregation in aggregations:
        results[aggregation.name] = aggregation.compute(records)

    genre_counts = results["shows_per_genre"]

    return {
        "source_url": API_URL,
        "records_processed": len(records),
        "shows_per_genre": genre_counts,
        "distinct_genres": sorted(genre_counts),
        "most_common_genre": most_common_genre(genre_counts),
        "average_rating_by_language": results["average_rating_by_language"],
        "shows_per_decade": results["shows_per_decade"],
    }


def write_summary(summary, path):
    """Write the summary dictionary to a JSON file."""
    Path(path).write_text(json.dumps(summary, indent=2), encoding="utf-8")
