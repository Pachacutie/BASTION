"""Trigger phrase registry and regex patterns for each red flag."""

from __future__ import annotations

import re

# Each flag ID maps to a list of compiled regex patterns.
# Patterns are case-insensitive. Each pattern should match a phrase that
# indicates the presence of the corresponding clause.

_RAW_PATTERNS: dict[str, list[str]] = {
    # ── RED ───────────────────────────────────────────────────────────────
    "R1": [
        r"automatically\s+renew",
        r"shall\s+renew",
        r"will\s+renew",
        r"auto[\s-]?renew",
        r"renewal\s+term",
        r"successive\s+period",
        r"unless\s+(canceled|cancelled|terminated)",
        r"renew\s+for\s+(an\s+)?additional",
        r"renewal\s+period",
        r"extended\s+for\s+(a\s+)?successive",
    ],
    "R2": [
        r"\d+\s*days?\s*(prior|before|in\s+advance)",
        r"written\s+notice\s+of\s+cancellation",
        r"notice\s+of\s+(cancellation|termination)",
        r"certified\s+mail",
        r"registered\s+mail",
        r"days['\u2019]?\s*notice",
        r"cancellation\s+must\s+be\s+(received|sent)",
        r"cancel.{0,30}(writing|written)",
        r"notice.{0,20}no\s+fewer\s+than",
        r"notice.{0,20}no\s+less\s+than",
    ],
    "R3": [
        r"early\s+termination\s+fee",
        r"cancellation\s+fee",
        r"termination\s+charge",
        r"remaining\s+balance",
        r"remaining\s+(months|payments)",
        r"liquidated\s+damages",
        r"(75|80|90|100)\s*%\s*(of\s+)?(the\s+)?remaining",
        r"sum\s+of\s+(all\s+)?remaining\s+(monthly\s+)?payments",
        r"pay.{0,30}remainder\s+of\s+(the\s+)?(contract|agreement|term)",
        r"early\s+cancellation\s+penalty",
    ],
    "R4": [
        r"liability\s+shall\s+not\s+exceed",
        r"maximum\s+liability",
        r"aggregate\s+liability",
        r"limited\s+to\s+\$",
        r"not\s+exceed\s+\$",
        r"total\s+liability.{0,30}\$\s*\d",
        r"liability.{0,30}(shall|will)\s+not\s+exceed",
        r"damages.{0,30}limited\s+to",
        r"\$\s*(250|500|750|1,?000)\b",
        r"in\s+no\s+event.{0,30}(liability|liable|damages)",
    ],
    "R5": [
        r"binding\s+arbitration",
        r"waive.{0,30}class\s+action",
        r"arbitration\s+agreement",
        r"\bAAA\b",
        r"\bJAMS\b",
        r"individual\s+basis",
        r"class\s+action\s+waiver",
        r"waive.{0,30}(right\s+to\s+)?(jury\s+)?trial",
        r"dispute.{0,30}(resolved|settled).{0,30}arbitration",
        r"agree\s+to\s+arbitrat",
        r"mandatory\s+arbitration",
    ],
    "R6": [
        r"share.{0,30}(information|data).{0,30}(third|3rd)\s*[\s-]?part",
        r"(third|3rd)\s*[\s-]?part.{0,30}(share|disclose|transfer|provide)",
        r"affiliates",
        r"marketing\s+(purpose|partner|use)",
        r"data.{0,30}transfer",
        r"disclose.{0,30}(personal|customer|subscriber)\s+(information|data)",
        r"share.{0,30}(partner|vendor|advertis)",
        r"(sell|rent|trade).{0,30}(personal|customer)\s+(information|data)",
        r"may\s+(share|disclose|provide).{0,30}information",
    ],
    # ── YELLOW ────────────────────────────────────────────────────────────
    "Y1": [
        r"(increase|raise|adjust).{0,30}(rate|price|fee|charge)",
        r"rate\s+(increase|adjustment|change)",
        r"(right|reserve).{0,30}(increase|modify|change).{0,30}(rate|price|fee)",
        r"continued\s+use.{0,30}(constitutes|means|indicates)\s+acceptance",
        r"30\s*days?\s*notice.{0,30}(rate|price|fee)",
        r"price.{0,30}subject\s+to\s+change",
    ],
    "Y2": [
        r"equipment.{0,30}(lease|leased|rental|rented)",
        r"(lease|rent).{0,30}equipment",
        r"does\s+not\s+own.{0,30}equipment",
        r"equipment.{0,30}(property\s+of|belongs\s+to|owned\s+by).{0,30}(provider|company)",
        r"return.{0,30}equipment.{0,30}(cancel|terminat)",
        r"(must|shall|agree\s+to)\s+return.{0,30}equipment",
        r"equipment.{0,30}remain.{0,30}property",
    ],
    "Y3": [
        r"(delegate|assign|transfer|subcontract).{0,30}monitor",
        r"third[\s-]?party.{0,30}(monitoring|central\s+station)",
        r"(change|substitute|replace).{0,30}(monitoring|central\s+station)",
        r"monitoring.{0,30}(outsource|subcontract)",
        r"central\s+station.{0,30}(discretion|choice|option)",
        r"reserve.{0,30}right.{0,30}(change|assign).{0,30}monitor",
    ],
    "Y4": [
        r"waiver\s+of\s+subrogation",
        r"waive.{0,30}subrogation",
        r"subrogation.{0,30}waiv",
        r"(insurer|insurance).{0,30}(waive|relinquish|give\s+up).{0,30}(right|claim)",
        r"(waive|relinquish).{0,30}(right|claim).{0,30}(insurer|insurance)",
    ],
    "Y5": [
        r"cancel.{0,30}(writing|written\s+notice|letter)",
        r"(written|physical).{0,30}(notice|letter).{0,30}cancel",
        r"certified\s+mail.{0,30}cancel",
        r"cancel.{0,30}certified\s+mail",
        r"(no|not).{0,30}(phone|email|online|electronic).{0,30}cancel",
        r"cancellation.{0,30}(must|shall).{0,30}(writing|written|mail)",
    ],
    "Y6": [
        r"(not|no)\s+(liable|liability|responsible|responsibility).{0,30}(install|damage)",
        r"installation.{0,30}damage.{0,30}(waive|not\s+liable)",
        r"damage.{0,30}(during|caused\s+by|resulting\s+from).{0,30}install",
        r"waive.{0,30}(claim|right).{0,30}install.{0,30}damage",
        r"hold\s+harmless.{0,30}install",
    ],
    # ── GENERAL RED ───────────────────────────────────────────────────────
    "GR1": [
        r"(may|right\s+to)\s+(modify|amend|change).{0,30}(terms|agreement|conditions)",
        r"(changes?|modifications?)\s+(effective|binding)\s+(upon|when)\s+(posting|notice)",
        r"right\s+to\s+amend",
        r"(modify|change|alter).{0,20}(terms|conditions).{0,20}(at\s+any\s+time|without\s+consent)",
        r"(sole|absolute)\s+discretion.{0,20}(modify|change|amend)",
        r"reserves?\s+(the\s+)?right\s+to\s+(update|revise|modify)",
    ],
    "GR2": [
        r"confess.{0,20}judgment",
        r"cognovit",
        r"authorize.{0,20}entry\s+of\s+judgment",
        r"consent.{0,20}judgment.{0,20}(against|entered)",
        r"waive.{0,20}right.{0,20}(defend|notice).{0,20}(judgment|court)",
    ],
    "GR3": [
        r"(trial|free\s+period).{0,30}(convert|transition|change).{0,20}(paid|subscription|billing)",
        r"automatically\s+(charged|billed|enrolled)",
        r"unless\s+(you\s+)?cancel\s+before",
        r"(free|trial).{0,20}(auto|automatic).{0,20}(renew|charge|bill|convert)",
        r"begin\s+billing.{0,20}(after|following|upon).{0,20}trial",
    ],
    "GR4": [
        r"personal(ly)?\s+(liable|guarantee|responsibility)",
        r"individual\s+capacity",
        r"personal\s+guarantee",
        r"(jointly|personally).{0,20}(and\s+severally\s+)?(liable|responsible)",
        r"guarantee.{0,20}(personal|individual).{0,20}(assets|property|funds)",
    ],
    "GR5": [
        r"(fee|charge|penalty|cost).{0,30}(disput|complain|request|exercis)",
        r"(administrative|processing)\s+(fee|charge).{0,20}(dispute|complaint|request)",
        r"(charge|fee).{0,20}(data\s+)?request",
        r"(penalt|fee|surcharge).{0,20}(filing|submitting).{0,20}(complaint|dispute|grievance)",
    ],
    "GR6": [
        r"increase.{0,20}(CPI|consumer\s+price\s+index)",
        r"adjusted\s+annually",
        r"(escalat|increase).{0,20}(\d+\.?\d*)\s*%\s*(per|each|every)\s*(year|annum)",
        r"(annual|yearly)\s+(increase|escalation|adjustment)",
        r"(rate|price|fee).{0,20}(increase|adjust).{0,20}(each|every|per)\s*(year|annum)",
        r"cost.of.living\s+(adjustment|increase)",
    ],
    # ── GENERAL YELLOW ────────────────────────────────────────────────────────
    "GY1": [
        r"(shall\s+)?not\s+disparage",
        r"(negative|unfavorable|derogatory)\s+(review|comment|statement|remark)",
        r"refrain\s+from\s+(making|publishing|posting).{0,20}(statement|comment|review)",
        r"non.disparagement",
        r"(agree|covenant).{0,20}not.{0,20}(criticize|disparage|defame)",
    ],
    "GY2": [
        r"indemnify.{0,20}hold\s+harmless",
        r"defend.{0,20}at\s+(your|customer|subscriber).{0,10}(expense|cost)",
        r"(bear|pay|assume)\s+(all|any)\s+(costs?|expenses?|fees?).{0,20}(defense|litigation|legal)",
        r"(indemnif|hold\s+harmless).{0,20}(against|from)\s+(any|all)\s+(claims?|losses?|damages?)",
    ],
    "GY3": [
        r"assign.{0,30}(agreement|contract|rights?).{0,20}without.{0,20}(your\s+)?(consent|approval|notice)",
        r"transfer.{0,20}(rights?|obligations?).{0,20}without\s+(notice|consent)",
        r"(may|right\s+to)\s+assign.{0,20}(without|at\s+any\s+time)",
        r"(assign|transfer|delegate).{0,20}(to\s+)?(any\s+)?(third\s+party|affiliate|successor)",
    ],
    "GY4": [
        r"exclusive\s+jurisdiction.{0,20}(court|state|county)",
        r"venue\s+shall\s+be",
        r"forum\s+selection",
        r"(disputes?|actions?|proceedings?).{0,20}(brought|filed|commenced).{0,20}(in|at)\s+(the\s+)?(courts?\s+of|state\s+of)",
        r"(consent|submit|agree)\s+to\s+(the\s+)?(exclusive\s+)?(jurisdiction|venue)",
    ],
    "GY5": [
        r"(no|waive|disclaim).{0,20}consequential\s+damages",
        r"(indirect|incidental|special|punitive)\s+damages?\s+(excluded|waived|disclaimed)",
        r"(not|never)\s+(be\s+)?(liable|responsible)\s+for.{0,20}(indirect|consequential|incidental)",
        r"(lost\s+profits?|lost\s+revenue).{0,20}(excluded|waived|not\s+recoverable)",
    ],
    "GY6": [
        r"consent\s+to\s+(receive|be\s+contacted)",
        r"autodialed",
        r"(agree|consent).{0,20}(marketing|promotional|commercial).{0,20}(call|text|email|message|communication)",
        r"(opt.in|agree).{0,20}(receive|accept).{0,20}(marketing|promotional|advertisement)",
        r"(robocall|auto.?dial|pre.?record)",
    ],
    # ── FINANCIAL RED ─────────────────────────────────────────────────────────
    "FR1": [
        r"(compound|additional).{0,20}(late|overdue)\s+(fee|charge|penalty)",
        r"late\s+(fee|charge).{0,20}(on|upon|for).{0,20}(unpaid|outstanding)\s+(fee|charge|balance)",
        r"(fee|charge).{0,20}(assessed|applied).{0,20}(on|to).{0,20}(unpaid|overdue)\s+(fee|charge)",
        r"(interest|fee).{0,20}(compound|accrue).{0,20}(unpaid|outstanding)",
    ],
    "FR2": [
        r"cross.default",
        r"default\s+under\s+(any\s+)?other\s+(agreement|contract|obligation)",
        r"(default|breach).{0,20}(trigger|constitute).{0,20}default.{0,20}(all|other|any)",
        r"(event\s+of\s+)?default.{0,20}(under|on)\s+(any|all)\s+(other|related)",
    ],
    "FR3": [
        r"(entire|full|total)\s+(remaining\s+)?(balance|amount).{0,20}(due|payable)\s+(immediately|at\s+once)",
        r"accelerat.{0,20}(all\s+)?(payment|balance|obligation|amount)",
        r"(all|entire)\s+(remaining\s+)?(payment|installment).{0,20}(become|due)\s+immediately",
        r"(declare|make).{0,20}(entire|full|total).{0,20}(balance|amount).{0,20}(due|payable)",
    ],
    "FR4": [
        r"variable\s+rate",
        r"rate.{0,20}(may\s+)?(increase|change).{0,20}without\s+(limit|cap|ceiling|maximum)",
        r"no\s+(maximum|cap|ceiling|upper\s+limit).{0,20}(rate|interest|charge)",
        r"(unlimited|uncapped).{0,20}(rate|interest)\s+(increase|adjustment)",
    ],
    # ── PRIVACY ───────────────────────────────────────────────────────────────
    "PD1": [
        r"(perpetual|irrevocable|permanent).{0,20}(license|right|grant).{0,20}(data|content|information)",
        r"retain.{0,20}(data|information|content).{0,20}indefinitely",
        r"(data|information).{0,20}(rights?|license).{0,20}(survive|continue|persist).{0,20}(termination|cancellation|expiration)",
        r"(irrevocable|perpetual|worldwide).{0,20}(right|license).{0,20}(use|access|retain)",
    ],
    "PD2": [
        r"biometric\s+(data|information|identifier)",
        r"facial\s+recognition",
        r"(location|geo.?location)\s+(tracking|data|monitoring|information)",
        r"(fingerprint|voiceprint|retina|iris)\s+(scan|data|recognition)",
        r"(behavioral|movement)\s+(tracking|monitoring|pattern)",
    ],
    "PD3": [
        r"(cannot|no\s+right|unable).{0,20}(request|demand|require).{0,20}delet",
        r"no\s+obligation\s+to\s+delete",
        r"(data|information).{0,20}(retained|stored|kept).{0,20}(at\s+)?(our|provider|company).{0,10}(discretion|option)",
        r"(not\s+required|no\s+obligation).{0,20}(erase|remove|purge|delete)",
    ],
    # ── RENEWAL/EXIT ──────────────────────────────────────────────────────────
    "RE1": [
        r"(continues?|remains?).{0,20}(in\s+)?(effect|force).{0,20}until\s+(cancel|terminat)",
        r"no\s+(expiration|end\s+date|termination\s+date)",
        r"perpetual\s+term",
        r"indefinite.{0,10}(term|period|duration)",
        r"(agreement|contract).{0,20}(has\s+)?no\s+(fixed|set|definite)\s+(term|end|expiration)",
    ],
    "RE2": [
        r"survives?\s+(the\s+)?(termination|expiration|cancellation|end)",
        r"obligations?\s+(shall\s+)?(continue|remain|persist).{0,20}after.{0,20}(termination|expiration|cancellation)",
        r"non.compete",
        r"non.solicit",
        r"(covenant|restriction).{0,20}(survives?|continues?|remains?).{0,20}(after|beyond|following)",
        r"(intellectual\s+property|IP).{0,20}(assignment|transfer).{0,20}survives?",
    ],
    # ── GENERAL GREEN ─────────────────────────────────────────────────────────
    "GG1": [
        r"govern.{0,10}(by|under|in\s+accordance\s+with)\s+(the\s+)?(laws?\s+of)\s+(the\s+)?(state\s+of\s+)?(\w+)",
        r"(laws?\s+of\s+the\s+state\s+of|laws?\s+of)\s+(\w+)",
        r"(construed|interpreted).{0,20}(in\s+accordance\s+with|under|pursuant\s+to).{0,20}(laws?\s+of)",
    ],
    "GG2": [
        r"(notice|notices).{0,40}(sent|mailed|delivered|addressed)\s+to.{0,80}(street|ave|blvd|road|drive|suite|p\.?o\.?\s*box|floor)",
        r"(notice|correspondence).{0,20}(address|shall\s+be\s+sent).{0,80}\d{5}",
        r"(send|mail|deliver).{0,20}(notice|correspondence).{0,20}(to|at).{0,80}\d{5}",
    ],
    # ── GREEN (value extraction patterns) ─────────────────────────────────
    "G1": [
        r"(?:initial|original|minimum)\s+(?:term|period).{0,40}(?:\((\d+)\)|(\d+))\s*(month|year)",
        r"(?:\((\d+)\)|(\d+))\s*[\s-]?(?:month|year)\s*(?:term|contract|agreement|period)",
        r"term\s+of\s+.{0,20}(?:\((\d+)\)|(\d+))\s*(?:month|year)",
        r"period\s+of\s+.{0,20}(?:\((\d+)\)|(\d+))\s*(?:month|year)",
    ],
    "G2": [
        r"\$\s*(\d+\.?\d*)\s*(?:per|/|a)\s*month",
        r"monthly.{0,20}\$\s*(\d+\.?\d*)",
        r"\$\s*(\d+\.?\d*)\s*(?:per|/)?\s*(?:mo|month)",
        r"monitoring.{0,20}\$\s*(\d+\.?\d*)",
    ],
    "G3": [
        r"equipment.{0,60}(purchase|purchased|own|owned|buy|bought)",
        r"equipment.{0,60}(lease|leased|rental|rented)",
        r"(free|no[\s-]?cost).{0,40}equipment",
        r"equipment.{0,40}(free|no[\s-]?cost|included)",
        r"(purchase|lease|rent).{0,40}(the\s+)?equipment",
    ],
    "G4": [
        r"(customer|subscriber|you).{0,30}(responsible|obligation).{0,30}(permit|license)",
        r"(alarm\s+)?permit.{0,30}(customer|subscriber|your)\s+(responsibility|obligation)",
        r"(obtain|secure|acquire).{0,30}(alarm\s+)?permit",
        r"permit.{0,30}(required|necessary|needed)",
    ],
}

# Compile all patterns (case-insensitive)
PATTERNS: dict[str, list[re.Pattern]] = {
    flag_id: [re.compile(p, re.IGNORECASE) for p in patterns]
    for flag_id, patterns in _RAW_PATTERNS.items()
}
