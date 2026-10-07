
"""Lab 02: Aggregating Records.

Downloads TV show records from the TVMaze API, summarizes them
by genre, language rating and premiere decade, and writes the
summary to summary.json.
"""

import json
from pathlib import Path

import requests

URL = "https://api.tvmaze.com/shows?page=0"
OUTPUT = Path("summary.json")


def fetch_records(url):
    """Download the records from the API and return them as a list.

    Returns None if the download fails, so the program can stop
    with a clear message instead of crashing.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print("Could not download the show records. Check your connection and try again.")
        return None


def shows_per_genre(records):
    """Count how many shows belong to each genre.

    A show can list several genres, so it is counted once under each
    genre it lists. Shows with no genres are skipped.
    """
    counts = {}
    for show in records:
        for genre in show.get("genres", []):
            counts[genre] = counts.get(genre, 0) + 1
    return counts


def most_common_genre(genre_counts):
    """Return the genre with the highest count."""
    top_genre = None
    top_count = 0
    for genre, count in genre_counts.items():
        if count > top_count:
            top_genre = genre
            top_count = count
    return top_genre


def average_rating_by_language(records):
    """Work out the average rating for each language.

    Shows with no rating are skipped, so a missing rating is never
    treated as a zero.
    """
    totals = {}
    counts = {}
    for show in records:
        language = show.get("language")
        rating_info = show.get("rating", {})
        rating = rating_info.get("average")
        if language is None or rating is None:
            continue
        totals[language] = totals.get(language, 0) + rating
        counts[language] = counts.get(language, 0) + 1
    return {
        language: round(totals[language] / counts[language], 2)
        for language in totals
    }


def shows_per_decade(records):
    """Count how many shows premiered in each decade, e.g. '1990s'.

    Shows with a missing or strange-looking premiere date are skipped.
    """
    counts = {}
    for show in records:
        premiered = show.get("premiered")
        if not premiered:
            continue
        year = premiered[:4]
        if not year.isdigit():
            continue
        decade = year[:3] + "0s"
        counts[decade] = counts.get(decade, 0) + 1
    return counts


def build_summary(records):
    """Combine the aggregations into one dictionary ready to write."""
    genre_counts = shows_per_genre(records)

    genres = set()
    for show in records:
        for genre in show.get("genres", []):
            genres.add(genre)

    return {
        "source_url": URL,
        "records_processed": len(records),
        "shows_per_genre": genre_counts,
        "distinct_genres": sorted(genres),
        "most_common_genre": most_common_genre(genre_counts),
        "average_rating_by_language": average_rating_by_language(records),
        "shows_per_decade": shows_per_decade(records),
    }


def write_summary(summary, path):
    """Write the summary dictionary to a JSON file."""
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main():
    """Download the records, summarize them and write summary.json."""
    records = fetch_records(URL)
    if records is None:
        return
    summary = build_summary(records)
    write_summary(summary, OUTPUT)
    print(f"Processed {summary['records_processed']} TV show records.")
    print(f"Most common genre: {summary['most_common_genre']}.")
    print(f"Summary written to {OUTPUT}.")


if __name__ == "__main__":
    main()
