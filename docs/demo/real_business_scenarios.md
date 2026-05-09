# Real Business Scenarios

## 1) Broker Asks Annual Limit
Scenario:
A broker needs quick annual-limit confirmation before sharing a quote.

Example query:
- classic3 limit

Expected behavior:
- Deterministic route to plan_core for Classic 3.
- Annual limit returned from validated plan data.
- Stable JSON envelope and business-safe message.

## 2) HR Asks Network
Scenario:
An HR representative asks which network the plan uses.

Example query:
- What is the network name for Classic 3?

Expected behavior:
- Deterministic route to plan_core.
- network_name returned with no internal metadata leakage.

## 3) Client Asks Coverage Area
Scenario:
A client asks where the plan is valid geographically.

Example queries:
- What is the area of coverage for Classic 3?
- What countries are covered by Classic 3?

Expected behavior:
- Deterministic route to plan_core.
- area_of_coverage returned from canonical data.

## 4) Shorthand Broker Wording
Scenario:
A broker uses compressed shorthand during a call.

Example queries:
- HN Classic 3 limit
- Classic 3 cashless?
- classic-3 limt

Expected behavior:
- Deterministic shorthand alias/keyword handling.
- Correct plan resolution to Classic 3.
- No probabilistic matching.

## 5) Arabic Usage
Scenario:
An Arabic-speaking broker asks key sales questions.

Example queries:
- ليمت كلاسيك 3
- شبكة كلاسيك 3
- هل كلاسيك 3 يحتاج referral؟

Expected behavior:
- Deterministic Arabic routing for supported plan-scoped prompts.
- Stable intent and plan resolution.

## 6) Mixed-Language Usage
Scenario:
A bilingual broker mixes Arabic and English in the same prompt.

Example queries:
- classic 3 الشبكة
- كلاسيك 3 coverage
- HN classic 3 ليمت

Expected behavior:
- Deterministic mixed-language routing for supported patterns.
- Correct plan resolution and stable output envelope.

## 7) Unsupported Protection
Scenario:
A user asks a plan-less shorthand or out-of-scope prompt.

Example queries:
- هل فيه direct billing؟
- هل يحتاج referral؟
- Tell me about Classic 4

Expected behavior:
- Safe deterministic unsupported response.
- No plan inference when plan is absent.
- No hallucinated values.

## 8) Demo Talking Point
The platform prioritizes safety and repeatability over over-broad interpretation. This keeps broker demos reliable and management outcomes auditable.
