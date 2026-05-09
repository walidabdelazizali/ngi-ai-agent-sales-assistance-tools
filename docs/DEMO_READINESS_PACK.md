# Demo Readiness Pack

## 1) Project Overview
NGI AI Agent Sales Assistance Tools is a deterministic insurance Q&A platform for controlled broker and management demos. It answers supported insurance questions with fixed routing, validated data sources, approval gates, and regression-backed behavior.

## 2) Current Stable Baseline
- Branch: stage2-live
- Stable baseline tag: v-enhanced-classic3-stable
- Current test status: 591 passed, 2 skipped
- Broker phrasing replay: 27/27 passed

## 3) Supported Plans
- Classic 2
- Classic 3
- Remedy 02
- Remedy 03
- Remedy 04
- Remedy 05
- Remedy 06

## 4) Supported Query Types
- Plan summary
- Annual limit lookup
- Network lookup
- Area of coverage lookup
- Direct billing lookup
- Referral requirement lookup
- Reimbursement rules (Remedy-safe flow)
- Deterministic unsupported-safe fallback

## 5) Deterministic Architecture (Executive Summary)
- No probabilistic answer generation and no hallucination layer.
- Query routing uses deterministic alias and keyword patterns.
- Plan loading uses canonical source mapping and approval validation.
- Customer-facing responses are gated behind readiness checks.
- Unsupported prompts return safe, stable envelopes and user-safe wording.

See detailed architecture: docs/architecture/DETERMINISTIC_INSURANCE_CORE.md

## 6) Safety + Validation Model
- Canonical source boundary: controlled source loading paths only.
- Approval boundary: only approved/ready plans return customer-facing answers.
- Validation gates: normalize + validate before response composition.
- Regression-first policy: behavior guarded by focused tests and full pytest.
- Output hardening: no internal field leakage in customer-safe responses.

## 7) English and Arabic Routing Examples

English supported examples:
- Summarize Classic 3
- What is the annual limit for Classic 3?
- What is the network name for Classic 3?
- Is direct billing available for Classic 3?

Arabic supported examples:
- ملخص كلاسيك 3
- ليمت كلاسيك 3
- شبكة كلاسيك 3
- هل كلاسيك 3 يحتاج referral؟

Mixed supported examples:
- classic 3 الشبكة
- كلاسيك 3 coverage
- HN classic 3 ليمت

## 8) Unsupported-Safe Behavior Examples
- هل فيه direct billing؟  (plan-less shorthand, safely unsupported)
- هل يحتاج referral؟  (plan-less shorthand, safely unsupported)
- Tell me about Classic 4  (out of scope plan)
- Compare Classic 3 and Remedy 04  (scope boundary: comparison expansion not enabled)

Typical safe response style:
- Sorry, this query is not supported or not available. Please specify a supported plan or question.

## 9) Scope Boundaries (Current Release)
- No new plans beyond current approved set.
- No comparison expansion for enhanced plans.
- No architecture refactor.
- No Telegram, CRM, RAG, or AI-probabilistic routing work in this demo package.

## 10) Demo Operator Checklist
1. Confirm branch and stable baseline tag.
2. Run python -m pytest -q and verify 591 passed, 2 skipped.
3. Run the demo query pack in docs/demo/demo_queries.md.
4. Verify expected routing and no internal leakage.
5. Show unsupported-safe behavior with boundary examples.

## 11) Evidence References
- docs/rollout_validation/validation_pack.md
- docs/rollout_validation/real_usage_validation_pack_classic3.md
- docs/rollout_validation/real_usage_validation_run_classic3.md
- docs/rollout_validation/broker_phrasing_hardening_report.md
- docs/rollout_validation/validation_run_03_runtime_results.md

## 12) Rollback Reference
- Stable presentation baseline tag: v-enhanced-classic3-stable
