# Supported Capabilities (Stabilization Freeze)

## Freeze Metadata
- Branch: stage2-live
- Stable commit: 953aad2
- Stable tag: v-safety-boundary-hardening-1
- Mode: deterministic internal baseline
- Scope: documentation and operationalization only

## Purpose
This document defines what the assistant is expected to do during the stabilization freeze. It is the authoritative list of supported behavior for internal operations and demos.

## Supported Capabilities

### 1) Plan Summary
- Supports deterministic summary queries for approved plans.
- Returns plan-identifying fields and approved summary content only.
- No recommendation text is included.

### 2) Plan Core Fields
- Supports deterministic plan-core lookups including:
  - annual limit
  - network
  - area of coverage
  - direct billing
  - referral required
- Supports reimbursement rule lookup where available in approved data.

### 3) Provider/Network Lookup
- Supports deterministic provider-to-network lookup for known providers.
- Supports network tier checks for known providers.
- Supports safe handling for provider ambiguity and provider-not-found conditions.

### 4) Arabic and Mixed Routing
- Supports deterministic Arabic and mixed Arabic-English phrasing for approved routing patterns.
- Supports Arabic/mixed plan and provider query forms covered by current normalization rules.

### 5) Classic 2R Enhanced Baseline
- Supports Classic 2R as an approved enhanced baseline plan for allowed deterministic intents.
- Supports classic core-field queries and summary behavior within the approved scope.
- Does not open additional enhanced-plan expansion.

### 6) Factual Comparisons
- Supports factual comparison phrasing between approved comparable plans.
- Comparison output is factual and field-based.
- Recommendation-style guidance is intentionally excluded.

### 7) Safe Blocking Behavior
- Deterministically blocks unsupported or out-of-scope requests.
- Uses explicit safe messaging for unsupported behavior.
- Maintains protected boundaries for recommendation, pricing, underwriting, and unapproved scope.

## Operational Classification Mapping
- GOOD: supported behavior returned deterministically as expected.
- REVIEW: non-ideal supported-path behavior requiring operational review.
- BLOCKED_OK: unsupported request was correctly and safely blocked.
- GAP: boundary failure or unsupported behavior leak requiring immediate containment.

## Freeze Guardrails
- No feature expansion in freeze mode.
- No enhanced plan expansion beyond current approved baseline.
- No RAG.
- No recommendation engine.
- No pricing engine.
- No UI/Telegram expansion work under this freeze document.
