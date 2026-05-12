# DevLog CLI

> A command-line developer journal and task tracker built with Python.

[![Run Tests](https://github.com/joeljoymon/devlog-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/joeljoymon/devlog-cli/actions/workflows/tests.yml)

DevLog is a lightweight CLI tool that helps developers track what
they worked on, mark tasks complete, and generate a daily summary
— all from the terminal without leaving your workflow.

---

## Installation

```bash
pip install devlog-cli-joel
```

---

## Quick Start

```bash
# Log what you're working on
devlog log "Fix authentication bug"
devlog log "Write unit tests for login"
devlog log "Review pull request #42"

# See everything on your list
devlog list

# Mark a task as done
devlog done 1

# See today's summary with progress
devlog summary
```

---

## Commands

| Command | Description | Example |
|---|---|---|
| `devlog log <message>` | Add a new task or note | `devlog log "Fix navbar bug"` |
| `devlog list` | Show all logged tasks | `devlog list` |
| `devlog done <id>` | Mark a task as complete | `devlog done 2` |
| `devlog summary` | Daily digest with progress | `devlog summary` |
| `devlog summary --date` | Summary for a specific date | `devlog summary --date 2024-01-15` |

---

## Example Output
---

## Development

```bash
# Clone the repo
git clone https://github.com/joeljoymon/devlog-cli.git
cd devlog-cli

# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# Install in editable mode
pip install -e .

# Run tests
pytest tests/ -v
```

---

## Project Structure
---
```
devlog-cli/
├── devlog/
│   ├── __init__.py
│   └── cli.py          # all CLI commands live here
├── tests/
|   ├── __init__.py
│   └── test_cli.py     # 18 tests covering all commands
├── .github/
│   └── workflows/
│       └── tests.yml   # CI pipeline runs on every push
├── pyproject.toml      # package configuration
└── README.md
```

## Tech Stack

- **Python 3.10** — core language
- **Click** — CLI framework for command routing and argument parsing
- **JSON** — lightweight data persistence
- **pytest** — testing framework with 18 test cases
- **GitHub Actions** — CI pipeline auto-runs tests on every push
- **PyPI** — package distribution

---

## What I Learned Building This

- Structuring a Python project as an installable package
- Writing a CLI using Click decorators and argument parsing
- Persisting data with JSON file I/O
- Writing positive and negative test cases with pytest
- Using monkeypatching and fixtures for test isolation
- Setting up a CI/CD pipeline with GitHub Actions
- Publishing a package to PyPI with twine

---

## License

MIT — see [LICENSE](LICENSE) for details.