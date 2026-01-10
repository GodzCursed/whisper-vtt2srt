<p align="right">
  <a href="https://www.buymeacoffee.com/jorcelinojunior" target="_blank">
    <img
      src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png"
      alt="Buy Me A Coffee"
      width="120"
    />
  </a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/jorcelinojunior/whisper-vtt2srt/main/docs/img/icon.png" alt="whisper-vtt2srt Icon" width="128" />
</p>

<h1 align="center">whisper-vtt2srt</h1>

<p align="center"><strong>A robust, production-grade library designed to convert WebVTT to SRT, turning messy AI transcripts into clean, usable subtitles.</strong></p>

<p align="center">
  A post-processing tool designed to clean the output from <strong>OpenAI Whisper</strong>, <strong>YouTube Auto-Captions</strong>, and other AI transcription services.
  <br>
  Perfect for <strong>TTS pipelines</strong>, video dubbing, and dataset preparation.
</p>

<p align="center">
   <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a> <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+" /></a> <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: Black" /></a> <a href="CONTRIBUTING.md"><img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a> <a href="https://github.com/jorcelinojunior/whisper-vtt2srt/issues"><img alt="Issues" src="https://img.shields.io/github/issues/jorcelinojunior/whisper-vtt2srt" /></a> <a href="https://badge.fury.io/py/whisper-vtt2srt"><img src="https://badge.fury.io/py/whisper-vtt2srt.svg" alt="PyPI version" /></a>
</p>

---

## 🧠 The Problem with Raw AI Subtitles

AI tools like Whisper are incredible at speech recognition, but their raw VTT output is often chaotic. They frequently produce:

* **The "Karaoke Effect":** Words accumulating screen-by-screen (e.g., "Hello", "Hello world", "Hello world!").
* **Micro-Glitches:** Subtitle frames lasting milliseconds that are invisible to humans but break TTS/dubbing scripts.
* **Metadata Clutter:** Tags like `align:start`, `<c>`, `<b>` or `<i>` that mess up text processing.

**whisper-vtt2srt** is the bridge between raw AI output and your production pipeline.
It stabilizes and normalizes the text, making it safe for **Text-to-Speech (TTS) generation**, video players, and NLP tasks.

---

## 📖 Table of Contents

* [👀 See the Difference](#-see-the-difference-before-vs-after)
* [🚀 Key Features](#-key-features)
* [📦 Installation](#-installation)
* [📘 How to Use](#-how-to-use)
  * [💻 CLI Usage](#-cli-usage)
    * [Command Help](#command-help)
  * [🐍 Python API Usage](#-python-api-usage)
    * [Basic Conversion](#basic-conversion)
    * [Advanced Control](#advanced-control)
* [🧠 How It Works](#-how-it-works)
* [📆 Changelog](#-changelog)
* [🤝 Contributing](#-contributing)
* [📜 License](#-license)
* [📚 Reference](#-reference)

---

## 👀 See the Difference (Before vs After)

<details open>
<summary>🚧 <strong>Raw Input</strong>&nbsp;— <em>(Typical output from YouTube/Whisper - with "Karaoke Effect")</em></summary>

> *Notice the accumulated text, repetitive lines, and internal tagging.*

```vtt
WEBVTT
Kind: captions
Language: en

00:00:03.110 --> 00:00:05.430 align:start position:0%
APIs are everywhere. They power your
apps,<00:00:03.600><c> your</c><00:00:03.840><c> payment</c><00:00:04.160><c> systems,</c><00:00:04.880><c> your</c><00:00:05.120><c> cloud</c>

00:00:05.430 --> 00:00:05.440 align:start position:0%
apps, your payment systems, your cloud
 

00:00:05.440 --> 00:00:07.829 align:start position:0%

apps, your payment systems, your cloud
services,<00:00:06.560><c> pretty</c><00:00:06.879><c> much</c><00:00:07.120><c> every</c><00:00:07.440><c> piece</c><00:00:07.680><c> of</c>

00:00:07.829 --> 00:00:07.839 align:start position:0%
services, pretty much every piece of
```

</details>

<details open>
<summary>✨<strong> Cleaned Output </strong>&nbsp;— <em>(Processed by whisper-vtt2srt)</em></summary>

> *Clean, stable, and ready for TTS input, YouTube, Netflix or standard players.*

```srt
1
00:00:03,110 --> 00:00:05,430
APIs are everywhere. They power your apps, your payment systems, your cloud

2
00:00:05,440 --> 00:00:07,829
services, pretty much every piece of
```

</details>

---

## 🚀 Key Features

* **🛡️ Stabilization Strategy**
   Intelligently detects and merges accumulating text blocks ("Karaoke Effect"), preventing the rapid flashing of partial sentences. Essential for generating smooth audio in TTS pipelines, video dubbing, and subtitles.

* **🎵 Sound Description Removal**
   Automatically filters out non-speech elements like `[Music]`, `[Applause]`, or `[Laughter]`, ensuring your TTS voice doesn't try to read stage directions.

* **🧹 Glitch Filtering**
   Automatically removes subtitle blocks with insignificant duration (< 50ms) that can cause audio generation errors or player flickering.

* **✨ Smart Normalization**
   Strips VTT-specific metadata (`align:start`, `position:0%`), removes internal tags (`<c>`, `<00:00:00>`), and **cleans up inconsistent whitespace** ensuring pure text output.

* **⚡ Zero Dependencies**
   Built with pure Python standard library. Lightweight and easy to install in any environment (Linux, Windows, Docker).

* **🔧 Configurable Strictness**
   Every cleaning step is optional. You enable exactly what your pipeline needs.

## 📦 Installation

```bash
pip install whisper-vtt2srt
```

## 📘 How to Use

### 💻 CLI Usage

Process files directly from the command line:

```bash
# Convert a Single File
whisper-vtt2srt input.vtt

# Batch Convert a Folder
whisper-vtt2srt ./my_dataset

# Recursive Conversion (subfolders included)
whisper-vtt2srt ./my_dataset --recursive

# Handle Legacy Encodings (e.g., Latin-1)
whisper-vtt2srt input_latin.vtt --encoding ISO-8859-1

# Keep the "karaoke" effect (disable deduplication)
whisper-vtt2srt input.vtt --no-karaoke
```

#### Command Help

```text
usage: whisper-vtt2srt [-h] [-r] [-e ENCODING] [--no-karaoke] [--keep-glitches] [--keep-formatting]
               [--keep-metadata] [--merge-short-lines]
               input [output]

Convert WebVTT to SRT with professional cleaning.

positional arguments:
  input                 Input VTT file or directory
  output                Output SRT file or directory (optional)

options:
  -h, --help            show this help message and exit
  -r, --recursive       Recursively process directories
  -e ENCODING, --encoding ENCODING
                        Input file encoding (default: utf-8)
  --no-karaoke          Disable anti-karaoke filter (keep accumulating text)
  --keep-sound-descriptions
                        Keep sound descriptions like [Music] or [Applause]
  --keep-glitches       Keep short <50ms blocks
  --keep-formatting     Keep VTT tags (bold, italic, colors)
  --keep-metadata       Keep metadata tags (align:start, position:0%)
  --merge-short-lines   Aggressively merge short lines into single lines
  --max-line-length MAX_LINE_LENGTH
                        Maximum line length allowed when merging short lines (default: 42, like YouTube/Netflix)
```

### 🐍 Python API Usage

Easily integrate `whisper-vtt2srt` into your own Python pipelines.
The library exports a high-level `Pipeline` class for full control.

#### Basic Conversion

```python
from whisper_vtt2srt import Pipeline

# 1. Initialize
pipeline = Pipeline()

# 2. Read input
with open("subs.vtt", "r", encoding="utf-8") as f:
    raw_vtt_content = f.read()

# 3. Convert raw VTT content
srt_content = pipeline.convert(raw_vtt_content)

# 4. Use the clean SRT (e.g., send to TTS engine, save to file, render in player, etc.)
print(srt_content)
```

#### Advanced Control

You can customize the cleaning options if needed:

> Just pass a `CleaningOptions` object to the `Pipeline` constructor to toggle specific cleaning rules.

```python
from whisper_vtt2srt import CleaningOptions, Pipeline

# Configure strictness
options = CleaningOptions(
    remove_pixelation=True,    # Fix Karaoke effect
    remove_sound_descriptions=True, # Remove [Music], [Applause]
    remove_glitches=True,      # Remove <50ms blocks
    simplify_formatting=True,  # Strip tags like <c> or <b> and fix whitespace
    remove_metadata=True,      # Clean VTT positioning
    merge_short_lines=False,   # Aggressively merge short lines
    max_line_length=42         # Max length constraint for merging
)

pipeline = Pipeline(options)
```

## 🧠 How It Works

1. **Parser (State Machine)**: Robustly reads messy VTT files, handling multi-line strings and irregular spacing.
2. **Deduplication Engine**: Uses a sliding window to identify comparison patterns between blocks. If a block is just a prefix of the next one (common in AI streams), it is merged or removed to stabilize the text.
3. **Filter Layer**: Applies duration checks and regex cleaning to ensure the final output is compliant with the SubRip (SRT) standard.

## 📆 Changelog

Project history and updates are tracked in [`CHANGELOG.md`](./CHANGELOG.md).

## 🤝 Contributing

Contributions are welcome! We follow a strict SOLID architecture. See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for details.

## 📜 License

MIT License - see [`LICENSE`](LICENSE).

## 📚 Reference

If you use this library in your research or project, please cite it as:

```bibtex
@software{whisper_vtt2srt,
  author = {Jorcelino Junior},
  title = {whisper-vtt2srt: A robust WebVTT to SRT converter for AI subtitles},
  year = {2026},
  url = {https://github.com/jorcelinojunior/whisper-vtt2srt}
}
```

---

<div align="center">
  <p><strong>Saved you time? Helped your project?</strong></p>
  <p>Support independent open-source development!</p>
  <a href="https://www.buymeacoffee.com/jorcelinojunior">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="180">
  </a>
</div>
