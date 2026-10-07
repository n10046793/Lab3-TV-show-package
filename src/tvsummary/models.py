"""The record class: one clean TV show."""


class ShowRecord:
    """One TV show, with its values cleaned when it is created.

    Missing or strange values are fixed here in __init__, so the rest
    of the program can trust what it gets from a record.
    """

    def __init__(self, data):
        """Pull the fields we need out of one raw API dictionary."""
        self.name = data.get("name") or "Unknown"
        genres = data.get("genres")
        self.genres = genres if isinstance(genres, list) else []
        self.language = data.get("language")
        rating_info = data.get("rating") or {}
        rating = rating_info.get("average")
        self.rating = rating if isinstance(rating, (int, float)) else None
        premiered = data.get("premiered")
        self.premiered = premiered if isinstance(premiered, str) else None

    def __str__(self):
        """A one-line description of the show."""
        return f"{self.name} ({self.language}) - rating {self.rating}"
