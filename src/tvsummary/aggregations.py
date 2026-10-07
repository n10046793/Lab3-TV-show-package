"""The aggregations: a base class with one subclass per question."""


class Aggregation:
    """Base class for the aggregations.

    Each subclass answers one question about the records by overriding
    compute(). The summary builder calls compute() on each one without
    checking which subclass it is.
    """

    name = "aggregation"

    def compute(self, records):
        """Work out this aggregation's answer from the records."""
        raise NotImplementedError


class ShowsPerGenre(Aggregation):
    """Count how many shows belong to each genre.

    A show can list several genres, so it is counted once under each
    genre it lists. Shows with no genres are skipped.
    """

    name = "shows_per_genre"

    def compute(self, records):
        counts = {}
        for record in records:
            for genre in record.genres:
                counts[genre] = counts.get(genre, 0) + 1
        return counts


class AvgRatingByLanguage(Aggregation):
    """Work out the average rating for each language.

    Shows with no rating are skipped, so a missing rating is never
    treated as a zero.
    """

    name = "average_rating_by_language"

    def compute(self, records):
        totals = {}
        counts = {}
        for record in records:
            if record.language is None or record.rating is None:
                continue
            totals[record.language] = totals.get(record.language, 0) + record.rating
            counts[record.language] = counts.get(record.language, 0) + 1
        return {
            language: round(totals[language] / counts[language], 2)
            for language in totals
        }


class ShowsPerDecade(Aggregation):
    """Count how many shows premiered in each decade, e.g. '1990s'.

    Shows with a missing or strange-looking premiere date are skipped.
    """

    name = "shows_per_decade"

    def compute(self, records):
        counts = {}
        for record in records:
            if not record.premiered:
                continue
            year = record.premiered[:4]
            if not year.isdigit():
                continue
            decade = year[:3] + "0s"
            counts[decade] = counts.get(decade, 0) + 1
        return counts
