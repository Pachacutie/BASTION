"""Flesch-Kincaid readability scoring."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ReadabilityResult:
    grade_level: float
    interpretation: str
    word_count: int
    sentence_count: int


def _count_syllables(word: str) -> int:
    """Estimate syllable count using vowel-group heuristic."""
    word = word.lower().strip()
    if not word:
        return 0
    if word.endswith("e") and len(word) > 2:
        word = word[:-1]
    count = len(re.findall(r"[aeiouy]+", word))
    return max(1, count)


def _interpret(grade: float) -> str:
    """Map grade level to human-readable interpretation."""
    if grade <= 8:
        return "Easy to read"
    if grade <= 12:
        return "Average complexity"
    if grade <= 16:
        return "College level — above average complexity"
    return "Graduate level — unusually complex"


def compute_readability(text: str) -> ReadabilityResult:
    """Compute Flesch-Kincaid Grade Level for the given text."""
    words = re.findall(r"[a-zA-Z']+", text)
    sentences = re.split(r"[.!?]+", text)
    sentences = [s for s in sentences if s.strip()]

    word_count = len(words)
    sentence_count = len(sentences) or 1

    if word_count == 0:
        return ReadabilityResult(
            grade_level=0.0,
            interpretation=_interpret(0.0),
            word_count=0,
            sentence_count=0,
        )

    syllable_count = sum(_count_syllables(w) for w in words)

    grade = (
        0.39 * (word_count / sentence_count)
        + 11.8 * (syllable_count / word_count)
        - 15.59
    )
    grade = round(max(0.0, grade), 1)

    return ReadabilityResult(
        grade_level=grade,
        interpretation=_interpret(grade),
        word_count=word_count,
        sentence_count=sentence_count,
    )
