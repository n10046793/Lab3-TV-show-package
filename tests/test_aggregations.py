"""Tests for the aggregation classes. No network: the records are hand-made."""

import unittest

from tvsummary.aggregations import AvgRatingByLanguage, ShowsPerGenre
from tvsummary.models import ShowRecord


def make_show(name, genres, language, rating, premiered):
    """Build one ShowRecord from plain values, like the API would give."""
    return ShowRecord(
        {
            "name": name,
            "genres": genres,
            "language": language,
            "rating": {"average": rating},
            "premiered": premiered,
        }
    )


class TestShowsPerGenre(unittest.TestCase):
    """Check the genre counts on three hand-made shows."""

    def test_counts_each_genre(self):
        records = [
            make_show("A", ["Drama"], "English", 8.0, "2010-01-01"),
            make_show("B", ["Drama", "Comedy"], "English", 7.0, "2012-01-01"),
            make_show("C", [], "English", 6.0, "2015-01-01"),
        ]
        result = ShowsPerGenre().compute(records)
        self.assertEqual(result, {"Drama": 2, "Comedy": 1})

    def test_average_rating_skips_missing_ratings(self):
        records = [
            make_show("A", ["Drama"], "English", 8.0, "2010-01-01"),
            make_show("B", ["Drama"], "English", 6.0, "2012-01-01"),
            make_show("C", ["Drama"], "English", None, "2015-01-01"),
        ]
        result = AvgRatingByLanguage().compute(records)
        self.assertEqual(result, {"English": 7.0})


if __name__ == "__main__":
    unittest.main()
