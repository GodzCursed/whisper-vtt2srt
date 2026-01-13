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
    """Tests for the KaraokeDeduplicator filter.

    The new algorithm removes duplicate "context lines" that Whisper includes
    for visual continuity, preserving original timestamps without overlap.
    """

    def test_removes_duplicate_context_lines(self, make_block):
        """Whisper-style output: each block shows previous line + new content.

        Input pattern (typical Whisper karaoke output):
            Block 1: ["Hello world"]
            Block 2: ["Hello world", "How are you?"]  <- "Hello world" is context
            Block 3: ["How are you?", "Nice day."]    <- "How are you?" is context

        Expected output:
            Block 1: ["Hello world"]         (original timestamps preserved)
            Block 2: ["How are you?"]        (duplicate removed, timestamps preserved)
            Block 3: ["Nice day."]           (duplicate removed, timestamps preserved)
        """
        blocks = [
            make_block(1, 0, 1000, "Hello world"),
            make_block(2, 1000, 2000, "Hello world\nHow are you?"),
            make_block(3, 2000, 3000, "How are you?\nNice day.")
        ]

        options = CleaningOptions(remove_pixelation=True)
        cleaned = KaraokeDeduplicator().apply(blocks, options)

        assert len(cleaned) == 3
        assert cleaned[0].lines == ["Hello world"]
        assert cleaned[1].lines == ["How are you?"]
        assert cleaned[2].lines == ["Nice day."]
        # Timestamps are preserved exactly
        assert cleaned[0].start.milliseconds == 0
        assert cleaned[0].end.milliseconds == 1000
        assert cleaned[1].start.milliseconds == 1000
        assert cleaned[1].end.milliseconds == 2000

    def test_removes_blocks_with_only_duplicates(self, make_block):
        """Blocks containing only duplicate content should be removed entirely.

        This handles the micro-glitch pattern where Whisper outputs a block
        that contains only the previous segment's text (e.g., during silence).
        """
        blocks = [
            make_block(1, 0, 1000, "Hello world"),
            make_block(2, 1000, 1010, "Hello world"),  # Only duplicate, remove
            make_block(3, 1010, 2000, "Hello world\nHow are you?")
        ]

        options = CleaningOptions(remove_pixelation=True)
        cleaned = KaraokeDeduplicator().apply(blocks, options)

        assert len(cleaned) == 2
        assert cleaned[0].lines == ["Hello world"]
        assert cleaned[1].lines == ["How are you?"]

    def test_merges_multiple_new_lines_into_single_line(self, make_block):
        """Multiple non-duplicate lines in a block should be merged."""
        blocks = [
            make_block(1, 0, 1000, "First"),
            make_block(2, 1000, 2000, "First\nSecond\nThird")
        ]

        options = CleaningOptions(remove_pixelation=True)
        cleaned = KaraokeDeduplicator().apply(blocks, options)

        assert len(cleaned) == 2
        assert cleaned[1].lines == ["Second Third"]

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
