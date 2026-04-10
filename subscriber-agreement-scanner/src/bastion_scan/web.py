"""Flask web interface for bastion-scan."""

from __future__ import annotations

import os
import tempfile
import time
from collections import defaultdict
from pathlib import Path

from flask import Flask, render_template, request

from .extractor import extract, ExtractionResult
from .readability import compute_readability
from .report import render
from .scanner import scan

# Rate limiting: {ip: [timestamps]}
_rate_log: dict[str, list[float]] = defaultdict(list)
_RATE_LIMIT = 10  # requests per minute
_RATE_WINDOW = 60  # seconds


def _is_rate_limited(ip: str) -> bool:
    now = time.time()
    _rate_log[ip] = [t for t in _rate_log[ip] if now - t < _RATE_WINDOW]
    if len(_rate_log[ip]) >= _RATE_LIMIT:
        return True
    _rate_log[ip].append(now)
    return False


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB
    is_hosted = os.environ.get("BASTION_HOSTED", "").lower() in ("1", "true", "yes")

    @app.route("/")
    def index():
        return render_template("index.html", hosted=is_hosted)

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/scan", methods=["POST"])
    def scan_contract():
        if is_hosted and _is_rate_limited(request.remote_addr or "unknown"):
            return render_template(
                "index.html", hosted=is_hosted,
                error="Too many requests. Please wait a minute and try again.",
            )

        tmp_path = None
        try:
            extraction, tmp_path = _extract_from_request()
        except ValueError as e:
            return render_template("index.html", hosted=is_hosted, error=str(e))
        finally:
            if tmp_path:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

        result = scan(extraction.text)
        readability = compute_readability(extraction.text)
        report_html = render(
            extraction, result,
            readability=readability,
            fmt="html",
            verbose=True,
        )
        return render_template("index.html", hosted=is_hosted, report_html=report_html)

    return app


ALLOWED_EXTENSIONS = {".pdf", ".txt", ".text"}


def _extract_from_request() -> tuple[ExtractionResult, str | None]:
    """Extract text from uploaded file or pasted text. Returns (result, tmp_path)."""
    file = request.files.get("file")
    text = request.form.get("text", "").strip()

    if file and file.filename:
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {ext}. Please upload a PDF or text file."
            )
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            file.save(tmp.name)
            return extract(tmp.name), tmp.name

    if text:
        return ExtractionResult(text=text, source="pasted text"), None

    raise ValueError("Please upload a file or paste contract text.")
