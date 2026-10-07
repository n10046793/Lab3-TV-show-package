# tvsummary

Downloads TV show records from the TVMaze API and summarizes them by
genre, language rating and premiere decade. This is the Lab 02 program
refactored into an installable package: same data in, same summary out.

## Data source

https://api.tvmaze.com/shows?page=0 — one record is one TV show.
About 240 shows per run.

## Setup

```
conda env create -f environment.yml
conda activate tvsummary
pip install -r requirements.txt
pip install -e .
```

## Run

```
python main.py
```

## Test

```
python -m unittest discover -s tests
```

## Layout

- `config.py` — the API URL, timeout and output path, all in one place.
- `models.py` — the `ShowRecord` class; cleans each show's values when created.
- `sources.py` — the `TVMazeSource` class; the only module that uses `requests`.
- `aggregations.py` — the `Aggregation` base class and its three subclasses.
- `report.py` — builds the summary dictionary and writes `summary.json`.
- `main.py` — thin entry point; only wires the pieces together.

## What moved where

| Lab 02 (`records.py`)              | Lab 03 (class and method, or module)        |
|------------------------------------|---------------------------------------------|
| `URL`, `OUTPUT` constants          | `config.py`: `API_URL`, `REQUEST_TIMEOUT`, `OUTPUT_PATH` |
| `fetch_records()`                  | `sources.py`: `TVMazeSource.fetch()`        |
| `shows_per_genre()`                | `aggregations.py`: `ShowsPerGenre.compute()` |
| `most_common_genre()`              | `report.py`: `most_common_genre()`          |
| `average_rating_by_language()`     | `aggregations.py`: `AvgRatingByLanguage.compute()` |
| `shows_per_decade()`               | `aggregations.py`: `ShowsPerDecade.compute()` |
| `build_summary()`                  | `report.py`: `build_summary()`              |
| `write_summary()`                  | `report.py`: `write_summary()`              |
| `main()`                           | `main.py`: `main()` (now only wiring)       |
| missing-value checks in each function | `models.py`: `ShowRecord.__init__`       |

## Design choices

- `ShowRecord` exists so missing or malformed values are cleaned in exactly
  one place — its `__init__` method — instead of being re-checked in every
  function.
- `Aggregation` is a base class with a `compute()` method; each subclass
  answers one question about the records. `build_summary()` loops over a
  list of `Aggregation` objects and calls `compute()` on each without
  checking which subclass it holds. Adding a fourth aggregation means
  writing one more subclass and adding it to the list — nothing else changes.
- `TVMazeSource.fetch()` returns `ShowRecord` objects, not raw dictionaries,
  so the aggregations never touch the API's raw format.
- Only `sources.py` imports `requests`, so switching to a different data
  source would only touch that one module.

## Known limitations

- The summary depends on live TVMaze data, so ratings can change between runs.
- The program prints messages instead of logging (Lab 04 adds logging).
