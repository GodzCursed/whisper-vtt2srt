from pathlib import Path
from typing import List, Optional

from whisper_vtt2srt.domain.options import CleaningOptions
from whisper_vtt2srt.use_cases.pipeline import Pipeline


class BatchConverter:
    def __init__(self, options: Optional[CleaningOptions] = None):
        self.pipeline = Pipeline(options)

    def convert(self,
                input_path: str,
                output_path: Optional[str] = None,
                recursive: bool = False,
                encoding: str = "utf-8") -> List[str]:
        """Converts a VTT file or a directory of files to SRT.

        Args:
            input_path: Path to a single `.vtt` file or a directory containing them.
            output_path: Optional destination path.
                - If input is a file, this acts as the output filename.
                - If input is a directory, this acts as the output root directory.
                - If None, outputs are generated alongside inputs.
            recursive: If True and input is a directory, processes subdirectories recursively.
            encoding: The encoding of the input file(s) (e.g., "utf-8", "latin-1").
                Defaults to "utf-8".

        Returns:
            List[str]: A list of paths to the generated `.srt` files.

        Raises:
            UnicodeDecodeError: If a file cannot be decoded with the specified encoding.
            IOError: If files cannot be read or written.
        """
        path_obj = Path(input_path)
        processed_files = []

        if path_obj.is_file():
            if self._is_vtt(path_obj):
                result = self._convert_single_file(path_obj, output_path, encoding)
                processed_files.append(result)
        elif path_obj.is_dir():
            if output_path:
                # If output is specified for a dir input, it might be ambiguous depending on requirement.
                # Usually batch processing implies outputting to same dir or a specific output dir.
                # For simplicity/robustness, let's assume output_path is an Output DIRECTORY if input is a dir.
                out_dir = Path(output_path)
                out_dir.mkdir(parents=True, exist_ok=True)
            else:
                out_dir = None

            files_to_process = self._scan_directory(path_obj, recursive)
            for file_path in files_to_process:
                # determine output filename
                if out_dir:
                    rel_path = file_path.relative_to(path_obj)
                    target_srt = out_dir / rel_path.with_suffix(".srt")
                    target_srt.parent.mkdir(parents=True, exist_ok=True)
                    out_file_str = str(target_srt)
                else:
                    out_file_str = None # Let _convert_single_file decide (default: same dir)

                result = self._convert_single_file(file_path, out_file_str, encoding)
                processed_files.append(result)

        return processed_files

    def _scan_directory(self, root: Path, recursive: bool) -> List[Path]:
        vtt_files = []
        if recursive:
            for path in root.rglob("*.vtt"):
                vtt_files.append(path)
        else:
            for path in root.glob("*.vtt"):
                vtt_files.append(path)
        return sorted(vtt_files)

    def _is_vtt(self, path: Path) -> bool:
        return path.suffix.lower() == ".vtt"

    def _convert_single_file(self, intput_file: Path, output_file: Optional[str], encoding: str) -> str:
        # Determine output path if not set
        if not output_file:
            output_file = str(intput_file.with_suffix(".srt"))

        print(f"Converting: {intput_file} -> {output_file}")

        try:
            with open(intput_file, "r", encoding=encoding) as f:
                content = f.read()

            srt_content = self.pipeline.convert(content)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(srt_content)

            return output_file
        except UnicodeDecodeError:
            print(f"Error: Failed to decode {intput_file} with encoding '{encoding}'. Try specifying --encoding.")
            raise
        except Exception as e:
            print(f"Error processing {intput_file}: {e}")
            raise
