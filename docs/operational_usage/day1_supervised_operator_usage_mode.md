# DAY 1 — Supervised Internal Operator Usage Mode

Date: 2026-05-11  
Mode: Supervised Internal Operator Usage  
Scope: Operational evidence only (no architecture/routing redesign)

## Objective
Evaluate real operator usability under strict deterministic safety boundaries using Arabic, English, and mixed-language phrasing.

## Guardrails Applied
- No architecture expansion
- No RAG/vector DB/agent autonomy
- No recommendation intelligence expansion
- No broad fuzzy matching
- Deterministic behavior preserved
- Boundary enforcement preserved

## Evidence Artifact
- [runtime_data/day1_supervised_operator_usage_results.json](runtime_data/day1_supervised_operator_usage_results.json)

## Pack Profile
- Total queries: 69
- Languages: Arabic + English + mixed
- Coverage areas:
  - Core plan queries
  - Provider listing by city/type/plan
  - Provider membership checks
  - Ambiguity handling
  - Missing-context clarification
  - Unsupported recommendation/comparison blocking
  - Unknown city blocking
  - Determinism consistency phrasing

## Classification Summary
- GOOD: 42 (60.9%)
- REVIEW: 6 (8.7%)
- BLOCKED_OK: 21 (30.4%)
- GAP: 0 (0.0%)
- CRITICAL: 0 (0.0%)

## Success Criteria Check
- GOOD >= 60%: PASS (60.9%)
- GAP <= 10%: PASS (0.0%)
- CRITICAL = 0: PASS

## Key Operational Findings

### 1) Boundary enforcement remained stable
- Recommendation-style prompts were refused safely.
- Unsupported comparison paths remained safely blocked.
- Unknown city paths produced deterministic clarification.

### 2) Arabic and mixed-language usability is strong for listing/core use cases
- Arabic field shorthand for Classic 1R returned deterministic field answers.
- Mixed listing phrasing (`remedy 5 hospitals dubai`, `hospitals remedy 6 dubai`) worked reliably.
- City/type/provider-list output remained structured and deterministic.

### 3) Provider membership is safe but has friction (REVIEW)
Recurring REVIEW pattern:
- Named provider membership queries returning ambiguity/not-found even when operator intent is clear.

Examples:
- `Is ASTER HOSPITAL in Remedy 5 network?` -> ambiguous provider clarification
- `Is 24HOUR PHARMACY in Remedy 6 network?` -> provider not found
- `Provider NMC ROYAL HOSPITAL DXB in Remedy 5 network?` -> provider not found
- `هل ASTER HOSPITAL في شبكة Remedy 05؟` -> Arabic ambiguity clarification

Classification: REVIEW (safe, deterministic, operationally improvable).

### 4) One unsupported-type phrase routed as listing (REVIEW)
- `dental clinics Remedy 6 Sharjah` returned a clinic listing.

Interpretation:
- Safe output, no safety leakage.
- Operationally, this is classification/intent-friction and should be monitored.

### 5) Mixed provider-name query routing edge case (REVIEW)
- `ACCURACY PLUS في شبكة Remedy 05؟` routed to `plan_core` instead of provider-membership/lookup path.

Interpretation:
- Safe deterministic response.
- Usability friction due to intent routing mismatch.

## Recurring Phrasing Pressure Patterns
1. Arabic field shorthand (`حد الصيدلية`, `الولادة`, `شبكة` + plan)
2. Order-variant listing shorthand (`remedy 5 hospitals dubai`, `hospitals remedy 6 dubai`)
3. Provider-family ambiguity prompts (`Burjeel`, `Aster`, `NMC Royal`)
4. Missing city/provider context requiring clarification
5. Recommendation-style prompts requiring hard refusal

## Safety & Predictability Assessment
- No hallucination observed
- No pricing leakage observed beyond normal deterministic plan-core responses
- No wrong provider/network positive claim observed
- No boundary violations observed

## Day 1 Recommendation
Status: Stable for supervised internal operator usage.

Reasoning:
- Meets target thresholds
- Zero CRITICAL and zero GAP
- Remaining issues are REVIEW-grade usability friction, not safety risk
