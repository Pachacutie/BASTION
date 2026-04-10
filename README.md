# BASTION

Open-source tools that help you understand what you're signing. Built on a decade of home security industry experience — but useful for any contract.

**Try it now:** [bastion-contract-scan.onrender.com](https://bastion-contract-scan.onrender.com) | [bastion-compat-check.onrender.com](https://bastion-compat-check.onrender.com) | [bastion-cost-engine.onrender.com](https://bastion-cost-engine.onrender.com)

---

## The Problem

The home security industry charges $40-50/month for a notification relay with a human call center. Sensors are binary switches. "Monitoring" is a person reading an alert and making a phone call. The contract exists to protect recurring revenue, not the customer.

But this isn't just a home security problem. Predatory contract patterns — auto-renewal traps, forced arbitration, liability caps, hidden fees — show up in every industry that depends on long-term contracts: telecom, gyms, SaaS, solar leases, rent-to-own, insurance.

BASTION makes every layer of that model transparent.

## Tools

### [BASTION Contract Scan](https://github.com/Pachacutie/bastion-contract-scan)

Upload any contract (PDF or text) and get a plain-English report on what's hiding in the fine print.

- **39 flags** across security, financial, privacy, and general consumer protection categories
- **Negation-aware** — "there is no early termination fee" won't trigger a false alarm
- **Readability scoring** — Flesch-Kincaid grade level shows when a contract is written to confuse you
- **Web UI** — drag-and-drop in your browser, no install required
- **CLI** — `bastion-contract-scan agreement.pdf` for power users
- **Local-first** — install locally and your contract never leaves your machine

[Use it online](https://bastion-contract-scan.onrender.com) | [Install locally](https://github.com/Pachacutie/bastion-contract-scan#install) | [Source](https://github.com/Pachacutie/bastion-contract-scan)

### [BASTION Device Compatibility Checker](https://github.com/Pachacutie/bastion-compat-check)

Check if your home security devices are compatible before you buy. Free, instant, no signup.

- **403 devices** across **45 manufacturers** with **79 compatibility overrides**
- **4 verdicts** — COMPATIBLE, INCOMPATIBLE, PARTIAL, UNKNOWN
- **Rules engine** — checks frequency match, protocol compatibility, known edge cases, and platform requirements
- **Single-device mode** — select one device to see everything compatible with it
- **Browsable device database** — filterable table of all devices
- **Local-first** — stateless API, no data stored

[Use it online](https://bastion-compat-check.onrender.com) | [Source](https://github.com/Pachacutie/bastion-compat-check)

### [BASTION Cost Engine](https://github.com/Pachacutie/bastion-cost-engine)

Find out what you're really paying for home security. True cost transparency — no sales pitch required.

- **7 providers** — Frontpoint, ADT, Ring, SimpliSafe, Vivint, Abode, Cove
- **Equipment builder** — select your devices and see provider markup vs. generic retail
- **True monthly cost** — exposes hidden fees not shown on pricing pages
- **3-year total cost of ownership** — equipment + monitoring + fees vs. DIY
- **ETF escape timeline** — shows when paying the early termination fee is cheaper than staying
- **Provider comparison** — all providers side-by-side with your equipment profile
- **Shareable URL** — every result is a permalink, no database needed
- **Local-first** — stateless, no data stored, no accounts

[Use it online](https://bastion-cost-engine.onrender.com) | [Source](https://github.com/Pachacutie/bastion-cost-engine)

---

## Philosophy

- **No cloud dependency.** Install locally and everything runs on your machine.
- **No accounts.** No signup, no login, no tracking.
- **No cost.** Free and open source. MIT license.
- **No fluff.** Each tool does one thing well. The report tells you what to do, not what to think.

## Contributing

Issues and pull requests welcome. If you've found predatory clauses we don't detect, [open an issue](https://github.com/Pachacutie/BASTION/issues).

## License

MIT
