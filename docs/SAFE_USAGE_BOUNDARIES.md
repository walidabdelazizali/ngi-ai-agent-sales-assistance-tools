# Safe Usage Boundaries (Stabilization Freeze)

## Freeze Metadata
- Branch: stage2-live
- Stable commit: 953aad2
- Stable tag: v-safety-boundary-hardening-1

## Boundary Principle
The assistant is deterministic and evidence-bounded. It may answer only within approved data and approved intents. Any request outside scope must be blocked safely.

## Allowed Behavior
- Plan summary for approved plans.
- Plan core-field retrieval for approved plans.
- Provider and network lookup for known providers.
- Arabic and mixed routing for currently normalized patterns.
- Classic 2R baseline behavior for approved deterministic intents.
- Factual comparisons for supported pairwise comparison prompts.

## Explicitly Blocked Behavior

### 1) Recommendation-Style Plan Selection
Blocked examples:
- Which plan is better for this client?
- What should I choose?
- افضل خطة للعميل؟

Expected behavior:
- Return unsupported/safe-block response.
- Direct operator/user to factual comparison phrasing where applicable.

### 2) Pricing Advice
Blocked examples:
- Give me the price.
- Which is the cheapest plan?

Expected behavior:
- Return unsupported/safe-block response.

### 3) Underwriting Advice
Blocked examples:
- Is this client accepted?
- Which plan is better for diabetes underwriting?

Expected behavior:
- Return unsupported/safe-block response.

### 4) Unapproved Enhanced Benefits
Blocked examples:
- maternity Classic 2R
- pharmacy Classic 2R
- dental Classic 2R
- optical Classic 2R

Expected behavior:
- Return unsupported/safe-block response.

### 5) Unknown Provider Guessing
Blocked examples:
- Guess network for unknown clinic names.
- Infer provider/network without known deterministic match.

Expected behavior:
- Return provider-not-found or ambiguity-safe response.
- Do not hallucinate provider membership.

### 6) Broad Business Advice
Blocked examples:
- What should brokers usually sell?
- What is best value overall for market strategy?

Expected behavior:
- Return unsupported/safe-block response.

## Safety Output Rules
- No recommendation output in blocked pathways.
- No internal leakage of protected internal fields in user-facing messages.
- No probabilistic or speculative statements.
- No invented provider or benefit data.

## Escalation Trigger
Escalate immediately if any blocked category produces a substantive recommendation/pricing/underwriting answer. Classify as GAP and follow containment in operator runbook.
