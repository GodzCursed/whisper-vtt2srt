# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Sound Description Removal**: Automatically filter out elements like `[Music]` or `[Applause]` for cleaner output.
- **Stream Consolidation**: Improved `KaraokeDeduplicator` to intelligently merge prefix-based accumulating captions (Anti-Karaoke).
- **CLI**: Added `--keep-sound-descriptions` to preserve non-speech descriptions if needed.
- **Flat API**: Simplified import structure. Now you can import `Pipeline`, `CleaningOptions`, and `BatchConverter` directly from `whisper_vtt2srt`.
- **Documentation**: Added "Before vs After" comparison in README to visually demonstrate cleaning capabilities.
- **Documentation**: Added `CHANGELOG.md` to track project history.
- **Feature**: Added `ShortLineMerger` filter to merge short lines within a block.
- **Config**: Added `max_line_length` option (default: 42) to control line merging.
- **CLI**: Added `--merge-short-lines` and `--max-line-length` flags.

## [0.1.0] - 2026-01-09

### Added

- **Core Conversion Logic**: Implemented robust `VttParser` and `SrtWriter` based on SOLID principles.
- **Cleaning Filters**:
  - `KaraokeDeduplicator`: Intelligent sliding window algorithm to remove "karaoke effect" (accumulating text) from AI subtitles.
  - `GlitchFilter`: Automatically removes subtitle blocks shorter than 50ms.
  - `ContentNormalizer`: Strips VTT metadata (`align:start`, `position:0%`) and internal tags (`<c>`, `<b>`).
- **Batch Processing**: Added `BatchConverter` for processing entire directories recursively.
- **CLI**: Created `whisper-vtt2srt` command-line tool with support for:
  - Recursive directory scanning (`-r/--recursive`).
  - Custom input encodings (`-e/--encoding`).
  - Flags to disable specific cleaning filters (`--no-karaoke`, `--keep-glitches`, etc.).
- **Documentation Site**: Deployed full MkDocs Material documentation site.
- **Testing**: Comprehensive test suite using `pytest` covering Parsers, Filters, Models, and I/O.
- **CI/CD**: GitHub Actions workflow for automated testing, linting (`ruff`), and type checking (`mypy`).

### Changed

- **Rebranding**: Renamed project from `vtt2srt_pro` to `whisper-vtt2srt` to better reflect its primary use case.
- **Architecture**: Refactored to a simplified "Flat Layout" structure for better packaging.

### Fixed

- **Type Safety**: Resolved `mypy` strict type errors across the codebase.
- **Parsing**: Fixed handling of multi-line subtitles and irregular VTT timestamps.
