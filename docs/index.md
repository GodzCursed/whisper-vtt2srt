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

## Why whisper-vtt2srt?

Unlike simple regex-based converters, this tool allows for **intelligent cleaning strategies** specifically engineered to handle the chaotic output of modern AI transcription services like **OpenAI Whisper**.

### Key Features 🚀

* **🛡️ Stabilization Strategy**: Intelligently detects and merges accumulating text blocks ("Karaoke Effect").
* **🎵 Sound Description Removal**: Automatically filters out `[Music]`, `[Applause]`, etc.
* **🧹 Glitch Filtering**: Removes imperceptible <50ms blocks.
* **✨ Smart Normalization**: Strips VTT metadata (`align:start`, `<c>`, `<b>`, `<i>`) and cleans whitespace.
* **⚡ Zero Dependencies**: Built with pure Python standard library.
* **🔧 Configurable Strictness**: Every cleaning step is optional.

## Installation

```bash
pip install whisper-vtt2srt
```

## Quick Start

### CLI

```bash
# Convert a single file
whisper-vtt2srt video.vtt

# Convert a folder recursively
whisper-vtt2srt ./videos --recursive
```

### Python

```python
from whisper_vtt2srt import Pipeline

pipeline = Pipeline()

with open("video.vtt", "r", encoding="utf-8") as f:
    srt_content = pipeline.convert(f.read())

```
