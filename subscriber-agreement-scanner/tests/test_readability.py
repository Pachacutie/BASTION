"""Tests for readability scoring."""

from bastion_scan.readability import compute_readability, ReadabilityResult


def test_readability_returns_result():
    result = compute_readability("This is a simple sentence. Another one here.")
    assert isinstance(result, ReadabilityResult)
    assert isinstance(result.grade_level, float)
    assert isinstance(result.interpretation, str)


def test_readability_simple_text():
    text = "The cat sat on the mat. The dog ran fast. I like my home."
    result = compute_readability(text)
    assert result.grade_level < 6


def test_readability_complex_text():
    text = (
        "Notwithstanding the aforementioned provisions, the indemnification "
        "obligations herein shall survive the termination or expiration of "
        "this agreement in perpetuity. The subrogation rights established "
        "pursuant to the arbitration provisions shall be enforceable "
        "irrespective of jurisdictional limitations. Furthermore, the "
        "consequential damages exclusion shall apply retroactively to all "
        "antecedent obligations and representations."
    )
    result = compute_readability(text)
    assert result.grade_level > 12


def test_interpretation_bands():
    from bastion_scan.readability import _interpret
    assert _interpret(5.0) == "Easy to read"
    assert _interpret(10.0) == "Average complexity"
    assert _interpret(14.0) == "College level — above average complexity"
    assert _interpret(18.0) == "Graduate level — unusually complex"


def test_readability_counts():
    text = "Hello world. Goodbye world."
    result = compute_readability(text)
    assert result.word_count == 4
    assert result.sentence_count == 2


def test_readability_empty_text():
    result = compute_readability("")
    assert result.grade_level == 0.0
    assert result.interpretation == "Easy to read"
