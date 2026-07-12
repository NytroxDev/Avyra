# Contributing to Avyra

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/NytroxDev/Avyra.git
cd Avyra
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Code Quality

```bash
ruff check avyra/ tests/
python -m mypy avyra/
```

## Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-change`)
3. Make your changes
4. Run tests and linter
5. Commit with a descriptive message
6. Open a pull request

## Commit Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation only
- `test:` adding or updating tests
- `refactor:` code change that neither fixes a bug nor adds a feature
- `chore:` maintenance tasks

## Code Style

- Follow existing patterns in the codebase
- All public methods must have docstrings
- Type annotations are required
- No external runtime dependencies
