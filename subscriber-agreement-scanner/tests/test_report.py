"""Tests for report output formatting."""

import json
import re

from bastion_scan.extractor import ExtractionResult
from bastion_scan.readability import compute_readability
from bastion_scan.scanner import scan
from bastion_scan.report import render


def _make_extraction(text: str, source: str = "test.txt") -> ExtractionResult:
    return ExtractionResult(text=text, source=source)


def test_terminal_output(sample_contract):
    extraction = _make_extraction(sample_contract)
    result = scan(sample_contract)
    output = render(extraction, result, readability=compute_readability(sample_contract), fmt="terminal")
    assert "BASTION" in output
    assert "RED FLAGS" in output
    assert "SCORE:" in output


def test_terminal_no_color(sample_contract):
    extraction = _make_extraction(sample_contract)
    result = scan(sample_contract)
    output = render(extraction, result, readability=compute_readability(sample_contract), fmt="terminal", no_color=True)
    # Should not contain ANSI escape codes
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*m")
    assert not ansi_pattern.search(output), "Output contains ANSI codes with --no-color"


def test_terminal_verbose(sample_contract):
    extraction = _make_extraction(sample_contract)
    result = scan(sample_contract)
    output = render(extraction, result, readability=compute_readability(sample_contract), fmt="terminal", verbose=True)
    assert "TRIGGER:" in output


def test_json_output_valid(sample_contract):
    extraction = _make_extraction(sample_contract)
    result = scan(sample_contract)
    output = render(extraction, result, readability=compute_readability(sample_contract), fmt="json")
    data = json.loads(output)  # should not raise
    assert "findings" in data
    assert "score" in data
    assert data["score"]["red"] == 19
    assert data["score"]["yellow"] == 14


def test_json_output_verbose(sample_contract):
    extraction = _make_extraction(sample_contract)
    result = scan(sample_contract)
    output = render(extraction, result, readability=compute_readability(sample_contract), fmt="json", verbose=True)
    data = json.loads(output)
    for finding in data["findings"]:
        assert "trigger" in finding
        assert "evidence" in finding


def test_json_output_has_all_fields(sample_contract):
    extraction = _make_extraction(sample_contract)
    result = scan(sample_contract)
    output = render(extraction, result, readability=compute_readability(sample_contract), fmt="json")
    data = json.loads(output)
    assert data["version"] == "1.0.0"
    assert data["source"] == "test.txt"
    assert "word_count" in data
    for f in data["findings"]:
        assert "id" in f
        assert "name" in f
        assert "severity" in f


def test_markdown_output(sample_contract):
    extraction = _make_extraction(sample_contract)
    result = scan(sample_contract)
    output = render(extraction, result, readability=compute_readability(sample_contract), fmt="md")
    assert output.startswith("# BASTION")
    assert "## RED FLAGS" in output
    assert "**Score:**" in output


def test_markdown_verbose(sample_contract):
    extraction = _make_extraction(sample_contract)
    result = scan(sample_contract)
    output = render(extraction, result, readability=compute_readability(sample_contract), fmt="md", verbose=True)
    assert "**Trigger:**" in output


def test_clean_contract_report(sample_clean):
    extraction = _make_extraction(sample_clean)
    result = scan(sample_clean)
    output = render(extraction, result, readability=compute_readability(sample_clean), fmt="terminal", no_color=True)
    assert "0 RED" in output
    assert "0 YELLOW" in output


def test_clean_contract_json(sample_clean):
    extraction = _make_extraction(sample_clean)
    result = scan(sample_clean)
    output = render(extraction, result, readability=compute_readability(sample_clean), fmt="json")
    data = json.loads(output)
    assert data["score"]["red"] == 0
    assert data["score"]["yellow"] == 0


def test_terminal_shows_readability(sample_contract):
    extraction = _make_extraction(sample_contract)
    result = scan(sample_contract)
    readability = compute_readability(sample_contract)
    output = render(extraction, result, readability=readability, fmt="terminal", no_color=True)
    assert "Reading Level:" in output
    assert "Grade" in output


def test_json_has_readability(sample_contract):
    extraction = _make_extraction(sample_contract)
    result = scan(sample_contract)
    readability = compute_readability(sample_contract)
    output = render(extraction, result, readability=readability, fmt="json")
    data = json.loads(output)
    assert "readability" in data
    assert "grade_level" in data["readability"]
    assert "interpretation" in data["readability"]
    assert "word_count" in data["readability"]
    assert "sentence_count" in data["readability"]


def test_markdown_has_readability(sample_contract):
    extraction = _make_extraction(sample_contract)
    result = scan(sample_contract)
    readability = compute_readability(sample_contract)
    output = render(extraction, result, readability=readability, fmt="md")
    assert "Reading Level" in output
