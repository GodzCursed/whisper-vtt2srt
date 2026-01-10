from dataclasses import dataclass


@dataclass
class CleaningOptions:
    """Configuration options for the VTT to SRT cleaning pipeline.

    Attributes:
        remove_pixelation (bool): If True, removes the "karaoke effect" where text accumulates
            over multiple blocks (e.g., "Hello" -> "Hello world"). Defaults to True.
        remove_glitches (bool): If True, removes blocks with invisible duration (< 50ms)
            that cause player flickering. Defaults to True.
        simplify_formatting (bool): If True, strips internal formatting tags
            like `<b>`, `<i>`, `<c.color>`, etc. Defaults to True.
        remove_metadata (bool): If True, removes positioning tags often found in VTT
            (e.g., `align:start position:0%`). Defaults to True.
        merge_short_lines (bool): If True, aggressively merges short lines into single lines.
            Defaults to False.
    """
    remove_pixelation: bool = True
    remove_glitches: bool = True
    simplify_formatting: bool = True
    remove_metadata: bool = True
    merge_short_lines: bool = False
    max_line_length: int = 42
