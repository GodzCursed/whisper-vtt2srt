.PHONY: test install clean lint

# Default target
all: test

# Install dependencies and the package in editable mode
install:
	./venv/bin/pip install -e .[dev,docs] pytest ruff mypy

# Run tests
test:
	./venv/bin/pytest

# Simulate CI locally (Install + Lint + Test)
ci: install lint test

# Run linting
lint:
	./venv/bin/ruff check .
	./venv/bin/mypy whisper_vtt2srt --ignore-missing-imports

# Clean build artifacts
clean:
	rm -rf build dist *.egg-info .pytest_cache site
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Documentation
docs-serve:
	./venv/bin/mkdocs serve

docs-build:
	./venv/bin/mkdocs build

# Release
build:
	./venv/bin/pip install build twine
	./venv/bin/python -m build

publish-test: build
	./venv/bin/twine upload --repository testpypi dist/*

publish: build
	./venv/bin/twine upload dist/*
