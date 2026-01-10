import pytest

from whisper_vtt2srt.domain.models import SubtitleBlock, TimeCode
from whisper_vtt2srt.domain.options import CleaningOptions
from whisper_vtt2srt.use_cases.filters import ContentNormalizer, GlitchFilter, KaraokeDeduplicator


@pytest.fixture
def make_block():
    def _make(index, start_ms, end_ms, text):
        return SubtitleBlock(
            index=index,
            start=TimeCode(start_ms),
            end=TimeCode(end_ms),
            lines=text.split("\n") if text else []
        )
    return _make

class TestKaraokeDeduplicator:
    def test_basic_deduplication(self, make_block):
        # Before:
        # 1. "Hello"
        # 2. "Hello world"
        # 3. "Hello world!"

        blocks = [
            make_block(1, 0, 1000, "Hello"),
            make_block(2, 1000, 2000, "Hello world"),
            make_block(3, 2000, 3000, "Hello world!")
        ]

        options = CleaningOptions(remove_pixelation=True)
        cleaned = KaraokeDeduplicator().apply(blocks, options)

        # Expectation:
        # Instead of fragments (Hello, world, !), we want the final stable line
        # to subsume the prefixes and cover the entire time range (0 -> 3000).

        assert len(cleaned) == 1
        assert cleaned[0].lines == ["Hello world!"]
        assert cleaned[0].start.milliseconds == 0
        assert cleaned[0].end.milliseconds == 3000

class TestGlitchFilter:
    def test_removes_short_blocks(self, make_block):
        blocks = [
            make_block(1, 0, 1000, "Valid"),
            make_block(2, 1000, 1020, "Glitch"), # 20ms < 50ms
            make_block(3, 2000, 3000, "Valid")
        ]

        options = CleaningOptions(remove_glitches=True)
        cleaned = GlitchFilter().apply(blocks, options)

        assert len(cleaned) == 2
        assert cleaned[0].lines == ["Valid"]
        assert cleaned[1].lines == ["Valid"]

class TestContentNormalizer:
    def test_removes_metadata(self, make_block):
        blocks = [make_block(1, 0, 1000, "Hello align:start position:0%")]
        options = CleaningOptions(remove_metadata=True)
        cleaned = ContentNormalizer().apply(blocks, options)

        assert cleaned[0].lines == ["Hello"]

    def test_simplifies_tags(self, make_block):
        blocks = [make_block(1, 0, 1000, "Hello <c.red>world</c>")]
        options = CleaningOptions(simplify_formatting=True)
        cleaned = ContentNormalizer().apply(blocks, options)

        assert cleaned[0].lines == ["Hello world"]
