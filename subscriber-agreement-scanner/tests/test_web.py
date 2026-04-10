"""Tests for the Flask web interface."""

from io import BytesIO
from pathlib import Path

import pytest

from bastion_scan.web import create_app

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_index_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"BASTION" in resp.data
    assert b"Upload your contract" in resp.data or b"Drop your contract" in resp.data


def test_scan_with_text(client):
    resp = client.post("/scan", data={
        "text": "Customer shall pay an early termination fee equal to the remaining balance. "
                "All disputes resolved by binding arbitration.",
    })
    assert resp.status_code == 200
    assert b"RED" in resp.data
    assert b"critical flags detected" in resp.data


def test_scan_with_file(client):
    fixture = FIXTURES_DIR / "sample_contract.txt"
    data = fixture.read_bytes()
    resp = client.post("/scan", data={
        "file": (BytesIO(data), "contract.txt"),
    }, content_type="multipart/form-data")
    assert resp.status_code == 200
    assert b"RED" in resp.data
    assert b"Reading Level" in resp.data


def test_scan_invalid_file_type(client):
    resp = client.post("/scan", data={
        "file": (BytesIO(b"not a contract"), "photo.jpg"),
    }, content_type="multipart/form-data")
    assert resp.status_code == 200
    assert b"Unsupported file type" in resp.data


def test_scan_no_input(client):
    resp = client.post("/scan", data={})
    assert resp.status_code == 200
    assert b"Please upload a file" in resp.data


def test_scan_clean_contract(client):
    fixture = FIXTURES_DIR / "sample_clean.txt"
    data = fixture.read_bytes()
    resp = client.post("/scan", data={
        "file": (BytesIO(data), "clean.txt"),
    }, content_type="multipart/form-data")
    assert resp.status_code == 200
    assert b"0 RED" in resp.data


def test_html_report_contains_score(client):
    resp = client.post("/scan", data={
        "text": "This Agreement shall automatically renew for successive 36-month periods. "
                "Provider's maximum liability shall not exceed $500.",
    })
    assert resp.status_code == 200
    assert b"critical flags detected" in resp.data
