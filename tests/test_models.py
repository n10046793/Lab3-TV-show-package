"""Tests for the ShowRecord class. No network: the records are hand-made."""

import unittest

from tvsummary.models import ShowRecord


class TestShowRecord(unittest.TestCase):
    """Check that a record cleans its own values when it is created."""

    def test_missing_values_are_cleaned(self):
        record = ShowRecord({"name": "Mystery Show"})
        self.assertEqual(record.genres, [])
        self.assertIsNone(record.language)
        self.assertIsNone(record.rating)
        self.assertIsNone(record.premiered)

    def test_str_shows_name_language_and_rating(self):
        record = ShowRecord(
            {
                "name": "Example Show",
                "language": "English",
                "rating": {"average": 8.5},
                "genres": ["Drama"],
                "premiered": "2010-04-05",
            }
        )
        self.assertEqual(str(record), "Example Show (English) - rating 8.5")


if __name__ == "__main__":
    unittest.main()
