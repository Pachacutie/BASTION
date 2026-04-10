"""Extract text from PDF files, text files, or stdin."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import pdfplumber


@dataclass
class ExtractionResult:
    text: str
    source: str
    page_count: int | None = None
    word_count: int = 0

    def __post_init__(self):
        self.word_count = len(self.text.split())


def extract_from_pdf(path: Path) -> ExtractionResult:
    """Extract text from a PDF file."""
    try:
        with pdfplumber.open(path) as pdf:
            pages = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)

            if not pages:
                raise ValueError(
                    f"This PDF appears to be image-based. Text extraction is not "
                    f"supported in v1. Try converting with OCR first."
                )

            return ExtractionResult(
                text="\n\n".join(pages),
                source=str(path),
                page_count=len(pdf.pages),
            )
    except (OSError, pdfplumber.pdfminer.pdfparser.PDFSyntaxError, ValueError) as e:
        raise ValueError(f"Could not read '{path}' — {e}") from e


def extract_from_text(path: Path) -> ExtractionResult:
    """Extract text from a plain text file."""
    return ExtractionResult(
        text=path.read_text(encoding="utf-8"),
        source=str(path),
    )


def extract_from_stdin() -> ExtractionResult:
    """Read text from stdin."""
    text = sys.stdin.read()
    if not text.strip():
        raise ValueError("No input received from stdin.")
    return ExtractionResult(text=text, source="stdin")


def extract(file_path: str | None = None) -> ExtractionResult:
    """Extract text from a file or stdin.

    Args:
        file_path: Path to PDF or text file. None reads from stdin.
    """
    if file_path is None:
        return extract_from_stdin()

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")

    if path.suffix.lower() == ".pdf":
        return extract_from_pdf(path)
    else:
        return extract_from_text(path)
