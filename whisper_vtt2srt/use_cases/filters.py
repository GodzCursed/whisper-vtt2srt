"""Content filters for the VTT to SRT conversion pipeline.

This module provides a collection of filters that implement the ContentFilter
interface. Each filter performs a specific cleaning or transformation operation
on subtitle blocks, following the Chain of Responsibility pattern.

Filters are designed to be composable and can be enabled/disabled individually
through the CleaningOptions configuration.

Example:
    >>> from whisper_vtt2srt.use_cases.filters import KaraokeDeduplicator
    >>> from whisper_vtt2srt.domain.options import CleaningOptions
    >>> deduplicator = KaraokeDeduplicator()
    >>> cleaned_blocks = deduplicator.apply(blocks, CleaningOptions())
"""

import re
from typing import List

from ..domain.interfaces import ContentFilter
from ..domain.models import SubtitleBlock
from ..domain.options import CleaningOptions


class ContentNormalizer(ContentFilter):
    """Removes VTT-specific metadata and formatting tags from subtitle blocks.

    This filter cleans up WebVTT artifacts that are not valid in the SRT format,
    including positioning metadata (`align:`, `position:`, `line:`) and inline
    formatting tags (`<c>`, `<b>`, `<i>`, timestamps like `<00:00:01.234>`).

    Attributes:
        None

    Note:
        This filter should typically run early in the pipeline to ensure
        downstream filters work with clean text content.
    """

    def apply(self, blocks: List[SubtitleBlock], options: CleaningOptions) -> List[SubtitleBlock]:
        """Apply content normalization to all subtitle blocks.

        Args:
            blocks: List of subtitle blocks to process.
            options: Configuration options controlling which normalizations to apply.

        Returns:
            List of blocks with cleaned text. Empty blocks are removed.
        """
        if not options.remove_metadata and not options.simplify_formatting:
            return blocks

        for block in blocks:
            new_lines = []
            for line in block.lines:
                # Remove VTT alignment tags (align:start, position:0%)
                if options.remove_metadata:
                    line = re.sub(r" align:\S+", "", line)
                    line = re.sub(r" position:\S+", "", line)
                    line = re.sub(r" line:\S+", "", line)

                # Remove <c>, <timestamp>, and other tags
                if options.simplify_formatting:
                    line = re.sub(r"<[^>]+>", "", line)

                # Clean extra whitespace
                line = line.strip()
                if line:
                    new_lines.append(line)
            block.lines = new_lines

        return [b for b in blocks if b.lines] # Remove empty blocks

class GlitchFilter(ContentFilter):
    """Removes subtitle blocks with imperceptibly short durations.

    AI transcription tools often produce "glitch" blocks lasting only a few
    milliseconds. These blocks are invisible to viewers but can cause issues
    in TTS pipelines and video player rendering.

    Attributes:
        MIN_DURATION_MS: Minimum block duration in milliseconds (default: 50).
            Blocks shorter than this threshold are removed.
    """

    MIN_DURATION_MS = 50

    def apply(self, blocks: List[SubtitleBlock], options: CleaningOptions) -> List[SubtitleBlock]:
        """Remove blocks shorter than the minimum duration threshold.

        Args:
            blocks: List of subtitle blocks to filter.
            options: Configuration options. Uses `remove_glitches` flag.

        Returns:
            Filtered list containing only blocks with sufficient duration.
        """
        if not options.remove_glitches:
            return blocks

        return [b for b in blocks if b.duration_ms >= self.MIN_DURATION_MS]


class KaraokeDeduplicator(ContentFilter):
    """Removes duplicate "context lines" from Whisper's karaoke-style VTT output.

    Whisper and similar AI transcription tools produce VTT files with a distinctive
    pattern where each block contains two lines:

    - **Line 1**: The text from the previous segment (for visual continuity)
    - **Line 2**: The new text being revealed in this segment

    This creates a "karaoke effect" where text appears to accumulate on screen.
    This filter identifies and removes these duplicate context lines, keeping only
    the genuinely new content while preserving the original timestamps.

    Algorithm:
        1. Track the text shown in the previous kept block (`prev_shown_text`)
        2. For each line in the current block, skip it if it matches `prev_shown_text`
        3. Merge remaining lines into a single line per block
        4. Remove blocks that contain only duplicate content (e.g., silence periods)

    Example:
        Input blocks::

            Block 1 (0:00-0:03): ["APIs are everywhere."]
            Block 2 (0:03-0:05): ["APIs are everywhere.", "They power your apps."]
            Block 3 (0:05-0:05): ["They power your apps."]  # Glitch, only duplicate
            Block 4 (0:05-0:07): ["They power your apps.", "And your cloud."]

        Output blocks::

            Block 1 (0:00-0:03): ["APIs are everywhere."]
            Block 2 (0:03-0:05): ["They power your apps."]
            Block 3 (0:05-0:07): ["And your cloud."]

    Note:
        This filter preserves original timestamps exactly as they appear in the
        source VTT file. Unlike approaches that attempt to merge or extend
        timestamps, this ensures no timestamp overlap occurs in the output.
    """

    def apply(self, blocks: List[SubtitleBlock], options: CleaningOptions) -> List[SubtitleBlock]:
        """Remove karaoke-style duplicate lines from subtitle blocks.

        Args:
            blocks: List of subtitle blocks to deduplicate.
            options: Configuration options. Uses `remove_pixelation` flag.

        Returns:
            Deduplicated list with sequential indices. Blocks containing only
            duplicate content are removed entirely.
        """
        if not options.remove_pixelation or not blocks:
            return blocks

        filtered_blocks = []
        prev_shown_text = ""

        for block in blocks:
            new_lines = []

            for line in block.lines:
                line_stripped = line.strip()

                if not line_stripped:
                    continue

                if line_stripped == prev_shown_text:
                    continue

                new_lines.append(line_stripped)

            if new_lines:
                merged_text = " ".join(new_lines)
                block.lines = [merged_text]
                prev_shown_text = merged_text
                filtered_blocks.append(block)

        for idx, block in enumerate(filtered_blocks, 1):
            block.index = idx

        return filtered_blocks


class ShortLineMerger(ContentFilter):
    """Merges short lines within a block to optimize subtitle readability.

    Subtitle standards (Netflix, YouTube) recommend a maximum line length of
    approximately 42 characters. This filter combines short lines within a
    single block when doing so would not exceed the configured maximum length.

    Attributes:
        None (uses `max_line_length` from CleaningOptions)

    Note:
        This filter operates within individual blocks only; it does not merge
        lines across different subtitle blocks.
    """

    def apply(self, blocks: List[SubtitleBlock], options: CleaningOptions) -> List[SubtitleBlock]:
        """Merge short lines within blocks up to the maximum line length.

        Args:
            blocks: List of subtitle blocks to process.
            options: Configuration options. Uses `merge_short_lines` flag
                and `max_line_length` value.

        Returns:
            Blocks with merged lines where applicable.
        """
        if not options.merge_short_lines:
            return blocks

        for block in blocks:
            if len(block.lines) < 2:
                continue

            merged_lines = []
            current_line = block.lines[0]

            for next_line in block.lines[1:]:
                # Check length constraint: current + space + next
                combined_len = len(current_line) + 1 + len(next_line)

                if combined_len <= options.max_line_length:
                    current_line = f"{current_line} {next_line}"
                else:
                    merged_lines.append(current_line)
                    current_line = next_line

            merged_lines.append(current_line)
            block.lines = merged_lines

        return blocks


class SoundDescriptionFilter(ContentFilter):
    """Removes non-speech sound descriptions from subtitle content.

    AI transcription tools often include bracketed annotations for non-speech
    sounds such as `[Music]`, `[Applause]`, `[Laughter]`, etc. While useful
    for accessibility, these annotations can cause issues in TTS pipelines
    where they would be read aloud literally.

    This filter removes any text enclosed in square brackets.

    Example:
        Input: ``"[Music] Hello world [Applause]"``
        Output: ``"Hello world"``

    Note:
        Blocks that contain only sound descriptions (no actual speech) are
        removed entirely from the output.
    """

    def apply(self, blocks: List[SubtitleBlock], options: CleaningOptions) -> List[SubtitleBlock]:
        """Remove bracketed sound descriptions from all blocks.

        Args:
            blocks: List of subtitle blocks to filter.
            options: Configuration options. Uses `remove_sound_descriptions` flag.

        Returns:
            Filtered list with sound descriptions removed. Blocks containing
            only sound descriptions are excluded.
        """
        if not options.remove_sound_descriptions:
            return blocks

        filtered_blocks = []
        for block in blocks:
            new_lines = []
            for line in block.lines:
                # Remove content within square brackets [Music]
                clean_line = re.sub(r'\[[^\]]+\]', '', line)
                clean_line = clean_line.strip()
                if clean_line:
                    new_lines.append(clean_line)

            if new_lines:
                block.lines = new_lines
                filtered_blocks.append(block)

        return filtered_blocks
