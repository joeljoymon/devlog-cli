import json
import os
import pytest
from click.testing import CliRunner
from devlog.cli import cli
from datetime import datetime

# ── Setup ────────────────────────────────────────────────────
# CliRunner lets us call CLI commands in tests without a real terminal
runner = CliRunner()

@pytest.fixture(autouse=True)
def temp_data_file(tmp_path, monkeypatch):
    """
    Before each test: point DATA_FILE to a temp file so tests
    never touch your real ~/.devlog.json data.
    """
    import devlog.cli as cli_module
    temp_file = str(tmp_path / "test_devlog.json")
    monkeypatch.setattr(cli_module, "DATA_FILE", temp_file)
    return temp_file


# ── Tests for: log command ───────────────────────────────────
class TestLogCommand:

    def test_log_creates_entry(self):
        """Running log should save one entry to the file."""
        result = runner.invoke(cli, ["log", "Fix the login bug"])

        assert result.exit_code == 0
        assert "Logged #1" in result.output

    def test_log_multiple_entries(self):
        """Each log call should increment the ID."""
        runner.invoke(cli, ["log", "First task"])
        result = runner.invoke(cli, ["log", "Second task"])

        assert "Logged #2" in result.output

    def test_log_empty_message_fails(self):
        """Log command should fail if no message is given."""
        result = runner.invoke(cli, ["log"])

        assert result.exit_code != 0


# ── Tests for: list command ──────────────────────────────────
class TestListCommand:

    def test_list_empty(self):
        """List should tell the user when there are no entries."""
        result = runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "No entries yet" in result.output

    def test_list_shows_entries(self):
        """List should display logged entries."""
        runner.invoke(cli, ["log", "Build the API"])
        result = runner.invoke(cli, ["list"])

        assert "Build the API" in result.output

    def test_list_shows_pending_icon(self):
        runner.invoke(cli, ["log", "Pending task"])
        result = runner.invoke(cli, ["list"])
        assert "Pending task" in result.output
        assert "o #1" in result.output


# ── Tests for: done command ──────────────────────────────────
class TestDoneCommand:

    def test_done_marks_entry(self):
        """Done command should mark the right entry as complete."""
        runner.invoke(cli, ["log", "Deploy to production"])
        result = runner.invoke(cli, ["done", "1"])

        assert result.exit_code == 0
        assert "✔ Marked #1 as done: Deploy to production" in result.output

    def test_done_reflects_in_list(self):
        """After marking done, list should show ✔ icon."""
        runner.invoke(cli, ["log", "Write tests"])
        runner.invoke(cli, ["done", "1"])
        result = runner.invoke(cli, ["list"])

        assert "✔" in result.output

    def test_done_invalid_id(self):
        """Done with a non-existent ID should show an error message."""
        result = runner.invoke(cli, ["done", "999"])

        assert "No entry found" in result.output

    def test_done_requires_integer(self):
        """Done should fail if a non-integer ID is passed."""
        result = runner.invoke(cli, ["done", "abc"])

        assert result.exit_code != 0


# ── Tests for: summary command ───────────────────────────────
class TestSummaryCommand:

    def test_summary_empty(self):
        """Summary should handle no entries gracefully."""
        result = runner.invoke(cli, ["summary"])

        assert result.exit_code == 0
        assert "No entries found" in result.output

    def test_summary_shows_totals(self):
        """Summary should show correct total count."""
        runner.invoke(cli, ["log", "Task one"])
        runner.invoke(cli, ["log", "Task two"])
        result = runner.invoke(cli, ["summary"])

        assert "Total logged : 2" in result.output

    def test_summary_completed_count(self):
        """Summary should correctly count completed tasks."""
        runner.invoke(cli, ["log", "Task one"])
        runner.invoke(cli, ["log", "Task two"])
        runner.invoke(cli, ["done", "1"])
        result = runner.invoke(cli, ["summary"])

        assert "Completed    : 1" in result.output

    def test_summary_custom_date(self):
        """Summary with a past date that has no entries."""
        result = runner.invoke(cli, ["summary", "--date", "01-01-2000"])

        assert "No entries found in 01-01-2000" in result.output

# ── Stronger negative tests ──────────────────────────────────
class TestNegativeCases:

    def test_done_on_empty_log(self):
        """Done should fail gracefully when no entries exist at all."""
        result = runner.invoke(cli, ["done", "1"])

        assert result.exit_code == 0          # it shouldn't crash
        assert "No entry found" in result.output  # but it should warn

    def test_log_does_not_mark_as_done(self):
        """A freshly logged entry must never start as done."""
        runner.invoke(cli, ["log", "New task"])
        result = runner.invoke(cli, ["list"])

        assert "✔" not in result.output   # ← asserting something is ABSENT

    def test_done_wrong_id_doesnt_corrupt_data(self):
        runner.invoke(cli, ["log", "Real task"])
        runner.invoke(cli, ["done", "999"])
        result = runner.invoke(cli, ["list"])
        assert "Real task" in result.output   # entry still exists
        assert "o #1" in result.output        # still has its ID


    def test_summary_does_not_show_other_dates(self):
        """Summary for one date should never leak entries from another date."""
        runner.invoke(cli, ["log", "Task from today"])
        result = runner.invoke(cli, ["summary", "--date", "01-01-2000"])

        assert "Task from today" not in result.output  # ← must be absent