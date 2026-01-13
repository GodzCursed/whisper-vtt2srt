# ruff: noqa: E501

from whisper_vtt2srt.domain.options import CleaningOptions
from whisper_vtt2srt.use_cases.pipeline import Pipeline


def test_pipeline_produces_clean_output_without_timestamp_overlap():
    """Tests that the pipeline produces clean output with preserved timestamps.

    This test validates the core goal: duplicates are removed, timestamps are
    preserved exactly as in the source, and no timestamp overlap occurs.
    """
    vtt_content = """WEBVTT
Kind: captions
Language: en

00:00:00.640 --> 00:00:03.110 align:start position:0%

APIs<00:00:01.280><c> are</c><00:00:01.520><c> everywhere.</c><00:00:02.399><c> They</c><00:00:02.639><c> power</c><00:00:02.960><c> your</c>

00:00:03.110 --> 00:00:03.120 align:start position:0%
APIs are everywhere. They power your


00:00:03.120 --> 00:00:05.430 align:start position:0%
APIs are everywhere. They power your
apps,<00:00:03.600><c> your</c><00:00:03.840><c> payment</c><00:00:04.160><c> systems,</c><00:00:04.880><c> your</c><00:00:05.120><c> cloud</c>

00:00:05.430 --> 00:00:05.440 align:start position:0%
apps, your payment systems, your cloud


00:00:05.440 --> 00:00:07.829 align:start position:0%
apps, your payment systems, your cloud
services,<00:00:06.560><c> pretty</c><00:00:06.879><c> much</c><00:00:07.120><c> every</c><00:00:07.440><c> piece</c><00:00:07.680><c> of</c>
"""

    options = CleaningOptions(
        remove_pixelation=True,
        remove_glitches=True,
        simplify_formatting=True,
        remove_metadata=True
    )
    pipeline = Pipeline(options)
    srt_output = pipeline.convert(vtt_content)

    print("\nGenerated SRT:\n")
    print(srt_output)

    # Parse output blocks
    blocks = srt_output.strip().split("\n\n")

    # After glitch removal and deduplication, we expect exactly 3 blocks:
    # Block 1: APIs are everywhere. They power your (00:00:00,640 --> 00:00:03,110)
    # Block 2: apps, your payment systems, your cloud (00:00:03,120 --> 00:00:05,430)
    # Block 3: services, pretty much every piece of (00:00:05,440 --> 00:00:07,829)
    assert len(blocks) == 3, f"Expected 3 blocks, got {len(blocks)} blocks"

    # Verify timestamps are preserved exactly (no overlap/extension)
    assert "00:00:00,640 --> 00:00:03,110" in blocks[0]
    assert "00:00:03,120 --> 00:00:05,430" in blocks[1]
    assert "00:00:05,440 --> 00:00:07,829" in blocks[2]


def test_sound_description_removal():
    vtt_content = """WEBVTT

    00:00:01.000 --> 00:00:02.000
    [Music]

    00:00:02.000 --> 00:00:04.000
    Hello world.

    00:00:04.000 --> 00:00:05.000
    (Applause)
    """

    # 1. Default limits (Top quality = remove sound)
    pipeline = Pipeline()
    output = pipeline.convert(vtt_content)

    assert "[Music]" not in output
    assert "Hello world" in output
    # Note: Currently we only target square brackets [] per plan,
    # so (Applause) might remain unless we expanded regex.
    # Let's check my implementation: `r'\[[^\]]+\]'`
    # So (Applause) should REMAIN.
    assert "(Applause)" in output

    # 2. Disable removal
    options = CleaningOptions(remove_sound_descriptions=False)
    pipeline_keep = Pipeline(options)
    output_keep = pipeline_keep.convert(vtt_content)

    assert "[Music]" in output_keep
