"""Red flag definitions — severity, descriptions, and consumer actions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


@dataclass(frozen=True)
class FlagDef:
    id: str
    name: str
    severity: Severity
    description: str
    action: str


# ── RED FLAGS ────────────────────────────────────────────────────────────────

R1 = FlagDef(
    id="R1",
    name="Auto-Renewal",
    severity=Severity.RED,
    description="Contract renews for 12+ months automatically if not canceled in a narrow window.",
    action="Mark your calendar 31+ days before renewal.",
)

R2 = FlagDef(
    id="R2",
    name="Short Cancellation Window",
    severity=Severity.RED,
    description="Must cancel 30-60+ days before renewal date, in writing, often via certified mail.",
    action="Note the exact cancellation deadline and method required.",
)

R3 = FlagDef(
    id="R3",
    name="ETF = Remaining Balance",
    severity=Severity.RED,
    description="Early termination fee calculated as total remaining contract value.",
    action="Calculate your exposure before signing.",
)

R4 = FlagDef(
    id="R4",
    name="Liability Cap Under $1,000",
    severity=Severity.RED,
    description="Provider limits liability to $250-$1,000 regardless of actual loss.",
    action="Understand the maximum the provider will pay if the system fails.",
)

R5 = FlagDef(
    id="R5",
    name="Forced Arbitration",
    severity=Severity.RED,
    description="Disputes resolved through binding arbitration, class action waiver.",
    action="You cannot sue or join a class action.",
)

R6 = FlagDef(
    id="R6",
    name="Data Sharing",
    severity=Severity.RED,
    description="Provider may share alarm data, usage patterns, or personal info with third parties.",
    action="Review what data is shared and with whom.",
)

# ── YELLOW FLAGS ─────────────────────────────────────────────────────────────

Y1 = FlagDef(
    id="Y1",
    name="Unilateral Rate Increase",
    severity=Severity.YELLOW,
    description="Provider may increase monthly rate with 30 days notice, continued use = acceptance.",
    action="Watch for rate increase notices.",
)

Y2 = FlagDef(
    id="Y2",
    name="Equipment Lease",
    severity=Severity.YELLOW,
    description="Customer pays for equipment but does not own it — must return at cancellation.",
    action="Clarify whether you own the equipment.",
)

Y3 = FlagDef(
    id="Y3",
    name="Monitoring Center Change",
    severity=Severity.YELLOW,
    description="Provider reserves right to delegate monitoring to any third-party central station.",
    action="Ask which monitoring center handles your alerts.",
)

Y4 = FlagDef(
    id="Y4",
    name="Waiver of Subrogation",
    severity=Severity.YELLOW,
    description="Customer waives right for their insurance company to recover costs from the provider.",
    action="Your insurer cannot pursue the security company if the system fails.",
)

Y5 = FlagDef(
    id="Y5",
    name="Written Cancel Only",
    severity=Severity.YELLOW,
    description="No phone, no email, no online — must send a physical letter or certified mail.",
    action="Plan to send cancellation via certified mail with tracking.",
)

Y6 = FlagDef(
    id="Y6",
    name="Installation Damage Waiver",
    severity=Severity.YELLOW,
    description="Customer agrees provider is not liable for damage during installation.",
    action="Document your home's condition before installation.",
)

# ── GREEN (INFORMATIONAL) ───────────────────────────────────────────────────

G1 = FlagDef(
    id="G1",
    name="Contract Term",
    severity=Severity.GREEN,
    description="Initial contract term length in months.",
    action="",
)

G2 = FlagDef(
    id="G2",
    name="Monthly Rate",
    severity=Severity.GREEN,
    description="The monthly monitoring rate.",
    action="",
)

G3 = FlagDef(
    id="G3",
    name="Equipment Ownership",
    severity=Severity.GREEN,
    description="Purchase vs. lease vs. free-with-contract.",
    action="",
)

G4 = FlagDef(
    id="G4",
    name="Permit Responsibility",
    severity=Severity.GREEN,
    description="Who is responsible for obtaining the alarm permit.",
    action="",
)

# ── GENERAL RED ──────────────────────────────────────────────────────────────

GR1 = FlagDef(
    id="GR1",
    name="Unilateral Contract Modification",
    severity=Severity.RED,
    description="Provider may modify terms at any time without consent.",
    action="Review how and when terms can change.",
)

GR2 = FlagDef(
    id="GR2",
    name="Confession of Judgment",
    severity=Severity.RED,
    description="Customer authorizes entry of judgment against them.",
    action="This waives your right to defend yourself in court.",
)

GR3 = FlagDef(
    id="GR3",
    name="Auto-Charge After Trial",
    severity=Severity.RED,
    description="Free trial converts to paid subscription automatically.",
    action="Set a reminder before the trial ends.",
)

GR4 = FlagDef(
    id="GR4",
    name="Personal Guarantee",
    severity=Severity.RED,
    description="Customer is personally liable beyond the service agreement.",
    action="Understand your personal financial exposure.",
)

GR5 = FlagDef(
    id="GR5",
    name="Penalty for Exercising Rights",
    severity=Severity.RED,
    description="Fees for disputing charges, requesting data, or filing complaints.",
    action="Know the cost of exercising your consumer rights.",
)

GR6 = FlagDef(
    id="GR6",
    name="Automatic Price Escalation",
    severity=Severity.RED,
    description="Locked-in annual price increases tied to CPI or fixed percentages.",
    action="Calculate your total cost over the contract term.",
)

# ── GENERAL YELLOW ────────────────────────────────────────────────────────────

GY1 = FlagDef(
    id="GY1",
    name="Non-Disparagement",
    severity=Severity.YELLOW,
    description="Customer may not leave negative reviews or public criticism.",
    action="Understand what you can and cannot say publicly.",
)

GY2 = FlagDef(
    id="GY2",
    name="Broad Indemnification",
    severity=Severity.YELLOW,
    description="Customer must pay provider's legal costs in disputes.",
    action="Assess your potential legal cost exposure.",
)

GY3 = FlagDef(
    id="GY3",
    name="Assignment Without Consent",
    severity=Severity.YELLOW,
    description="Provider can sell or transfer your contract without notice.",
    action="Your service may change hands without your approval.",
)

GY4 = FlagDef(
    id="GY4",
    name="Choice of Venue",
    severity=Severity.YELLOW,
    description="Disputes must be filed in provider's home jurisdiction.",
    action="Check the travel and cost implications of this venue.",
)

GY5 = FlagDef(
    id="GY5",
    name="Consequential Damages Waiver",
    severity=Severity.YELLOW,
    description="Cannot claim lost wages, opportunity costs, or indirect damages.",
    action="Understand the limits on what you can recover.",
)

GY6 = FlagDef(
    id="GY6",
    name="Consent to Communications",
    severity=Severity.YELLOW,
    description="Buried opt-in to marketing calls, texts, or emails.",
    action="Review what communications you're agreeing to receive.",
)

# ── FINANCIAL RED ─────────────────────────────────────────────────────────────

FR1 = FlagDef(
    id="FR1",
    name="Compound Late Fees",
    severity=Severity.RED,
    description="Late fees generate additional fees on themselves.",
    action="Understand how quickly fees can escalate.",
)

FR2 = FlagDef(
    id="FR2",
    name="Cross-Default",
    severity=Severity.RED,
    description="Default on one account triggers default on all accounts with provider.",
    action="Check if this affects other agreements you hold.",
)

FR3 = FlagDef(
    id="FR3",
    name="Acceleration Clause",
    severity=Severity.RED,
    description="Miss one payment and the entire remaining balance becomes due immediately.",
    action="Understand your exposure from a single missed payment.",
)

FR4 = FlagDef(
    id="FR4",
    name="Variable Rate Without Cap",
    severity=Severity.RED,
    description="Rate can increase indefinitely with no ceiling.",
    action="Ask what the maximum possible rate is.",
)

# ── PRIVACY RED ───────────────────────────────────────────────────────────────

PD1 = FlagDef(
    id="PD1",
    name="Perpetual Data License",
    severity=Severity.RED,
    description="Provider keeps rights to your data forever, even after cancellation.",
    action="Review what data rights survive cancellation.",
)

PD2 = FlagDef(
    id="PD2",
    name="Biometric/Location Consent",
    severity=Severity.RED,
    description="Buried consent for fingerprint, face, GPS, or behavioral tracking.",
    action="Review what personal data is being collected.",
)

PD3 = FlagDef(
    id="PD3",
    name="No Data Deletion Right",
    severity=Severity.RED,
    description="No mechanism to request your data be deleted.",
    action="Ask about data deletion procedures.",
)

# ── RENEWAL/EXIT YELLOW ───────────────────────────────────────────────────────

RE1 = FlagDef(
    id="RE1",
    name="Evergreen Clause",
    severity=Severity.YELLOW,
    description="Contract has no end date, continues until actively canceled.",
    action="Set a recurring reminder to review this agreement.",
)

RE2 = FlagDef(
    id="RE2",
    name="Post-Termination Obligations",
    severity=Severity.YELLOW,
    description="Obligations continue after contract ends (non-compete, non-solicit, IP).",
    action="Review what obligations survive after you leave.",
)

# ── GENERAL GREEN ─────────────────────────────────────────────────────────────

GG1 = FlagDef(
    id="GG1",
    name="Governing Law",
    severity=Severity.GREEN,
    description="Which state's law governs the contract.",
    action="",
)

GG2 = FlagDef(
    id="GG2",
    name="Notice Address",
    severity=Severity.GREEN,
    description="Where to send formal notices.",
    action="",
)

# ── REGISTRY ─────────────────────────────────────────────────────────────────

ALL_FLAGS: list[FlagDef] = [
    R1, R2, R3, R4, R5, R6, Y1, Y2, Y3, Y4, Y5, Y6, G1, G2, G3, G4,
    GR1, GR2, GR3, GR4, GR5, GR6, GY1, GY2, GY3, GY4, GY5, GY6,
    FR1, FR2, FR3, FR4, PD1, PD2, PD3, RE1, RE2, GG1, GG2,
]
RED_FLAGS = [f for f in ALL_FLAGS if f.severity == Severity.RED]
YELLOW_FLAGS = [f for f in ALL_FLAGS if f.severity == Severity.YELLOW]
GREEN_FLAGS = [f for f in ALL_FLAGS if f.severity == Severity.GREEN]
FLAG_BY_ID = {f.id: f for f in ALL_FLAGS}
