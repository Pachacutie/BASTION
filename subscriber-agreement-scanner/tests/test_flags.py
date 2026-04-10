"""Tests for flag definitions."""

from bastion_scan.flags import (
    ALL_FLAGS, RED_FLAGS, YELLOW_FLAGS, GREEN_FLAGS,
    FLAG_BY_ID, Severity,
)


def test_flag_counts():
    assert len(RED_FLAGS) == 19
    assert len(YELLOW_FLAGS) == 14
    assert len(GREEN_FLAGS) == 6
    assert len(ALL_FLAGS) == 39


def test_all_flags_have_ids():
    ids = [f.id for f in ALL_FLAGS]
    assert len(ids) == len(set(ids))  # unique


def test_red_flag_ids():
    red_ids = {f.id for f in RED_FLAGS}
    expected = {"R1", "R2", "R3", "R4", "R5", "R6",
                "GR1", "GR2", "GR3", "GR4", "GR5", "GR6",
                "FR1", "FR2", "FR3", "FR4", "PD1", "PD2", "PD3"}
    assert red_ids == expected


def test_yellow_flag_ids():
    yellow_ids = {f.id for f in YELLOW_FLAGS}
    expected = {"Y1", "Y2", "Y3", "Y4", "Y5", "Y6",
                "GY1", "GY2", "GY3", "GY4", "GY5", "GY6", "RE1", "RE2"}
    assert yellow_ids == expected


def test_green_flag_ids():
    expected = {"G1", "G2", "G3", "G4", "GG1", "GG2"}
    assert {f.id for f in GREEN_FLAGS} == expected


def test_all_flags_have_names():
    for f in ALL_FLAGS:
        assert f.name, f"Flag {f.id} has no name"


def test_all_flags_have_descriptions():
    for f in ALL_FLAGS:
        assert f.description, f"Flag {f.id} has no description"


def test_red_yellow_have_actions():
    for f in RED_FLAGS + YELLOW_FLAGS:
        assert f.action, f"Flag {f.id} has no action text"


def test_flag_by_id_lookup():
    assert FLAG_BY_ID["R1"].name == "Auto-Renewal"
    assert FLAG_BY_ID["Y4"].name == "Waiver of Subrogation"
    assert FLAG_BY_ID["G2"].name == "Monthly Rate"


def test_severity_values():
    assert Severity.RED.value == "RED"
    assert Severity.YELLOW.value == "YELLOW"
    assert Severity.GREEN.value == "GREEN"
