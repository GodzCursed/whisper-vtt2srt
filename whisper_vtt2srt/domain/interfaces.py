from abc import ABC, abstractmethod
from typing import Generator, List

from .models import SubtitleBlock
from .options import CleaningOptions


class SubtitleParser(ABC):
    @abstractmethod
    def parse(self, content: str) -> Generator[SubtitleBlock, None, None]:
        """Parses raw content into subtitle blocks."""
        pass

class ContentFilter(ABC):
    @abstractmethod
    def apply(self, blocks: List[SubtitleBlock], options: CleaningOptions) -> List[SubtitleBlock]:
        """Applies a filtering strategy to a list of subtitle blocks."""
        pass
