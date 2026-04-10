"""Shared test fixtures."""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_contract() -> str:
    return (FIXTURES_DIR / "sample_contract.txt").read_text(encoding="utf-8")


@pytest.fixture
def sample_clean() -> str:
    return (FIXTURES_DIR / "sample_clean.txt").read_text(encoding="utf-8")


@pytest.fixture
def sample_contract_path() -> Path:
    return FIXTURES_DIR / "sample_contract.txt"


@pytest.fixture
def sample_clean_path() -> Path:
    return FIXTURES_DIR / "sample_clean.txt"


@pytest.fixture
def sample_general() -> str:
    return (FIXTURES_DIR / "sample_general.txt").read_text(encoding="utf-8")


@pytest.fixture
def sample_general_path() -> Path:
    return FIXTURES_DIR / "sample_general.txt"
