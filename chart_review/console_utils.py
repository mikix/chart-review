"""Helper methods for printing to the console."""

import rich

from chart_review import cohort, types


def pretty_note_range(notes: types.NoteSet) -> str:
    """
    Returns a pretty, human-readable string for a set of notes.

    If no notes, this returns an empty string.

    Example:
        pretty_note_range({1, 2, 3, 7, 9, 10})
        -> "1–3, 7, 9–10"
    """
    ranges = []
    range_start = None
    prev_note = None

    def end_range() -> None:
        if prev_note is None:
            return
        if range_start == prev_note:
            ranges.append(str(prev_note))
        else:
            ranges.append(f"{range_start}–{prev_note}")  # en dash

    for note in sorted(notes):
        if prev_note is None or prev_note + 1 != note:
            end_range()
            range_start = note
        prev_note = note

    end_range()

    return ", ".join(ranges)


def print_ignored_charts(reader: cohort.CohortReader):
    """Prints a line about ignored charts, suitable for underlying a table"""
    if not reader.ignored_notes:
        return

    ignored_count = len(reader.ignored_notes)
    chart_word = "chart" if ignored_count == 1 else "charts"
    pretty_ranges = pretty_note_range(reader.ignored_notes)
    rich.get_console().print(
        f"  Ignoring {ignored_count} {chart_word} ({pretty_ranges})",
        highlight=False,
        style="italic",
    )
