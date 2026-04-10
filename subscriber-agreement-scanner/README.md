# BASTION Contract Scan

Detect predatory clauses in any contract. 39 flags across security, financial, privacy, and general consumer protection categories. Pattern-based detection of auto-renewal traps, excessive ETFs, forced arbitration, liability caps, data sharing, and more.

**Try it now:** [bastion-contract-scan.onrender.com](https://bastion-contract-scan.onrender.com)

Built on a decade of home security industry experience. Works on any consumer contract.

## Install

```bash
pip install bastion-contract-scan
```

Requires Python 3.12+.

## Usage

```bash
# Scan a PDF contract
bastion-contract-scan agreement.pdf

# Scan a text file
bastion-contract-scan contract.txt

# Pipe text from stdin
cat contract.txt | bastion-contract-scan

# Show matched trigger phrases and evidence
bastion-contract-scan --verbose agreement.pdf

# JSON output for programmatic use
bastion-contract-scan --json agreement.pdf > results.json

# Markdown output
bastion-contract-scan --md agreement.pdf > report.md

# No color (for piping)
bastion-contract-scan --no-color agreement.pdf
```

## What It Detects

### RED — High Severity

| Flag | Name | What It Means |
|------|------|---------------|
| R1 | Auto-Renewal | Contract renews for 12+ months automatically if you miss a narrow cancellation window |
| R2 | Short Cancellation Window | Must cancel 30-60+ days before renewal, often via certified mail |
| R3 | ETF = Remaining Balance | Early termination fee is 75-100% of remaining contract value |
| R4 | Liability Cap Under $1,000 | Provider pays at most $250-$1,000 if the system fails during a real event |
| R5 | Forced Arbitration | You cannot sue or join a class action |
| R6 | Data Sharing | Your alarm data and usage patterns shared with third parties |

### YELLOW — Medium Severity

| Flag | Name | What It Means |
|------|------|---------------|
| Y1 | Unilateral Rate Increase | Provider can raise your rate with 30 days notice |
| Y2 | Equipment Lease | You pay for equipment but never own it |
| Y3 | Monitoring Center Change | Your alerts may route to an unknown subcontractor |
| Y4 | Waiver of Subrogation | Your insurer can't go after the security company |
| Y5 | Written Cancel Only | Must send a physical letter — no phone, email, or online |
| Y6 | Installation Damage Waiver | Provider not liable for damage during installation |

### GREEN — Informational

| Flag | Name | What It Extracts |
|------|------|-----------------|
| G1 | Contract Term | Initial term length in months |
| G2 | Monthly Rate | Dollar amount per month |
| G3 | Equipment Ownership | Purchase vs. lease vs. free-with-contract |
| G4 | Permit Responsibility | Who obtains the alarm permit |

## How It Works

Pattern matching against extracted text. No AI, no cloud, no network calls. Your contract never leaves your machine.

Each flag has a set of trigger phrases — keywords and regex patterns drawn from real contract language across the home security industry. When a trigger matches, the scanner extracts the surrounding context as evidence.

## Output Formats

- **Terminal** (default): Colored report with severity sections and score
- **JSON** (`--json`): Structured data for programmatic consumption
- **Markdown** (`--md`): Formatted report for documentation

## Development

```bash
git clone https://github.com/Pachacutie/BASTION.git
cd BASTION/subscriber-agreement-scanner
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pytest
```

## License

MIT
