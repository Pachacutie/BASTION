"""Output formatting — terminal (rich), JSON, and Markdown."""

from __future__ import annotations

import json
from io import StringIO

from rich.console import Console
from rich.text import Text

from . import __version__
from .extractor import ExtractionResult
from .flags import RED_FLAGS, Severity
from .readability import ReadabilityResult
from .scanner import Finding, ScanResult


# ── Terminal Report ──────────────────────────────────────────────────────────

_SEVERITY_COLORS = {
    Severity.RED: "bold red",
    Severity.YELLOW: "bold yellow",
    Severity.GREEN: "bold green",
}

_SECTION_TITLES = {
    Severity.RED: "RED FLAGS",
    Severity.YELLOW: "YELLOW FLAGS",
    Severity.GREEN: "INFORMATIONAL",
}


def _render_terminal(
    extraction: ExtractionResult,
    result: ScanResult,
    verbose: bool = False,
    no_color: bool = False,
    readability: ReadabilityResult | None = None,
) -> str:
    """Render a terminal report using rich."""
    buf = StringIO()
    console = Console(file=buf, force_terminal=not no_color, no_color=no_color, width=72)

    # Header
    console.print()
    console.print(f"BASTION — Contract Scan v{__version__}", style="bold")
    console.print()

    # File info
    source = extraction.source
    parts = [f"Source: {source}"]
    if extraction.page_count is not None:
        parts.append(f"Pages: {extraction.page_count}")
    parts.append(f"Words: {extraction.word_count:,}")
    console.print(" | ".join(parts))
    console.print()

    if readability:
        console.print(f"Reading Level: Grade {readability.grade_level} ({readability.interpretation})")
        console.print()

    # Group findings by severity
    by_severity: dict[Severity, list[Finding]] = {
        Severity.RED: [],
        Severity.YELLOW: [],
        Severity.GREEN: [],
    }
    for f in result.findings:
        by_severity[f.flag.severity].append(f)

    for severity in (Severity.RED, Severity.YELLOW, Severity.GREEN):
        findings = by_severity[severity]
        if not findings:
            continue

        color = _SEVERITY_COLORS[severity]
        title = _SECTION_TITLES[severity]

        console.print(title, style=color)
        console.print("─" * 50)

        for f in findings:
            # Flag line
            label = f"{f.flag.id:<4}{f.flag.name}"
            detail = f.value if f.value else ""
            if detail:
                console.print(f"{label:<26}{detail}", style=color)
            else:
                console.print(label, style=color)

            if verbose:
                # Show trigger pattern
                console.print(f"    TRIGGER: {f.trigger}", style="dim")
                # Show evidence
                evidence_lines = f.evidence.split("\n")
                for line in evidence_lines[:4]:
                    console.print(f"    \"{line.strip()}\"", style="dim italic")

            # Action (for RED and YELLOW only)
            if f.flag.action:
                console.print(f"    ACTION: {f.flag.action}")

            console.print()

    # Score
    console.print("─" * 50)

    score_parts = []
    if result.red_count > 0:
        score_parts.append(f"[bold red]{result.red_count} RED[/bold red]")
    else:
        score_parts.append(f"0 RED")
    if result.yellow_count > 0:
        score_parts.append(f"[bold yellow]{result.yellow_count} YELLOW[/bold yellow]")
    else:
        score_parts.append(f"0 YELLOW")
    score_parts.append(f"{result.green_count} INFO")

    console.print(f"SCORE: {' · '.join(score_parts)}")

    # Bar
    filled = result.red_count
    total = len(RED_FLAGS)
    bar = "█" * (filled * 3) + "░" * ((total - filled) * 3)
    console.print(f"     {bar} {filled}/{total} critical flags detected")
    console.print()

    return buf.getvalue()


# ── JSON Report ──────────────────────────────────────────────────────────────

def _render_json(
    extraction: ExtractionResult,
    result: ScanResult,
    verbose: bool = False,
    readability: ReadabilityResult | None = None,
) -> str:
    """Render a JSON report."""
    findings_data = []
    for f in result.findings:
        entry = {
            "id": f.flag.id,
            "name": f.flag.name,
            "severity": f.flag.severity.value,
            "description": f.flag.description,
        }
        if f.value:
            entry["value"] = f.value
        if verbose:
            entry["trigger"] = f.trigger
            entry["evidence"] = f.evidence
        if f.flag.action:
            entry["action"] = f.flag.action
        findings_data.append(entry)

    data = {
        "version": __version__,
        "source": extraction.source,
        "page_count": extraction.page_count,
        "word_count": extraction.word_count,
        "score": {
            "red": result.red_count,
            "yellow": result.yellow_count,
            "info": result.green_count,
        },
        "findings": findings_data,
    }
    if readability:
        data["readability"] = {
            "grade_level": readability.grade_level,
            "interpretation": readability.interpretation,
            "word_count": readability.word_count,
            "sentence_count": readability.sentence_count,
        }
    return json.dumps(data, indent=2)


# ── Markdown Report ──────────────────────────────────────────────────────────

def _render_markdown(
    extraction: ExtractionResult,
    result: ScanResult,
    verbose: bool = False,
    readability: ReadabilityResult | None = None,
) -> str:
    """Render a Markdown report."""
    lines = [
        "# BASTION — Contract Scan",
        "",
        f"**Source:** {extraction.source}",
    ]
    if extraction.page_count is not None:
        lines.append(f"**Pages:** {extraction.page_count}")
    lines.append(f"**Words:** {extraction.word_count:,}")
    if readability:
        lines.append(f"**Reading Level:** Grade {readability.grade_level} — {readability.interpretation}")
    lines.append(f"**Score:** {result.red_count} RED · {result.yellow_count} YELLOW · {result.green_count} INFO")
    lines.append("")

    by_severity: dict[Severity, list[Finding]] = {
        Severity.RED: [],
        Severity.YELLOW: [],
        Severity.GREEN: [],
    }
    for f in result.findings:
        by_severity[f.flag.severity].append(f)

    for severity in (Severity.RED, Severity.YELLOW, Severity.GREEN):
        findings = by_severity[severity]
        if not findings:
            continue

        lines.append(f"## {_SECTION_TITLES[severity]}")
        lines.append("")

        for f in findings:
            value_str = f" — {f.value}" if f.value else ""
            lines.append(f"### {f.flag.id}: {f.flag.name}{value_str}")
            lines.append("")
            lines.append(f"{f.flag.description}")
            lines.append("")

            if verbose:
                lines.append(f"**Trigger:** `{f.trigger}`")
                lines.append("")
                lines.append(f"> {f.evidence[:300]}")
                lines.append("")

            if f.flag.action:
                lines.append(f"**Action:** {f.flag.action}")
                lines.append("")

    return "\n".join(lines)


# ── HTML Report ──────────────────────────────────────────────────────────────

_SEVERITY_HTML_COLORS = {
    Severity.RED: "#dc3545",
    Severity.YELLOW: "#f0ad4e",
    Severity.GREEN: "#28a745",
}


def _esc(text: str) -> str:
    """Escape text for safe HTML interpolation."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _render_html(
    extraction: ExtractionResult,
    result: ScanResult,
    verbose: bool = False,
    readability: ReadabilityResult | None = None,
) -> str:
    """Render a self-contained HTML report."""
    from . import __version__ as ver

    findings_html = []
    by_severity: dict[Severity, list[Finding]] = {
        Severity.RED: [], Severity.YELLOW: [], Severity.GREEN: [],
    }
    for f in result.findings:
        by_severity[f.flag.severity].append(f)

    for severity in (Severity.RED, Severity.YELLOW, Severity.GREEN):
        findings_list = by_severity[severity]
        if not findings_list:
            continue
        color = _SEVERITY_HTML_COLORS[severity]
        title = _SECTION_TITLES[severity]
        findings_html.append(f'<h2 style="color:{color};border-bottom:2px solid {color};padding-bottom:8px;margin-top:32px">{title}</h2>')
        for f in findings_list:
            value_str = f' — <strong>{_esc(f.value)}</strong>' if f.value else ""
            findings_html.append(f'<div style="margin:16px 0;padding:16px;background:#f8f9fa;border-left:4px solid {color};border-radius:4px">')
            findings_html.append(f'<div style="font-size:18px;font-weight:bold;color:{color}">{f.flag.id}: {f.flag.name}{value_str}</div>')
            findings_html.append(f'<p style="margin:8px 0;color:#555">{f.flag.description}</p>')
            if f.flag.action:
                findings_html.append(f'<p style="margin:4px 0"><strong>Action:</strong> {f.flag.action}</p>')
            if verbose and f.evidence:
                findings_html.append(f'<details style="margin-top:8px"><summary style="cursor:pointer;color:#888">Show evidence</summary>')
                evidence_escaped = _esc(f.evidence)
                findings_html.append(f'<pre style="background:#fff;padding:12px;border:1px solid #ddd;border-radius:4px;white-space:pre-wrap;font-size:13px;margin-top:8px">{evidence_escaped}</pre>')
                findings_html.append('</details>')
            findings_html.append('</div>')

    findings_block = "\n".join(findings_html)

    # Score bar
    filled = result.red_count
    total = len(RED_FLAGS)
    pct = int((filled / total) * 100) if total else 0
    bar_color = "#dc3545" if filled > total // 2 else "#f0ad4e" if filled > 0 else "#28a745"

    readability_block = ""
    if readability:
        readability_block = f'''
        <div style="margin:16px 0;padding:16px;background:#f0f4ff;border-radius:8px;font-size:16px">
            <strong>Reading Level:</strong> Grade {readability.grade_level} — {readability.interpretation}
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BASTION — Contract Scan Results</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.6;color:#333;max-width:800px;margin:0 auto;padding:24px;background:#fff}}
h1{{font-size:24px;margin-bottom:8px}}
.meta{{color:#666;font-size:14px;margin-bottom:16px}}
.score{{font-size:20px;font-weight:bold;margin:24px 0;padding:20px;background:#f8f9fa;border-radius:8px;text-align:center}}
.bar{{height:24px;background:#e9ecef;border-radius:12px;overflow:hidden;margin:12px auto;max-width:400px}}
.bar-fill{{height:100%;border-radius:12px;transition:width 0.3s}}
</style>
</head>
<body>
<h1>BASTION — Contract Scan Results</h1>
<p class="meta">Source: {_esc(extraction.source)} | Words: {extraction.word_count:,}{f" | Pages: {extraction.page_count}" if extraction.page_count else ""}</p>
{readability_block}
<div class="score">
<span style="color:#dc3545">{result.red_count} RED</span> &middot;
<span style="color:#f0ad4e">{result.yellow_count} YELLOW</span> &middot;
<span style="color:#28a745">{result.green_count} INFO</span>
<div class="bar"><div class="bar-fill" style="width:{pct}%;background:{bar_color}"></div></div>
<div style="font-size:14px;color:#666">{filled}/{total} critical flags detected</div>
</div>
{findings_block}
<footer style="margin-top:48px;padding-top:16px;border-top:1px solid #eee;color:#999;font-size:12px;text-align:center">
BASTION Contract Scan v{ver} — Your contract never left your computer.
</footer>
</body>
</html>'''


# ── Public API ───────────────────────────────────────────────────────────────

def render(
    extraction: ExtractionResult,
    result: ScanResult,
    *,
    fmt: str = "terminal",
    verbose: bool = False,
    no_color: bool = False,
    readability: ReadabilityResult | None = None,
) -> str:
    """Render a scan report.

    Args:
        fmt: "terminal", "json", or "md"
        verbose: Show trigger phrases and evidence
        no_color: Strip ANSI codes (terminal only)
        readability: Optional readability metrics to include in output
    """
    match fmt:
        case "json":
            return _render_json(extraction, result, verbose, readability)
        case "md":
            return _render_markdown(extraction, result, verbose, readability)
        case "html":
            return _render_html(extraction, result, verbose, readability)
        case _:
            return _render_terminal(extraction, result, verbose, no_color, readability)
