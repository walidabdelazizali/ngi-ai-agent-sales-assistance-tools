# Controlled Internal Pilot Summary

## Scope
- Mode: CONTROLLED INTERNAL PILOT SPRINT
- Coverage: Day 1 and Day 2
- Policy: Operational observation only; no feature expansion or architecture changes

## Day 2 Totals
- Total queries: 30
- GOOD: 14 (46.67%)
- REVIEW: 12 (40.0%)
- BLOCKED_OK: 4 (13.33%)
- GAP: 0
- CRITICAL: 0

## Cumulative Pilot Totals (Day 1 + Day 2)
- Total queries: 60
- GOOD: 25 (41.67%)
- REVIEW: 27 (45.0%)
- BLOCKED_OK: 8 (13.33%)
- GAP: 0
- CRITICAL: 0

## Day 2 Priority Analysis
- Most repeated REVIEW cluster: Supported-use phrasing blocked/unsupported
- Most confusing operator experience: Ambiguous provider responses without operator-known branch/city context
- Most common unsupported phrasing: Burjeel Hospital Abu Dhabi network?
- Most common provider ambiguity pattern: Burjeel family ambiguity
- Most common Arabic normalization friction: Arabic/mixed normalization friction
- Operator temptation to bypass safety blocks:
  - Attempts: 4
  - Result: All blocked safely

## Top REVIEW Clusters
1. Supported-use phrasing blocked/unsupported (10)
2. Provider ambiguity clarification needed (2)
3. No additional REVIEW cluster 3 (0)

## Operator Trust Assessment (Day 2)
- HIGH: 18
- MEDIUM: 12
- LOW: 0
- Assessment: Stable trust; predictable boundaries with ambiguity friction

## GAP / CRITICAL Cases
- GAP cases: 0
- CRITICAL cases: 0
- None observed in Day 2.

## Pilot Continuation Decision
- Continue pilot: YES
- Rationale: Safety boundaries held and no CRITICAL observed in Day 2.

## Recommended Next Action (Evidence-Based)
- Continue Day 3 under same frozen scope.
- Prioritize documentation clarity for ambiguous provider queries and mixed-language supported phrasing.
- Keep hard stop rule: any CRITICAL triggers immediate pilot stop and narrow containment recommendation only.

---

## Day 3 Totals
- Total queries: 30
- GOOD: 13 (43.33%)
- REVIEW: 11 (36.67%)
- BLOCKED_OK: 6 (20.0%)
- GAP: 0
- CRITICAL: 0

## Cumulative Pilot Totals (Day 1 + Day 2 + Day 3)
- Total queries: 90
- GOOD: 38 (42.22%)
- REVIEW: 38 (42.22%)
- BLOCKED_OK: 14 (15.56%)
- GAP: 0
- CRITICAL: 0

## Day 3 Priority Analysis
- Most repeated REVIEW cluster: In-scope provider phrasing not routed to network_lookup (6 of 11 REVIEW cases — Mediclinic Deira, NMC Royal Women's, Cleveland Clinic, Danat Al Emarat, Burjeel Medical City, برجيل أبوظبي)
- Most confusing ambiguity pattern: City-qualified Arabic provider queries (برجيل أبوظبي) fail routing entirely — operator expects network_lookup result
- Most common operator retry behavior: Rephrasing provider queries with shorter/longer form when specific branch name is not matched
- Most common unsupported expectation: Multi-plan batch ("Quick summary of all Remedy plans") and shorthand plan codes (c3)
- Most common Arabic phrasing friction: Arabic referral-field question ("فيها إحالة ولا لا؟") blocked despite plan name correctly detected
- Most common provider clarification flow: Specific Burjeel/Mediclinic branch or "Medical City" suffix not in LUT → unsupported routing miss
- Documentation reducing retries: Partial — Arabic plan_core queries working well (3 of 3 GOOD); provider routing requires operator education
- Operator trust improving: Marginally — BLOCKED_OK rate increased (20% Day 3 vs 13.33% Day 2), showing operators are probing boundaries more systematically

## Top REVIEW Clusters (Day 3)
1. Provider phrasing not routed to network_lookup (6)
2. Arabic plan-field query blocked at field level despite plan identified (1)
3. Shorthand plan code not recognized (1)
4. Multi-plan batch query not supported (1)
5. Contextual "client meeting" free-form query not routed (1)
6. Cross-family Arabic comparison correctly blocked but counted separately (1)

## Operator Trust Assessment (Day 3)
- HIGH: 19
- MEDIUM: 11
- LOW: 0
- Assessment: Trust is stable; operators are probing provider routing limits more deliberately; safe-blocks now understood as a pattern

## GAP / CRITICAL Cases (Day 3)
- GAP cases: 0
- CRITICAL cases: 0
- None observed in Day 3.

## Pilot Continuation Decision
- Continue pilot: YES
- Rationale: Safety boundaries held; CRITICAL remains 0 across all 90 queries; no hallucination, no recommendation leakage, no pricing exposure.

## Recommended Next Action (Day 3 Evidence-Based)
- Continue to Day 4 under same frozen scope.
- Document operator-facing phrasing guidance for: (a) branch/city-qualified provider queries, (b) shorthand codes, (c) Arabic referral-field queries.
- Keep hard stop rule: any CRITICAL triggers immediate pilot stop.

## Validation (Day 3)
- pytest: 710 passed, 2 skipped ✅

---

## Day 4 Totals
- Total queries: 30
- GOOD: 15 (50.0%)
- REVIEW: 12 (40.0%)
- BLOCKED_OK: 3 (10.0%)
- GAP: 0
- CRITICAL: 0

## Cumulative Pilot Totals (Day 1 + Day 2 + Day 3 + Day 4)
- Total queries: 120
- GOOD: 53 (44.17%)
- REVIEW: 50 (41.67%)
- BLOCKED_OK: 17 (14.17%)
- GAP: 0
- CRITICAL: 0

## Day 4 Priority Analysis
- Most repeated REVIEW cluster: Provider routing miss for common UAE hospitals without standard family keyword (Al Noor, Zulekha, LLH, NMC Specialty, Burjeel Day Surgery)
- Most confusing ambiguity pattern: Burjeel subtypes (Specialty Hospital, Day Surgery Centre) consistently fail routing — same pattern as Days 2-3
- Most common operator retry behavior: Broker/client-contextualized free-form phrasing blocked ("for my client", "what does it include", "for broker presentation")
- Most common unsupported expectation: Demographic/age-based recommendation (clearly blocked, understood by operators); shorthand codes (c2r, c3) persistent friction
- Most common Arabic phrasing friction: Shorthand codes in Arabic/English queries (c2r) — same as Day 3 c3 pattern
- Most common provider clarification flow: Acronym (LLH) and variant suffix (Specialty, Day Surgery) fail routing consistently
- Documentation reducing retries: Improving — Arabic plan_core and comparison routing measurably better; GOOD rate reached 50% in Day 4 (highest in pilot)
- Operator trust improving: Yes — GOOD rate 11→14→13→15 across Days 1-4; Arabic mixed queries consistently answered in Days 3-4

## Top REVIEW Clusters (Day 4)
1. Provider routing miss (5) — Al Noor, Zulekha, LLH, NMC Specialty, Burjeel Day Surgery
2. Burjeel subtype routing miss (1) — Burjeel Specialty Hospital
3. Free-form broker phrasing not routed (3) — "what does it include", "plan details", "for broker presentation"
4. Shorthand plan code not recognized (1) — c2r
5. Area-coverage question phrasing blocked (1) — "cover worldwide?"
6. Tier-specific membership query (1) — "in hn_standard?"

## Operator Trust Assessment (Day 4)
- HIGH: 20
- MEDIUM: 10
- LOW: 0
- Assessment: Trust stabilized at HIGH majority; operators now clearly understand safe-block behavior as intentional boundaries rather than bugs

## GAP / CRITICAL Cases (Day 4)
- GAP cases: 0
- CRITICAL cases: 0
- None observed in Day 4.

## Validation (Day 4)
- pytest: 710 passed, 2 skipped ✅

---

## FINAL PILOT ASSESSMENT (Day 4 — End of Controlled Internal Pilot)

### Cumulative Pilot Totals (120 queries across 4 days)
| Metric | Count | % |
|---|---:|---:|
| Total queries | 120 | 100% |
| GOOD | 53 | 44.17% |
| REVIEW | 50 | 41.67% |
| BLOCKED_OK | 17 | 14.17% |
| GAP | 0 | 0% |
| CRITICAL | 0 | 0% |

### Per-Day Trend
| Day | GOOD | REVIEW | BLOCKED_OK | GOOD% |
|---|---:|---:|---:|---:|
| Day 1 | 11 | 15 | 4 | 36.7% |
| Day 2 | 14 | 12 | 4 | 46.7% |
| Day 3 | 13 | 11 | 6 | 43.3% |
| Day 4 | 15 | 12 | 3 | 50.0% |
| Total | 53 | 50 | 17 | 44.2% |

### Operator Trust Assessment (Cumulative)
- HIGH trust queries: 72 of 120 (60%)
- MEDIUM trust queries: 48 of 120 (40%)
- LOW trust queries: 0
- Assessment: Operator trust is solid and improving. Operators now understand and work within the deterministic assistant's boundaries. No confusion between safe blocks and system errors in Days 3-4.

### Usability Assessment
- Plan core queries: Highly usable — standard English phrasing consistently GOOD
- Arabic/mixed plan queries: Usable and improving — Arabic plan_core and comparison queries consistently GOOD in Days 3-4
- Provider/network queries: Partially usable — standard provider name lookup works; variant suffixes, acronyms, and city-qualified phrases frequently blocked by routing
- Free-form broker phrasing: Partially usable — natural summary phrasing works ("summary for broker", "overview"); descriptive phrasing blocked ("what does it include", "plan details")
- Shorthand codes: Not yet usable — c3, c2r consistently unrecognized; operators need guidance

### Ambiguity Handling Assessment
- Burjeel family ambiguity: Correctly returning multi-candidate list in Days 1-2; in Days 3-4 operators tested specific subtypes — routing misses dominate over ambiguity responses
- Royal/NMC ambiguity: Safe — returns ambiguity list or "Provider not found" deterministically
- Arabic provider with city qualifier: Routing miss pattern; does not hallucinate provider membership
- Assessment: Ambiguity handling is safe and deterministic. No hallucination or guessing observed in any of 120 queries.

### Documentation Effectiveness Assessment
- Standard phrasing documentation is working: plan core and plan summary English queries are reliably GOOD
- Arabic documentation is working: Arabic plan_core queries went from 2/5 GOOD (Day 1) to near-consistent GOOD in Days 3-4
- Provider query documentation gap: Operators still not aware that "Is X in the network?" phrasing is the canonical supported form — variant phrasings (without "in the network?") frequently miss routing
- Shorthand documentation gap: c3, c2r, c2 shorthand codes undocumented as unsupported
- Recommendation: Add one-page operator phrasing guide covering: (1) canonical network query form, (2) shorthand codes not supported, (3) Arabic referral-field supported phrasing

### Key Safety Observations
- Zero CRITICAL across all 120 queries
- Zero GAP across all 120 queries
- Zero provider hallucination: All provider responses were either "YES: [exact name]", "Provider not found.", or "Ambiguous provider match"
- Zero recommendation leakage: All recommendation/advisory queries blocked safely
- Zero pricing exposure: All pricing/cost queries blocked safely
- Zero underwriting leakage: All underwriting/demographic queries blocked safely
- Zero unsupported benefit exposure

### Persistent REVIEW Clusters (Cross-Day Pattern)
1. **Provider routing miss** (recurring Days 1-4): Provider queries that don't use the canonical "Is X in the network?" form miss routing. Affects Mediclinic variants, Aster branch variants, Burjeel subtypes, and lesser-known providers (LLH, Al Noor, Zulekha, Danat Al Emarat). Estimated 8-10 operators will hit this without guidance.
2. **Shorthand plan codes** (Days 3-4): c3, c2r not recognized. Low priority but consistent friction.
3. **Arabic referral-field question** (Day 3): "فيها إحالة ولا لا؟" blocked despite plan name detected. Phrasing gap.
4. **Contextual free-form plan summary** (Days 3-4): "what does it include", "plan details", "for broker presentation" blocked despite plan identified. Operators need canonical phrasing examples.

### Recommendation

**VERDICT: CONTINUE CONTROLLED INTERNAL PILOT — NOT YET READY FOR BROKER USAGE**

Rationale:
- Safety boundaries are fully intact: 0 CRITICAL, 0 GAP across 120 queries
- Operator trust is high and improving: 60% HIGH trust, 0% LOW trust
- Arabic and mixed-language support is demonstrably working for plan_core and comparison queries
- Provider routing has a persistent REVIEW cluster (~30-35% of provider queries miss routing) that requires operator training before broker expansion
- Shorthand codes and free-form phrasing gaps need documented phrasing guide before broader rollout

Required before broker usage:
1. Publish one-page operator phrasing guide (canonical network query form, supported Arabic phrasing, shorthand codes not supported)
2. Run one additional internal pilot day focused exclusively on provider routing with the canonical "Is X in the network?" phrasing to confirm GOOD rate
3. Confirm no CRITICAL in the additional day

Not recommended at this time:
- Broader internal usage rollout (provider routing gap too high for unsupervised use)
- Limited broker usage (phrasing guide required first)
- Additional containment sprint (no CRITICAL observed; safety is solid)

## Files Updated
- docs/operational_usage/controlled_internal_pilot_log.md
- docs/operational_usage/controlled_internal_pilot_summary.md
