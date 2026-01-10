import re
from typing import List

from ..domain.interfaces import ContentFilter
from ..domain.models import SubtitleBlock
from ..domain.options import CleaningOptions


class ContentNormalizer(ContentFilter):
    """Removes VTT metadata and formatting tags."""

    def apply(self, blocks: List[SubtitleBlock], options: CleaningOptions) -> List[SubtitleBlock]:
        if not options.remove_metadata and not options.simplify_formatting:
            return blocks

        for block in blocks:
            new_lines = []
            for line in block.lines:
                # Remove VTT alignment tags (align:start, position:0%)
                if options.remove_metadata:
                    line = re.sub(r' align:\S+', '', line)
                    line = re.sub(r' position:\S+', '', line)
                    line = re.sub(r' line:\S+', '', line)

                # Remove <c>, <timestamp>, and other tags
                if options.simplify_formatting:
                    line = re.sub(r'<[^>]+>', '', line)

                # Clean extra whitespace
                line = line.strip()
                if line:
                    new_lines.append(line)
            block.lines = new_lines

        return [b for b in blocks if b.lines] # Remove empty blocks

class GlitchFilter(ContentFilter):
    """Removes blocks that are too short to be readable."""

    MIN_DURATION_MS = 50

    def apply(self, blocks: List[SubtitleBlock], options: CleaningOptions) -> List[SubtitleBlock]:
        if not options.remove_glitches:
            return blocks

        return [b for b in blocks if b.duration_ms >= self.MIN_DURATION_MS]

class KaraokeDeduplicator(ContentFilter):
    """
    Simulates the "Anti-Karaoke" logic.
    Merges/Removes blocks where the text is just a prefix of the next block.
    """

    def apply(self, blocks: List[SubtitleBlock], options: CleaningOptions) -> List[SubtitleBlock]:
        if not options.remove_pixelation:
            return blocks

        cleaned_blocks = []

        # Cache original text to handle daisy-chain stripping (A -> AB -> ABC)
        original_texts = [" ".join(b.lines).strip() for b in blocks]

        for i in range(len(blocks)):
            current = blocks[i]

            # If this is the last block, just add it
            if i == len(blocks) - 1:
                if any(current.lines):
                    cleaned_blocks.append(current)
                continue

            curr_text_raw = original_texts[i]
            next_text_raw = original_texts[i+1]

            # 1. Exact duplicate? Skip current.
            if curr_text_raw == next_text_raw:
                continue

            # 2. Current is prefix of Next? (Karaoke effect)
            if next_text_raw.startswith(curr_text_raw) and curr_text_raw:
                # Calculate what to keep in the NEXT block
                # We strip the length of the current raw text from the next raw text
                remainder = next_text_raw[len(curr_text_raw):].strip()

                next_block = blocks[i+1]
                if remainder:
                    next_block.lines = [remainder]
                else:
                    next_block.lines = [] # Mark as empty

            # Add current if not empty
            if any(line.strip() for line in current.lines):
                cleaned_blocks.append(current)

        # Re-index
        final_blocks = []
        for idx, block in enumerate(cleaned_blocks, 1):
            if any(line.strip() for line in block.lines):
                block.index = idx
                final_blocks.append(block)

        return final_blocks

class ShortLineMerger(ContentFilter):
    """Merges short lines within a block into valid single lines."""

    def apply(self, blocks: List[SubtitleBlock], options: CleaningOptions) -> List[SubtitleBlock]:
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
