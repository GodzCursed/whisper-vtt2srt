#!/usr/bin/env python3
"""Basic usage example for the whisper-vtt2srt library.

This script demonstrates how to use the Pipeline API to convert VTT content
to SRT format. It is also used as a debug target in VS Code.

Usage:
    python examples/basic_usage.py
"""

from pathlib import Path

from whisper_vtt2srt import CleaningOptions, Pipeline


def main():
    # Sample VTT content (Whisper karaoke-style output)
    vtt_content = """WEBVTT
Kind: captions
Language: en

00:00:00.500 --> 00:00:02.500 align:start position:0%

Hello<00:00:01.000><c> world.</c>

00:00:02.500 --> 00:00:02.510 align:start position:0%
Hello world.


00:00:02.510 --> 00:00:05.000 align:start position:0%
Hello world.
This<00:00:03.000><c> is</c><00:00:03.500><c> a</c><00:00:04.000><c> test.</c>
"""

    # Option 1: Default options (all cleaning enabled)
    pipeline = Pipeline()
    srt_output = pipeline.convert(vtt_content)

    print("=" * 60)
    print("OUTPUT (Default Options)")
    print("=" * 60)
    print(srt_output)

    # Option 2: Custom options
    custom_options = CleaningOptions(
        remove_pixelation=True,         # Remove karaoke duplicates
        remove_glitches=True,           # Remove <50ms blocks
        simplify_formatting=True,       # Strip VTT tags
        remove_metadata=True,           # Remove align:start, etc.
        remove_sound_descriptions=True, # Remove [Music], etc.
        merge_short_lines=False,        # Keep lines separate
    )
    pipeline_custom = Pipeline(custom_options)
    srt_custom = pipeline_custom.convert(vtt_content)

    print("=" * 60)
    print("OUTPUT (Custom Options)")
    print("=" * 60)
    print(srt_custom)

    # Option 3: Convert from file
    fixture_path = Path(__file__).parent.parent / "tests" / "fixtures" / "sample.vtt"
    if fixture_path.exists():
        with open(fixture_path, encoding="utf-8") as f:
            file_content = f.read()

        srt_from_file = pipeline.convert(file_content)

        print("=" * 60)
        print(f"OUTPUT (From File: {fixture_path.name})")
        print("=" * 60)
        print(srt_from_file)


if __name__ == "__main__":
    main()
