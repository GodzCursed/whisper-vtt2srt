import re
from typing import Generator

from ..domain.interfaces import SubtitleParser
from ..domain.models import SubtitleBlock, TimeCode


class VttParser(SubtitleParser):
    """
    Robust State Machine Parser for WebVTT.
    """

    # Regex to capture timestamps: 00:00:00.000 --> 00:00:05.000
    TIMESTAMP_PATTERN = re.compile(
        r'((?:\d{2}:)?\d{2}:\d{2}\.\d{3})\s-->\s((?:\d{2}:)?\d{2}:\d{2}\.\d{3})'
    )

    def parse(self, content: str) -> Generator[SubtitleBlock, None, None]:
        lines = content.splitlines()
        current_block = None
        block_index = 1

        potential_id = None

        for line in lines:
            line = line.strip()

            # Skip header or empty lines at the start (if parsing hasn't started)
            if not current_block and (
                not line
                or line == "WEBVTT"
                or line.startswith("Kind:")
                or line.startswith("Language:")
            ):
                continue

            # Check for timestamp
            match = self.TIMESTAMP_PATTERN.search(line)
            if match:
                # If we have a potential_id buffered, it was indeed an ID for this new block. Discard it.
                potential_id = None

                # If we were building a previous block, yield it
                if current_block:
                    yield current_block
                    block_index += 1

                start_str, end_str = match.groups()
                current_block = SubtitleBlock(
                    index=block_index,
                    start=TimeCode.from_str(start_str),
                    end=TimeCode.from_str(end_str),
                    lines=[]
                )
                continue

            # If inside a block, add content lines
            if current_block:
                # If line is empty, it might mean end of block, but we keep going until next timestamp or EOF
                if not line:
                    continue

                # Handle potential IDs
                if line.isdigit():
                    # If we already have a potential ID buffered, the previous one was likely text (e.g. "1" then "2")
                    # Flush the previous one as text
                    if potential_id:
                        current_block.lines.append(potential_id)

                    potential_id = line
                    continue
                else:
                    # It's an ordinary line
                    # If we have a buffered potential ID, it was actually text! Flush it.
                    if potential_id:
                        current_block.lines.append(potential_id)
                        potential_id = None

                    current_block.lines.append(line)

        # Flush trailing potential ID if it exists (at EOF, a number is just text)
        if current_block and potential_id:
            current_block.lines.append(potential_id)

        # Yield the final block
        if current_block:
            yield current_block
