from typing import Optional

from ..adapters.parsers import VttParser
from ..adapters.writers import SrtWriter
from ..domain.options import CleaningOptions
from .filters import ContentNormalizer, GlitchFilter, KaraokeDeduplicator, ShortLineMerger, SoundDescriptionFilter


class Pipeline:
    """Orchestrates the full VTT to SRT conversion process.

    This class combines the parser, the cleaning filters, and the writer into a
    single flow. It is the main entry point for in-memory conversion.

    Attributes:
        options (CleaningOptions): Configuration for the cleaning filters.
        parser (VttParser): The component that reads VTT text.
        writer (SrtWriter): The component that builds SRT text.
        filters (List[ContentFilter]): A list of filters to apply sequentially.
    """

    def __init__(self, options: Optional[CleaningOptions] = None):
        self.options = options or CleaningOptions()
        self.parser = VttParser()
        self.writer = SrtWriter()

        # Register filters
        self.filters = [
            SoundDescriptionFilter(),  # Clean sound descriptions first
            ContentNormalizer(),
            GlitchFilter(),
            KaraokeDeduplicator(),
            ShortLineMerger()
        ]

    def convert(self, content: str) -> str:
        """Converts raw VTT string content into formatted SRT string content.

        Args:
            content: The raw text content of a WebVTT file.

        Returns:
            str: The processed content formatted as SubRip (SRT).
        """
        # 1. Parse
        blocks = list(self.parser.parse(content))

        # 2. Clean/Filter
        for filter_ in self.filters:
            blocks = filter_.apply(blocks, self.options)

        # 3. Write
        return self.writer.write(blocks)
