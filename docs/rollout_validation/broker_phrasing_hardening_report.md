# Broker Phrasing Hardening Evidence: Classic 3

## Summary
- Queries replayed: 27
- Pass: 27
- Fail: 0
- Supported queries stabilized: 20
- Unsupported-safe queries: 7
- Routing ambiguities remaining: 0
- Typo failures remaining: 0
- Arabic parsing gaps remaining: 0
- Internal leakage hits: 0

## Pass / Fail Table
| Question | Expected | Actual | Result | Notes |
|---|---|---|---|---|
| classic3 limit | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| HN Classic 3 limit | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| كلاسيك3 ليمت | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| Classic 3 cashless? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| classic3 limt | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| classic 3 cash less | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| classic3 | unsupported / unsupported | unsupported / Classic 3 | PASS | safe unsupported |
| classic-3 | unsupported / unsupported | unsupported / Classic 3 | PASS | safe unsupported |
| Classic 03 | unsupported / unsupported | unsupported / Classic 3 | PASS | safe unsupported |
| Summarize HN_CLASSIC_3 | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| Summarize HN Classic 3 | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| classic3 summary | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| ليمت كلاسيك 3 | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| شبكة كلاسيك 3 | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| تغطية كلاسيك 3 | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| classic 3 الشبكة | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| classic3 annual limit | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| كلاسيك 3 coverage | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| HN classic 3 ليمت | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| هل كلاسيك 3 فيه direct billing؟ | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| هل كلاسيك 3 يحتاج referral؟ | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| هل فيه direct billing؟ | unsupported / unsupported | unsupported / None | PASS | safe unsupported |
| هل يحتاج referral؟ | unsupported / unsupported | unsupported / None | PASS | safe unsupported |
| classic3? | unsupported / unsupported | unsupported / Classic 3 | PASS | safe unsupported |
| classic3 summry | unsupported / unsupported | unsupported / Classic 3 | PASS | safe unsupported |
| classic-3 limt | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| What countries are covered by Classic 3? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |

## Unsupported Query List
- classic3
- classic-3
- Classic 03
- هل فيه direct billing؟
- هل يحتاج referral؟
- classic3?
- classic3 summry

## Routing Ambiguity List
- None

## Typo Failures
- None

## Arabic Parsing Gaps
- None

## Hardening Outcome
- Supported broker shorthand and collapsed-spacing variants now route deterministically.
- Plan-less Arabic shorthand remains safely unsupported; no plan inference was introduced.
- JSON envelopes remained stable and no internal fields leaked.
- No comparison behavior changed.
