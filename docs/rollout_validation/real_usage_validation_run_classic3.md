# Real Usage Validation Evidence: Classic 3

## Run Context
- Repo: walidabdelazizali/ngi-ai-agent-sales-assistance-tools
- Branch: stage2-live
- Baseline tag: v-enhanced-classic3-stable
- Validation pack: docs/rollout_validation/real_usage_validation_pack_classic3.md
- Date: 2026-05-09

## Summary
- Total queries replayed: 84
- Pass: 64
- Fail: 20
- Unsupported responses: 20
- Ambiguity hits: 8
- Typo failures: 1
- Arabic parsing gaps: 6
- Internal leakage hits: 0

## Pass / Fail Table
| ID | Category | Question | Expected | Actual | Result | Notes |
|---|---|---|---|---|---|---|
| 1 | A Summary | classic3 summary | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 2 | A Summary | classic-3 summary | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 3 | A Summary | Classic 03 summary | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 4 | A Summary | Summarize HN_CLASSIC_3 | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 5 | A Summary | Summarize HN Classic 3 | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 6 | A Summary | Summarize كلاسيك 3 | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 7 | A Summary | Give me a summary of Classic 3 | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 8 | A Summary | Tell me about Classic 3 | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 9 | A Summary | Classic 3 overview | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 10 | A Summary | Plan summary for Classic 3 | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 11 | B Annual Limit | classic3 limit | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 12 | B Annual Limit | classic-3 annual limit | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 13 | B Annual Limit | Classic 03 limit | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 14 | B Annual Limit | What is the annual limit for Classic 3? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 15 | B Annual Limit | HN_CLASSIC_3 annual limit | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 16 | B Annual Limit | HN Classic 3 limit | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 17 | B Annual Limit | ليمت كلاسيك 3 | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 18 | B Annual Limit | Annual limit Classic 3 | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 19 | B Annual Limit | How much is Classic 3 annual limit? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 20 | B Annual Limit | What is the plan limit for Classic 3? | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 21 | C Network | classic3 network | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 22 | C Network | classic-3 network | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 23 | C Network | Classic 03 network name | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 24 | C Network | What is the network name for Classic 3? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 25 | C Network | شبكة كلاسيك 3 | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 26 | C Network | HN_CLASSIC_3 network | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 27 | C Network | HN Classic 3 network | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 28 | C Network | What network is Classic 3 on? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 29 | C Network | classic 3 الشبكة | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 30 | C Network | Network for Classic 3 | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 31 | D Area of Coverage | classic3 coverage area | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 32 | D Area of Coverage | classic-3 area of coverage | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 33 | D Area of Coverage | Classic 03 coverage | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 34 | D Area of Coverage | What is the area of coverage for Classic 3? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 35 | D Area of Coverage | تغطية كلاسيك 3 | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 36 | D Area of Coverage | Classic 3 coverage area | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 37 | D Area of Coverage | HN_CLASSIC_3 coverage | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 38 | D Area of Coverage | HN Classic 3 area of coverage | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 39 | D Area of Coverage | What countries are covered by Classic 3? | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 40 | D Area of Coverage | Is Classic 3 valid in UAE and home country? | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 41 | E Direct Billing | does classic 3 have direct billing? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 42 | E Direct Billing | classic3 direct billing | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 43 | E Direct Billing | classic-3 direct billing available? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 44 | E Direct Billing | هل فيه direct billing؟ | plan_core / Classic 3 | unsupported / None | FAIL | unexpected unsupported; plan mismatch; intent mismatch; routing ambiguity |
| 45 | E Direct Billing | هل كلاسيك 3 فيه direct billing؟ | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 46 | E Direct Billing | HN_CLASSIC_3 direct billing | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 47 | E Direct Billing | HN Classic 3 direct billing | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 48 | E Direct Billing | direct billing Classic 3 | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 49 | E Direct Billing | Is direct billing available for Classic 3? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 50 | E Direct Billing | Classic 3 cashless? | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 51 | F Referral | does classic 3 require referral? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 52 | F Referral | classic3 referral | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 53 | F Referral | classic-3 referral required? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 54 | F Referral | هل يحتاج referral؟ | plan_core / Classic 3 | unsupported / None | FAIL | unexpected unsupported; plan mismatch; intent mismatch; routing ambiguity |
| 55 | F Referral | هل كلاسيك 3 يحتاج referral؟ | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 56 | F Referral | HN_CLASSIC_3 referral | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 57 | F Referral | HN Classic 3 needs referral? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 58 | F Referral | referral for Classic 3 | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 59 | F Referral | Is referral needed for Classic 3? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 60 | F Referral | Classic 3 need approval referral? | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 61 | G Arabic-only | ملخص كلاسيك 3 | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 62 | G Arabic-only | ما هو الحد السنوي لكلاسيك 3؟ | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 63 | G Arabic-only | ما هي الشبكة لكلاسيك 3؟ | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 64 | G Arabic-only | ما هي التغطية لكلاسيك 3؟ | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 65 | G Arabic-only | هل فيه دفع مباشر لكلاسيك 3؟ | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 66 | G Arabic-only | هل يحتاج إحالة كلاسيك 3؟ | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 67 | H Mixed Arabic/English | classic 3 الشبكة | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 68 | H Mixed Arabic/English | classic3 annual limit | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 69 | H Mixed Arabic/English | كلاسيك 3 coverage | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 70 | H Mixed Arabic/English | HN classic 3 ليمت | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 71 | H Mixed Arabic/English | classic 3 summary | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 72 | H Mixed Arabic/English | classic 3 direct billing | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 73 | I Short Broker-style | classic3? | plan_summary / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 74 | I Short Broker-style | Classic 3 limit please | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 75 | I Short Broker-style | Classic 3 network pls | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 76 | I Short Broker-style | Classic 3 coverage pls | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 77 | I Short Broker-style | Classic 3 direct billing pls | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 78 | I Short Broker-style | Classic 3 referral pls | plan_core / Classic 3 | plan_core / Classic 3 | PASS |  |
| 79 | J Typo Tolerance | classic 3 summary | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 80 | J Typo Tolerance | classic 03 summary | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |
| 81 | J Typo Tolerance | classic3 summry | unsupported / unsupported | unsupported / Classic 3 | FAIL | safe unsupported |
| 82 | J Typo Tolerance | classic-3 limt | plan_core / Classic 3 | unsupported / Classic 3 | FAIL | unexpected unsupported; intent mismatch; routing ambiguity |
| 83 | J Typo Tolerance | كلاسيك3 ليمت | plan_core / Classic 3 | unsupported / None | FAIL | unexpected unsupported; plan mismatch; intent mismatch; routing ambiguity |
| 84 | J Typo Tolerance | كلاسيك 03 ملخص | plan_summary / Classic 3 | plan_summary / Classic 3 | PASS |  |

## Unsupported Query List
- classic3 limit -> unsupported / Classic 3
- Classic 03 limit -> unsupported / Classic 3
- HN Classic 3 limit -> unsupported / Classic 3
- What is the plan limit for Classic 3? -> unsupported / Classic 3
- Classic 03 coverage -> unsupported / Classic 3
- HN_CLASSIC_3 coverage -> unsupported / Classic 3
- What countries are covered by Classic 3? -> unsupported / Classic 3
- Is Classic 3 valid in UAE and home country? -> unsupported / Classic 3
- هل فيه direct billing؟ -> unsupported / None
- Classic 3 cashless? -> unsupported / Classic 3
- هل يحتاج referral؟ -> unsupported / None
- هل فيه دفع مباشر لكلاسيك 3؟ -> unsupported / Classic 3
- هل يحتاج إحالة كلاسيك 3؟ -> unsupported / Classic 3
- كلاسيك 3 coverage -> unsupported / Classic 3
- classic3? -> unsupported / Classic 3
- Classic 3 limit please -> unsupported / Classic 3
- Classic 3 coverage pls -> unsupported / Classic 3
- classic3 summry -> unsupported / Classic 3
- classic-3 limt -> unsupported / Classic 3
- كلاسيك3 ليمت -> unsupported / None

## Routing Ambiguity List
- classic3 limit
- Classic 03 limit
- Classic 03 coverage
- هل فيه دفع مباشر لكلاسيك 3؟
- هل يحتاج إحالة كلاسيك 3؟
- كلاسيك 3 coverage
- classic3?
- classic-3 limt

## Typo Failures
- classic-3 limt

## Arabic Parsing Gaps
- هل فيه direct billing؟
- هل يحتاج referral؟
- هل فيه دفع مباشر لكلاسيك 3؟
- هل يحتاج إحالة كلاسيك 3؟
- كلاسيك 3 coverage
- كلاسيك3 ليمت

## Internal Leakage Check
- No raw/internal leakage detected in JSON envelopes or business text.

## Output Hardening Notes
- JSON envelopes remained stable for supported and unsupported queries.
- Business-facing messages stayed deterministic and non-hallucinatory for the replay set.
- Summary outputs did not duplicate core labels in the replayed samples.

## Future Hardening Recommendations
- Add more typo variants around collapsed spacing and hyphenation if future broker logs show them in the wild.
- Expand Arabic natural-language patterns only if new production phrasing emerges.
- Keep comparison out of scope for Classic 3 until a separate, deliberate expansion sprint.
