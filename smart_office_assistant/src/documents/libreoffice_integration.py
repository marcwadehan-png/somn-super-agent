# LibreOffice integration v22.5
"""
LibreOffice headless conversion support.
Provides DOCX/PPTX/XLSX to PDF conversion via LibreOffice headless mode.
"""

import os
import subprocess
import platform
from pathlib import Path
from typing import Optional, Dict, Any, List

# ── Platform-specific soffice paths ──────────────────────────────────────────
if platform.system() == "Windows":
    _DEFAULT_PATHS = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]
else:
    _DEFAULT_PATHS = [
        "/usr/bin/soffice",
        "/usr/lib/libreoffice/program/soffice",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    ]

# ── Supported conversion formats ────────────────────────────────────────────
SUPPORTED_OUTPUT_FORMATS = {
    "pdf", "doc", "docx", "odt", "rtf",
    "xls", "xlsx", "ods", "csv",
    "ppt", "pptx", "odp",
    "html", "xml", "txt",
}

INPUT_FORMATS = {
    "doc", "docx", "odt", "rtf",
    "xls", "xlsx", "ods", "csv",
    "ppt", "pptx", "odp",
    "html", "xml",
}


class LibreOfficeConverter:
    """
    Wraps LibreOffice headless for file format conversion.

    Usage:
        converter = LibreOfficeConverter()
        result = converter.convert("input.docx", "output.pdf")
        print(result["success"], result.get("output_path"))
    """

    def __init__(
        self,
        soffice_path: Optional[str] = None,
        timeout: int = 120,
    ):
        self.soffice_path = soffice_path or self._find_soffice()
        self.timeout = timeout
        self._available: bool = self.soffice_path is not None and os.path.isfile(self.soffice_path)

    # ── Discovery ───────────────────────────────────────────────────────────

    @staticmethod
    def _find_soffice() -> Optional[str]:
        for p in _DEFAULT_PATHS:
            if os.path.isfile(p):
                return p
        return None

    def is_available(self) -> bool:
        """Return True when a working soffice binary is found."""
        return self._available

    # ── Core conversion ──────────────────────────────────────────────────────

    def convert(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        output_format: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Convert a document to a different format.

        Args:
            input_path:  Path to the source file.
            output_path: Target file path. If None, the output is placed
                         next to the input with the detected format suffix.
            output_format: Target format string (e.g. "pdf"). If None,
                            inferred from output_path suffix.

        Returns:
            {"success": bool, "output_path": str | None, "error": str | None}
        """
        if not self.is_available():
            return {
                "success": False,
                "output_path": None,
                "error": "LibreOffice is not installed or not found",
            }

        input_path = os.path.abspath(input_path)
        if not os.path.isfile(input_path):
            return {
                "success": False,
                "output_path": None,
                "error": f"Input file not found: {input_path}",
            }

        # Resolve format
        fmt = (output_format or "").strip().lstrip(".").lower()
        if not fmt and output_path:
            fmt = Path(output_path).suffix.lstrip(".").lower()
        if not fmt:
            return {
                "success": False,
                "output_path": None,
                "error": "Cannot determine output format; provide output_format or output_path with extension",
            }
        if fmt not in SUPPORTED_OUTPUT_FORMATS:
            return {
                "success": False,
                "output_path": None,
                "error": f"Unsupported output format: {fmt}",
            }

        # Resolve output directory
        if output_path:
            out_dir = os.path.dirname(os.path.abspath(output_path))
        else:
            out_dir = os.path.dirname(input_path)

        os.makedirs(out_dir, exist_ok=True)

        cmd = [
            self.soffice_path,
            "--headless",
            "--convert-to", fmt,
            "--outdir", out_dir,
            input_path,
        ]

        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            success = completed.returncode == 0

            # Determine actual output path
            generated = Path(out_dir) / (Path(input_path).stem + "." + fmt)
            resolved = str(generated) if generated.exists() else None

            if output_path and resolved:
                # Rename to requested output_path
                try:
                    os.replace(resolved, os.path.abspath(output_path))
                    resolved = os.path.abspath(output_path)
                except OSError:
                    pass  # keep generated path on conflict

            return {
                "success": success,
                "output_path": resolved,
                "error": None if success else (completed.stderr or "conversion failed"),
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output_path": None,
                "error": f"Conversion timed out after {self.timeout}s",
            }
        except Exception as exc:
            return {
                "success": False,
                "output_path": None,
                "error": str(exc),
            }

    # ── Convenience wrappers ─────────────────────────────────────────────────

    def to_pdf(self, input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Convert any supported file to PDF."""
        return self.convert(input_path, output_path, "pdf")

    def to_docx(self, input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Convert to DOCX."""
        return self.convert(input_path, output_path, "docx")

    def to_xlsx(self, input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Convert to XLSX."""
        return self.convert(input_path, output_path, "xlsx")

    def to_pptx(self, input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Convert to PPTX."""
        return self.convert(input_path, output_path, "pptx")


# ── Module-level singleton ────────────────────────────────────────────────────

_lo_converter: Optional[LibreOfficeConverter] = None


def get_converter() -> LibreOfficeConverter:
    """Return the shared converter instance."""
    global _lo_converter
    if _lo_converter is None:
        _lo_converter = LibreOfficeConverter()
    return _lo_converter


def is_lo_available() -> bool:
    """Quick check for LibreOffice availability."""
    return get_converter().is_available()


def convert_file(
    input_path: str,
    output_path: Optional[str] = None,
    output_format: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience wrapper around get_converter().convert()."""
    return get_converter().convert(input_path, output_path, output_format)


def to_pdf(input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """Convenience wrapper for PDF conversion."""
    return get_converter().to_pdf(input_path, output_path)
