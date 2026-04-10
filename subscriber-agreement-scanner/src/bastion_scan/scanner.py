"""Core scanning logic — match patterns against extracted text."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .flags import ALL_FLAGS, FLAG_BY_ID, FlagDef, Severity
from .patterns import PATTERNS


@dataclass
class Finding:
    flag: FlagDef
    evidence: str  # the matched text context
    trigger: str  # the pattern that matched
    value: str | None = None  # extracted value for GREEN flags


@dataclass
class ScanResult:
    findings: list[Finding] = field(default_factory=list)
    red_count: int = 0
    yellow_count: int = 0
    green_count: int = 0

    def add(self, finding: Finding):
        self.findings.append(finding)
        match finding.flag.severity:
            case Severity.RED:
                self.red_count += 1
            case Severity.YELLOW:
                self.yellow_count += 1
            case Severity.GREEN:
                self.green_count += 1


def _extract_context(text: str, match: re.Match, chars: int = 200) -> str:
    """Extract surrounding context around a regex match, trimmed to sentence boundaries."""
    start = max(0, match.start() - chars)
    end = min(len(text), match.end() + chars)
    match_offset = match.start() - start
    match_end_offset = match.end() - start

    context = text[start:end]

    # Trim to nearest sentence start (only before the match)
    if start > 0:
        first_period = context.find(". ")
        if first_period != -1 and first_period + 2 < match_offset:
            context = context[first_period + 2 :]
            match_end_offset -= (first_period + 2)

    # Trim to nearest sentence end (only after the match)
    if end < len(text):
        last_period = context.rfind(". ")
        if last_period != -1 and last_period > match_end_offset:
            context = context[: last_period + 1]

    return context.strip()


def _extract_value(text: str, match: re.Match, flag_id: str) -> str | None:
    """Extract a specific value from a GREEN flag match."""
    groups = match.groups()
    if not groups:
        return None

    if flag_id == "G1":
        matched_text = match.group(0)
        # Extract the number from capturing groups (first non-None numeric group)
        for g in match.groups():
            if g and re.fullmatch(r"\d+", g):
                num = int(g)
                if "year" in matched_text.lower():
                    return f"{num * 12} months"
                return f"{num} months"

    elif flag_id == "G2":
        matched_text = match.group(0)
        amount = re.search(r"\$\s*(\d+\.?\d*)", matched_text)
        if amount:
            return f"${amount.group(1)}/month"

    return match.group(0).strip()


_NEGATION_PHRASES = [
    "does not", "will not", "shall not", "is not", "are not",
    "free of", "absence of", "exempt from",
]
_NEGATION_WORDS = {
    "no", "not", "never", "without", "waive", "waives",
    "waived", "neither", "nor", "excluded", "none",
}
# Comparative phrases that look like negation but aren't
_FALSE_NEGATION = [
    "no fewer than", "no less than", "no later than", "no more than",
    "no sooner than", "not less than", "not fewer than", "not later than",
]


def _is_negated(text: str, match: re.Match) -> bool:
    """Check if a match is negated within the same sentence."""
    # Look back to nearest sentence boundary (period, newline, or start)
    before_start = max(0, match.start() - 150)
    before_text = text[before_start:match.start()].lower()
    # Trim to same sentence — find last sentence break
    for sep in [". ", ".\n", "\n\n", "\n"]:
        last_break = before_text.rfind(sep)
        if last_break != -1:
            before_text = before_text[last_break + len(sep):]
            break
    before_words = before_text.split()[-10:]

    after_end = min(len(text), match.end() + 80)
    after_text = text[match.end():after_end].lower()
    after_words = after_text.split()[:3]

    window = " ".join(before_words + after_words)

    # Remove comparative phrases that look like negation but aren't
    for fp in _FALSE_NEGATION:
        window = window.replace(fp, " ")

    count = 0
    for phrase in _NEGATION_PHRASES:
        while phrase in window:
            count += 1
            window = window.replace(phrase, " ", 1)

    for word in window.split():
        if word.strip(".,;:!?'\"()") in _NEGATION_WORDS:
            count += 1

    return count % 2 == 1


def scan(text: str) -> ScanResult:
    """Scan text for all red flag patterns.

    Returns a ScanResult with findings for each detected flag.
    Each flag is reported at most once (first match wins).
    """
    result = ScanResult()
    detected: set[str] = set()

    for flag_def in ALL_FLAGS:
        if flag_def.id not in PATTERNS:
            continue

        for pattern in PATTERNS[flag_def.id]:
            if flag_def.id in detected:
                break

            match = pattern.search(text)
            if match:
                # Skip entire flag if negated (don't try other patterns)
                if flag_def.severity != Severity.GREEN and _is_negated(text, match):
                    detected.add(flag_def.id)
                    break

                detected.add(flag_def.id)
                value = None
                if flag_def.severity == Severity.GREEN:
                    value = _extract_value(text, match, flag_def.id)

                result.add(Finding(
                    flag=flag_def,
                    evidence=_extract_context(text, match),
                    trigger=pattern.pattern,
                    value=value,
                ))

    return result
