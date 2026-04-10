"""Tests for text extraction."""

from pathlib import Path
from unittest.mock import patch

import pytest

from bastion_scan.extractor import extract, ExtractionResult


def test_extract_text_file(sample_contract_path):
    result = extract(str(sample_contract_path))
    assert isinstance(result, ExtractionResult)
    assert result.word_count > 0
    assert "ACME HOME SECURITY" in result.text
    assert result.page_count is None  # text files have no page count
    assert result.source == str(sample_contract_path)


def test_extract_clean_file(sample_clean_path):
    result = extract(str(sample_clean_path))
    assert "GUARDIAN HOME SECURITY" in result.text


def test_extract_missing_file():
    with pytest.raises(FileNotFoundError, match="File not found"):
        extract("/nonexistent/file.txt")


def test_extract_stdin():
    with patch("sys.stdin") as mock_stdin:
        mock_stdin.read.return_value = "This is test input from stdin."
        result = extract(None)
        assert result.text == "This is test input from stdin."
        assert result.source == "stdin"


def test_extract_empty_stdin():
    with patch("sys.stdin") as mock_stdin:
        mock_stdin.read.return_value = "   "
        with pytest.raises(ValueError, match="No input received"):
            extract(None)


def test_extract_word_count(sample_contract_path):
    result = extract(str(sample_contract_path))
    assert result.word_count > 100  # contract has substantial text
