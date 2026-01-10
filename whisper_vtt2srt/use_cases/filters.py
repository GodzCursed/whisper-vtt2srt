import re
from typing import Dict, List, TypedDict

from ..domain.interfaces import ContentFilter
from ..domain.models import SubtitleBlock, TimeCode
from ..domain.options import CleaningOptions


class LineEvent(TypedDict):
    """Internal representation of a line's timing for consolidation."""
    text: str
    start: int
    end: int


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

        # 1. Explode blocks into individual line events
        # Format: {'text': "Content", 'start': 1000, 'end': 2000}
        line_events: List[LineEvent] = []
        for block in blocks:
            for line in block.lines:
                clean_line = line.strip()
                if clean_line:
                    line_events.append({
                        'text': clean_line,
                        'start': block.start.milliseconds,
                        'end': block.end.milliseconds
                    })

        if not line_events:
            return []

        # 2. Consolidate consecutive events for the same text
        # We process events in order. If 'text' matches the last processed event
        # and timing is contiguous (or overlapping), we merge them.

        # We need a way to look back at the 'active' entry for this specific text.
        # But simply iterating and merging "same text" is enough if the VTT is sequential.


        # Helper to find if we can merge with the VERY LAST entry of this same text
        # Ideally, we just check the list tip. But since we might have interleaved lines:
        # Block 1: "A"
        # Block 2: "A", "B"
        # We will see events: (A, t1, t2), (A, t2, t3), (B, t2, t3).
        # We want to merge the second A into the first A.

        # We can track "open" lines by text content.
        # But simple approach: Sort by Text then Start Time?
        # No, duplicate lines might appear later (e.g. chorus in song) and shouldn't merge.
        # We only merge if they are effectively adjacent in the original stream.

        # Let's iterate original stream and maintain a "buffer" of active lines.

        # Actually, simpler:
        # Group by text? No.
        # Just iterate. If we see "A" and we recently saw "A" and the gap is small (< 500ms?), merge.

        # Wait, using a map prevents "Chorus" (repeated lines later).
        # We need a list of consolidated objects.

        final_list: List[LineEvent] = []

        # Tracking the index of the last occurrence of each text in 'final_list'
        last_seen_index: Dict[str, int] = {} # text -> index in final_list

        tolerance_ms = 100 # Allow small gaps (e.g. 3.110 to 3.120 usually connects)

        for event in line_events:
            text = str(event['text'])
            start = int(event['start'])
            end = int(event['end'])

            merged = False

            # Check for EXACT match merge first (standard consolidation)
            if text in last_seen_index:
                idx = last_seen_index[text]
                last_entry = final_list[idx]

                if start <= last_entry['end'] + tolerance_ms:
                    last_entry['end'] = max(last_entry['end'], end)
                    merged = True

            # If not merged, check if this is a "growth" of the LAST event in the stream
            # e.g., "Hello" followed by "Hello world"
            if not merged and final_list:
                last_entry = final_list[-1]
                # Only if they are contiguous/close
                if start <= last_entry['end'] + tolerance_ms:
                    if text.startswith(last_entry['text']):
                        # This new event subsumes the previous one
                        last_entry['text'] = text
                        last_entry['end'] = max(last_entry['end'], end)
                        # Update index map to point this new text to the same entry
                        last_seen_index[text] = len(final_list) - 1
                        merged = True

            if not merged:
                # Create new entry
                new_entry: LineEvent = {'text': text, 'start': start, 'end': end}
                final_list.append(new_entry)
                last_seen_index[text] = len(final_list) - 1

        # 3. Convert back to SubtitleBlocks
        # Sort by start time for proper SRT ordering
        final_list.sort(key=lambda x: (x['start'], x['end']))

        new_blocks = []
        for i, item in enumerate(final_list, 1):
            new_blocks.append(SubtitleBlock(
                index=i,
                start=TimeCode(item['start']),
                end=TimeCode(item['end']),
                lines=[item['text']]
            ))

        return new_blocks

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


class SoundDescriptionFilter(ContentFilter):
    """Removes sound descriptions like [Music], [Applause], etc."""

    def apply(self, blocks: List[SubtitleBlock], options: CleaningOptions) -> List[SubtitleBlock]:
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
