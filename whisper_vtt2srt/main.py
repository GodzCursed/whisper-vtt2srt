import argparse

from whisper_vtt2srt.domain.options import CleaningOptions
from whisper_vtt2srt.use_cases.batch import BatchConverter


def main():
    parser = argparse.ArgumentParser(
        description="Convert WebVTT to SRT with professional cleaning.",
        epilog=(
            "Examples:\n"
            "  whisper-vtt2srt input.vtt\n"
            "  whisper-vtt2srt videos_folder/  --recursive\n"
            "  whisper-vtt2srt input_latin.vtt --encoding ISO-8859-1"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("input", help="Input VTT file or directory")
    parser.add_argument("output", nargs="?", help="Output SRT file or directory (optional)")

    # I/O Options
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively process directories")
    parser.add_argument("-e", "--encoding", default="utf-8", help="Input file encoding (default: utf-8)")

    # Cleaning Options
    parser.add_argument("--no-karaoke", action="store_false", dest="remove_pixelation",
                        default=True, help="Disable anti-karaoke filter (keep accumulating text)")
    parser.add_argument("--keep-glitches", action="store_false", dest="remove_glitches",
                        default=True, help="Keep short <50ms blocks")
    parser.add_argument("--keep-formatting", action="store_false", dest="simplify_formatting",
                        default=True, help="Keep VTT tags (bold, italic, colors)")
    parser.add_argument("--keep-metadata", action="store_false", dest="remove_metadata",
                        default=True, help="Keep metadata tags (align:start, position:0%%)")
    parser.add_argument("--merge-short-lines", action="store_true", dest="merge_short_lines",
                        default=False, help="Aggressively merge short lines into single lines")
    parser.add_argument("--keep-sound-descriptions", action="store_false", dest="remove_sound_descriptions",
                        default=True,
                        help="Keep sound descriptions like [Music], [Applause], [Laughter], etc.")
    parser.add_argument("--max-line-length", type=int, default=42,
                        help="Maximum line length allowed when merging short lines (default: 42)")

    args = parser.parse_args()

    options = CleaningOptions(
        remove_pixelation=args.remove_pixelation,
        remove_glitches=args.remove_glitches,
        simplify_formatting=args.simplify_formatting,
        remove_metadata=args.remove_metadata,
        merge_short_lines=args.merge_short_lines,
        remove_sound_descriptions=args.remove_sound_descriptions,
        max_line_length=args.max_line_length
    )

    converter = BatchConverter(options)

    try:
        results = converter.convert(
            input_path=args.input,
            output_path=args.output,
            recursive=args.recursive,
            encoding=args.encoding
        )

        if not results:
            print("No VTT files found to convert.")
        else:
            print(f"Successfully converted {len(results)} file(s).")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
