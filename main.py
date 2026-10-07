"""Thin entry point: wire the package pieces together."""

from tvsummary import OUTPUT_PATH, TVMazeSource, build_summary, write_summary


def main():
    """Download the records, summarize them and write the summary file."""
    records = TVMazeSource().fetch()
    if records is None:
        return
    summary = build_summary(records)
    write_summary(summary, OUTPUT_PATH)
    print(f"Processed {summary['records_processed']} TV show records.")
    print(f"Most common genre: {summary['most_common_genre']}.")
    print(f"Summary written to {OUTPUT_PATH}.")


if __name__ == "__main__":
    main()
