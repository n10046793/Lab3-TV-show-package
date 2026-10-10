"""Fetching records. This is the only module that uses requests."""

import requests

from tvsummary.config import API_URL, REQUEST_TIMEOUT
from tvsummary.models import ShowRecord


class TVMazeSource:
    """Downloads TV show records from the TVMaze API.

    Returns ShowRecord objects, not raw dictionaries.
    """
    def __init__(self):
        """Save the URL and timeout from the config module."""

        self.url = API_URL
        self.timeout = REQUEST_TIMEOUT


    def fetch(self):
        """Download the records and return them as ShowRecord objects.

        Returns None if the download fails, so the program can stop
        with a clear message instead of crashing.
        """
        try:
            response = requests.get(self.url, timeout=self.timeout)

            response.raise_for_status()
            return [ShowRecord(item) for item in response.json()]
        except requests.RequestException:
            print("Could not download the show records. Check your connection and try again.")
            return None