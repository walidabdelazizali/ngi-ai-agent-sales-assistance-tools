# Professional Simulation Review Actions

## Scope
- Source analyzed: docs/operational_usage/professional_simulation_results.md
- Rows included: REVIEW and GAP only
- Mode: hardening action plan only (no runtime changes in this task)

## Extraction Summary
- REVIEW rows: 8
- GAP rows: 4
- Total rows analyzed: 12

## Item-by-Item Classification and Action

### 1) Which network is better for Dubai?
- query: Which network is better for Dubai?
- current status: REVIEW
- current answer: Sorry, this query is not supported or not available. Please specify a supported plan or question.
- issue classification: unsafe/ambiguous query
- recommended action: Keep blocked. Requires ranking logic and network suitability criteria not in current deterministic core scope.
- patch now?: no
- reason: Comparative recommendation is outside current enabled boundaries and would risk implicit comparison enablement.

### 2) Is there private room coverage for Classic 2R?
- query: Is there private room coverage for Classic 2R?
- current status: REVIEW
- current answer: Sorry, this query is not supported or not available. Please specify a supported plan or question.
- issue classification: data gap
- recommended action: Defer. Capture as future normalization candidate for room-type exposure.
- patch now?: no
- reason: Room type is not currently exposed in approved runtime core fields; expanding now would be normalization scope change.

### 3) ينفع استخدمها في مصر؟
- query: ينفع استخدمها في مصر؟
- current status: REVIEW
- current answer: عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
- issue classification: unsafe/ambiguous query
- recommended action: Defer. Requires plan disambiguation and geography interpretation policy for multilingual free-text usage intent.
- patch now?: no
- reason: Query is plan-less and ambiguous across multiple plans.

### 4) هل يغطي الطوارئ في كلاسيك 2R؟
- query: هل يغطي الطوارئ في كلاسيك 2R؟
- current status: REVIEW
- current answer: عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
- issue classification: data gap
- recommended action: Defer. Add to future benefits normalization backlog (emergency/inpatient benefit exposure).
- patch now?: no
- reason: Emergency coverage is outside current approved deterministic answer surface.

### 5) ملخص كلاسيك 2
- query: ملخص كلاسيك 2
- current status: REVIEW
- current answer: عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
- issue classification: routing gap
- recommended action: Patch in a dedicated hardening sprint by adding Arabic Classic 2 alias variants (safe summary/core routing only).
- patch now?: no
- reason: Safe to fix, but appears as a single-instance wording/routing gap in this pack; current task is action-plan only.

### 6) worldwide classic2?
- query: worldwide classic2?
- current status: REVIEW
- current answer: Sorry, this query is not supported or not available. Please specify a supported plan or question.
- issue classification: wording issue
- recommended action: Consider a future wording hardening rule mapping plan-scoped "worldwide" to area-of-coverage intent.
- patch now?: no
- reason: One-off phrasing in this pack; not yet a repeated pattern.

### 7) best enhanced plan overall
- query: best enhanced plan overall
- current status: REVIEW
- current answer: Sorry, this query is not supported or not available. Please specify a supported plan or question.
- issue classification: intentionally unsupported
- recommended action: Keep blocked.
- patch now?: no
- reason: Requires recommendation logic and implicit comparison enablement, both out of current scope.

### 8) Tell me about Classic 4
- query: Tell me about Classic 4
- current status: REVIEW
- current answer: Sorry, this query is not supported or not available. Please specify a supported plan or question.
- issue classification: intentionally unsupported
- recommended action: Keep blocked.
- patch now?: no
- reason: Classic 4 is not in supported plan set.

### 9) maternity Classic 3
- query: maternity Classic 3
- current status: GAP
- current answer: Sorry, this query is not supported or not available. Please specify a supported plan or question.
- issue classification: data gap
- recommended action: Defer as explicit normalization candidate.
- patch now?: no
- reason: User constraint explicitly says do not expose pharmacy/maternity now.

### 10) pharmacy Classic 2R
- query: pharmacy Classic 2R
- current status: GAP
- current answer: Sorry, this query is not supported or not available. Please specify a supported plan or question.
- issue classification: data gap
- recommended action: Defer as explicit normalization candidate.
- patch now?: no
- reason: User constraint explicitly says do not expose pharmacy/maternity now.

### 11) pharmacy Classic 3
- query: pharmacy Classic 3
- current status: GAP
- current answer: Sorry, this query is not supported or not available. Please specify a supported plan or question.
- issue classification: data gap
- recommended action: Defer as explicit normalization candidate.
- patch now?: no
- reason: User constraint explicitly says do not expose pharmacy/maternity now.

### 12) maternity Classic 2R
- query: maternity Classic 2R
- current status: GAP
- current answer: Sorry, this query is not supported or not available. Please specify a supported plan or question.
- issue classification: data gap
- recommended action: Defer as explicit normalization candidate.
- patch now?: no
- reason: User constraint explicitly says do not expose pharmacy/maternity now.

## Patch-Now Decision
- Patch now candidates from this extraction: none

## Recommended Next Hardening Queue
1. Safe routing/wording queue (defer-to-next sprint):
   - Arabic Classic 2 summary phrasing (ملخص كلاسيك 2)
   - Plan-scoped worldwide phrasing for area of coverage (worldwide classic2?)
2. Deferred normalization queue (do not patch now):
   - private room exposure
   - emergency coverage exposure
   - pharmacy/maternity exposure for Classic 2R and Classic 3
3. Keep intentionally blocked:
   - enhanced plan recommendation/comparison intent
   - unsupported plan requests (Classic 4)