# Known Limitations (Stabilization Freeze)

## Freeze Metadata
- Branch: stage2-live
- Stable commit: 953aad2
- Stable tag: v-safety-boundary-hardening-1

## Scope Limitation
This baseline is intentionally constrained to deterministic internal operations. Expansion work is frozen.

## Functional Limitations
- No recommendation-style plan selection.
- No pricing computation or premium advice.
- No underwriting acceptance or underwriting strategy advice.
- No broad business strategy guidance.
- No unknown-provider guessing.
- No enhanced benefit expansion beyond approved baseline behavior.

## Comparison Limitation
- Factual comparison is supported only in approved deterministic phrasing and supported plan contexts.
- Recommendation-style comparison phrasing is blocked by design.

## Language and Routing Limitation
- Arabic/mixed support is deterministic and pattern-bound.
- Free-form language beyond normalized routes may be safely blocked.
- Plan-less ambiguous questions are expected to block safely.

## Data and Matching Limitation
- Provider lookup behavior depends on deterministic alias coverage and dataset mappings.
- Ambiguous provider family names may return ambiguity-safe responses instead of direct resolution.

## Architecture Limitation
- No RAG retrieval layer.
- No probabilistic ranking or semantic recommendation model.
- No architecture rewrite in freeze scope.

## Operational Limitation
- REVIEW outcomes still require operator triage and targeted follow-up.
- Any GAP requires immediate containment and narrow fix planning before replay.

## What This Means for Internal Use
- Use this assistant for deterministic evidence-backed Q and A only.
- Treat unsupported behavior as expected safety behavior, not feature failure.
- Use blocked responses to maintain boundary integrity during demos and operations.
