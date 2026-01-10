from dataclasses import dataclass, field
from typing import List


@dataclass(order=True)
class TimeCode:
    """Represents a specific point in time used for subtitle scheduling.

    Attributes:
        milliseconds (int): The total time in milliseconds.
    """
    milliseconds: int

    @staticmethod
    def from_str(time_str: str) -> 'TimeCode':
        """Parses a time string into a TimeCode object.

        Supports standard WebVTT formats:
        - `MM:SS.mmm`
        - `HH:MM:SS.mmm`

        Args:
            time_str: The time string to parse (e.g., "00:01:02.500").

        Returns:
            TimeCode: A new instance representing the parsed time.
        """
        parts = time_str.strip().split(':')
        seconds_parts = parts[-1].split('.')

        seconds = int(seconds_parts[0])
        milliseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
        minutes = int(parts[-2])
        hours = int(parts[-3]) if len(parts) > 2 else 0

        total_ms = (hours * 3600000) + (minutes * 60000) + (seconds * 1000) + milliseconds
        return TimeCode(total_ms)

    def to_srt_string(self) -> str:
        """Formats the timecode for SRT output.

        Returns:
            str: Time formatted as `HH:MM:SS,mmm`.
        """
        total_seconds, milliseconds = divmod(self.milliseconds, 1000)
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    def __str__(self):
        return self.to_srt_string()

@dataclass
class SubtitleBlock:
    """Represents a single subtitle event containing text and timing.

    Attributes:
        index (int): The sequential index of the subtitle (1-based).
        start (TimeCode): When the subtitle appears.
        end (TimeCode): When the subtitle disappears.
        lines (List[str]): The text content of the subtitle, split by lines.
    """
    index: int
    start: TimeCode
    end: TimeCode
    lines: List[str] = field(default_factory=list)

    @property
    def duration_ms(self) -> int:
        """Calculates the duration of the subtitle in milliseconds.

        Returns:
            int: The duration in ms.
        """
        return self.end.milliseconds - self.start.milliseconds
