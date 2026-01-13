.PHONY: test install clean lint

# Default target
all: test

# Environment variable for binary path (default to local venv)
BIN ?= ./venv/bin/

# Install dependencies and the package in editable mode
install:
	$(BIN)pip install -e .[dev,docs] pytest ruff mypy build

# Run tests
test:
	$(BIN)pytest

# Simulate CI locally (Install + Lint + Test)
ci: install lint test

# Run linting
lint:
	$(BIN)ruff check .
	$(BIN)mypy whisper_vtt2srt --ignore-missing-imports

# Clean build artifacts
clean:
	rm -rf build dist *.egg-info .pytest_cache site
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Documentation
docs-serve:
	$(BIN)mkdocs serve --livereload

docs-build:
	$(BIN)mkdocs build

# Release
build:
	$(BIN)pip install build twine
	$(BIN)python -m build

publish-test: build
	$(BIN)twine upload --repository testpypi dist/*

publish: build
	$(BIN)twine upload dist/*
