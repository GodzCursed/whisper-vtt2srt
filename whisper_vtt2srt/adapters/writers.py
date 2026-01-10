from typing import List

from ..domain.models import SubtitleBlock


class SrtWriter:
    """Formats subtitle blocks into SRT format."""

    def write(self, blocks: List[SubtitleBlock]) -> str:
        output = []
        for block in blocks:
            output.append(str(block.index))
            output.append(f"{block.start} --> {block.end}")
            output.extend(block.lines)
            output.append("") # Empty line after each block

        return "\n".join(output).strip() + "\n"
