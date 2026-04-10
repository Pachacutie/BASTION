"""Tests for scanner core logic."""

from bastion_scan.scanner import scan, ScanResult, Finding
from bastion_scan.flags import Severity


def test_scan_sample_contract_red_flags(sample_contract):
    result = scan(sample_contract)
    red_ids = {f.flag.id for f in result.findings if f.flag.severity == Severity.RED}
    assert "R1" in red_ids, "Should detect auto-renewal"
    assert "R2" in red_ids, "Should detect short cancellation window"
    assert "R3" in red_ids, "Should detect ETF = remaining balance"
    assert "R4" in red_ids, "Should detect liability cap"
    assert "R5" in red_ids, "Should detect forced arbitration"
    assert "R6" in red_ids, "Should detect data sharing"
    assert result.red_count == 19


def test_scan_sample_contract_yellow_flags(sample_contract):
    result = scan(sample_contract)
    yellow_ids = {f.flag.id for f in result.findings if f.flag.severity == Severity.YELLOW}
    assert "Y1" in yellow_ids, "Should detect rate increase"
    assert "Y2" in yellow_ids, "Should detect equipment lease"
    assert "Y3" in yellow_ids, "Should detect monitoring center change"
    assert "Y4" in yellow_ids, "Should detect subrogation waiver"
    assert "Y5" in yellow_ids, "Should detect written cancel only"
    assert "Y6" in yellow_ids, "Should detect installation damage waiver"
    assert result.yellow_count == 14


def test_scan_sample_contract_green_flags(sample_contract):
    result = scan(sample_contract)
    green_ids = {f.flag.id for f in result.findings if f.flag.severity == Severity.GREEN}
    assert "G1" in green_ids, "Should extract contract term"
    assert "G2" in green_ids, "Should extract monthly rate"
    assert "G3" in green_ids, "Should extract equipment ownership"
    assert "G4" in green_ids, "Should extract permit responsibility"
    assert result.green_count == 6


def test_scan_clean_contract_no_red(sample_clean):
    result = scan(sample_clean)
    assert result.red_count == 0, f"Clean contract should have 0 RED, got {result.red_count}"


def test_scan_clean_contract_no_yellow(sample_clean):
    result = scan(sample_clean)
    assert result.yellow_count == 0, f"Clean contract should have 0 YELLOW, got {result.yellow_count}"


def test_scan_empty_text():
    result = scan("")
    assert result.red_count == 0
    assert result.yellow_count == 0
    assert result.green_count == 0


def test_findings_have_evidence(sample_contract):
    result = scan(sample_contract)
    for f in result.findings:
        assert f.evidence, f"Finding {f.flag.id} has no evidence"
        assert len(f.evidence) > 10, f"Finding {f.flag.id} evidence too short"


def test_findings_have_triggers(sample_contract):
    result = scan(sample_contract)
    for f in result.findings:
        assert f.trigger, f"Finding {f.flag.id} has no trigger"


def test_green_flags_have_values(sample_contract):
    result = scan(sample_contract)
    green_findings = [f for f in result.findings if f.flag.severity == Severity.GREEN]
    for f in green_findings:
        assert f.value is not None, f"Green finding {f.flag.id} should have a value"


# --- Negation awareness tests ---

def test_negation_skips_negated_etf():
    text = "There is no early termination fee for this agreement."
    result = scan(text)
    assert result.red_count == 0, "Negated ETF should not trigger R3"


def test_negation_skips_negated_arbitration():
    text = "This agreement does not include binding arbitration."
    result = scan(text)
    r5 = [f for f in result.findings if f.flag.id == "R5"]
    assert len(r5) == 0, "Negated arbitration should not trigger R5"


def test_non_negated_etf_still_triggers():
    text = "Customer shall pay an early termination fee equal to the remaining balance."
    result = scan(text)
    r3 = [f for f in result.findings if f.flag.id == "R3"]
    assert len(r3) == 1, "Non-negated ETF should trigger R3"


def test_double_negation_triggers():
    text = "This agreement is not without an early termination fee."
    result = scan(text)
    r3 = [f for f in result.findings if f.flag.id == "R3"]
    assert len(r3) == 1, "Double negation should still trigger R3"


def test_negation_does_not_affect_green_flags():
    text = "There is no change to the monthly rate of $44.99 per month."
    result = scan(text)
    g2 = [f for f in result.findings if f.flag.id == "G2"]
    assert len(g2) == 1, "GREEN flags should fire even when negated"


# --- New flag detection tests ---

def test_scan_general_red_flags(sample_contract):
    result = scan(sample_contract)
    general_red_ids = {f.flag.id for f in result.findings
                       if f.flag.id.startswith(("GR", "FR", "PD"))}
    for flag_id in ["GR1", "GR2", "GR3", "GR4", "GR5", "GR6",
                     "FR1", "FR2", "FR3", "FR4", "PD1", "PD2", "PD3"]:
        assert flag_id in general_red_ids, f"Should detect {flag_id}"


def test_scan_general_yellow_flags(sample_contract):
    result = scan(sample_contract)
    general_yellow_ids = {f.flag.id for f in result.findings
                          if f.flag.id.startswith(("GY", "RE"))}
    for flag_id in ["GY1", "GY2", "GY3", "GY4", "GY5", "GY6", "RE1", "RE2"]:
        assert flag_id in general_yellow_ids, f"Should detect {flag_id}"


def test_scan_general_green_flags(sample_contract):
    result = scan(sample_contract)
    green_ids = {f.flag.id for f in result.findings if f.flag.severity == Severity.GREEN}
    assert "GG1" in green_ids, "Should extract governing law"
    assert "GG2" in green_ids, "Should extract notice address"


def test_general_only_contract(sample_general):
    result = scan(sample_general)
    security_ids = {f.flag.id for f in result.findings
                    if f.flag.id in {"R1","R2","R3","R4","R5","R6","Y1","Y2","Y3","Y4","Y5","Y6"}}
    assert len(security_ids) == 0, f"General contract should not trigger security flags: {security_ids}"
    assert result.red_count > 0, "Should find general RED flags"


def test_negation_per_new_group():
    """Test negation for one flag per new group."""
    cases = [
        ("Company shall not modify terms unilaterally.", "GR1"),
        ("There is no non-disparagement requirement.", "GY1"),
        ("No compound late fees apply.", "FR1"),
        ("We never retain data indefinitely.", "PD1"),
        ("This agreement does not continue indefinitely.", "RE1"),
    ]
    for text, flag_id in cases:
        result = scan(text)
        found = [f for f in result.findings if f.flag.id == flag_id]
        assert len(found) == 0, f"Negated text should not trigger {flag_id}"
