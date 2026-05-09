# Classic 2 + Classic 3 Usage Simulation Results

## Run Context
- Mode: simulation and evidence only
- Plans in scope: Classic 2, Classic 3
- Comparison in scope: existing Remedy comparison regression checks only

## Summary
- Total queries replayed: 153
- Passed: 148
- Failed: 5
- Pass rate: 96.73%

## Validation
- Test suite: python -m pytest -q (run separately in this sprint)
- Simulation replay: completed for all scenarios in this pack

## Issue Type Breakdown
- regression risk: 5

## Top Recurring Gaps
- summary: 4
- coverage: 1

## Detailed Results
| ID | Category | Query | Expected Intent | Expected Plan | Expected Behavior | Actual Result | Pass/Fail | Issue Type |
|---|---|---|---|---|---|---|---|---|
| 1 | Broker asking quickly | Classic 2 summary | plan_summary | Classic 2 | Fast summary answer | intent=plan_summary, plan=Classic 2, behavior=supported_response | PASS | - |
| 2 | Broker asking quickly | Classic 2 limit | plan_core | Classic 2 | Annual limit returned | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 3 | Broker asking quickly | classic2 summary | plan_summary | Classic 2 | Fast summary answer | intent=plan_summary, plan=Classic 2, behavior=supported_response | PASS | - |
| 4 | Broker asking quickly | classic2 limit | plan_core | Classic 2 | Annual limit returned | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 5 | Broker asking quickly | classic-2 summary | plan_summary | Classic 2 | Fast summary answer | intent=plan_summary, plan=Classic 2, behavior=supported_response | PASS | - |
| 6 | Broker asking quickly | classic-2 limit | plan_core | Classic 2 | Annual limit returned | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 7 | Broker asking quickly | Classic 02 summary | plan_summary | Classic 2 | Fast summary answer | intent=plan_summary, plan=Classic 2, behavior=supported_response | PASS | - |
| 8 | Broker asking quickly | Classic 02 limit | plan_core | Classic 2 | Annual limit returned | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 9 | Broker asking quickly | HN_CLASSIC_2 summary | plan_summary | Classic 2 | Fast summary answer | intent=plan_summary, plan=Classic 2, behavior=supported_response | PASS | - |
| 10 | Broker asking quickly | HN_CLASSIC_2 limit | plan_core | Classic 2 | Annual limit returned | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 11 | Broker asking quickly | HN Classic 2 summary | plan_summary | Classic 2 | Fast summary answer | intent=plan_summary, plan=Classic 2, behavior=supported_response | PASS | - |
| 12 | Broker asking quickly | HN Classic 2 limit | plan_core | Classic 2 | Annual limit returned | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 13 | Broker asking quickly | Classic 3 summary | plan_summary | Classic 3 | Fast summary answer | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 14 | Broker asking quickly | Classic 3 limit | plan_core | Classic 3 | Annual limit returned | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 15 | Broker asking quickly | classic3 summary | plan_summary | Classic 3 | Fast summary answer | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 16 | Broker asking quickly | classic3 limit | plan_core | Classic 3 | Annual limit returned | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 17 | Broker asking quickly | classic-3 summary | plan_summary | Classic 3 | Fast summary answer | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 18 | Broker asking quickly | classic-3 limit | plan_core | Classic 3 | Annual limit returned | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 19 | Broker asking quickly | Classic 03 summary | plan_summary | Classic 3 | Fast summary answer | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 20 | Broker asking quickly | Classic 03 limit | plan_core | Classic 3 | Annual limit returned | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 21 | Broker asking quickly | HN_CLASSIC_3 summary | plan_summary | Classic 3 | Fast summary answer | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 22 | Broker asking quickly | HN_CLASSIC_3 limit | plan_core | Classic 3 | Annual limit returned | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 23 | Broker asking quickly | HN Classic 3 summary | plan_summary | Classic 3 | Fast summary answer | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 24 | Broker asking quickly | HN Classic 3 limit | plan_core | Classic 3 | Annual limit returned | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 25 | Broker asking quickly | كلاسيك 3 summary | plan_summary | Classic 3 | Fast summary answer | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 26 | Broker asking quickly | كلاسيك 3 limit | plan_core | Classic 3 | Annual limit returned | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 27 | Broker asking quickly | كلاسيك3 summary | plan_summary | Classic 3 | Fast summary answer | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 28 | Broker asking quickly | كلاسيك3 limit | plan_core | Classic 3 | Annual limit returned | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 29 | HR asking formally | Could you provide a summary for Classic 2? | plan_summary | Classic 2 | Formal deterministic answer | intent=plan_summary, plan=Classic 2, behavior=supported_response | PASS | - |
| 30 | HR asking formally | What is the annual limit for Classic 2? | plan_core | Classic 2 | Formal deterministic answer | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 31 | HR asking formally | What is the network name for Classic 2? | plan_core | Classic 2 | Formal deterministic answer | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 32 | HR asking formally | What is the area of coverage for Classic 2? | plan_core | Classic 2 | Formal deterministic answer | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 33 | HR asking formally | Is direct billing available for Classic 2? | plan_core | Classic 2 | Formal deterministic answer | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 34 | HR asking formally | Does Classic 2 require referral? | plan_core | Classic 2 | Formal deterministic answer | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 35 | HR asking formally | Could you provide a summary for Classic 3? | plan_summary | Classic 3 | Formal deterministic answer | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 36 | HR asking formally | What is the annual limit for Classic 3? | plan_core | Classic 3 | Formal deterministic answer | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 37 | HR asking formally | What is the network name for Classic 3? | plan_core | Classic 3 | Formal deterministic answer | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 38 | HR asking formally | What is the area of coverage for Classic 3? | plan_core | Classic 3 | Formal deterministic answer | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 39 | HR asking formally | Is direct billing available for Classic 3? | plan_core | Classic 3 | Formal deterministic answer | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 40 | HR asking formally | Does Classic 3 require referral? | plan_core | Classic 3 | Formal deterministic answer | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 41 | Client asking in simple Arabic | ملخص كلاسيك 3 | plan_summary | Classic 3 | Arabic deterministic route | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 42 | Client asking in simple Arabic | ليمت كلاسيك 3 | plan_core | Classic 3 | Arabic deterministic route | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 43 | Client asking in simple Arabic | شبكة كلاسيك 3 | plan_core | Classic 3 | Arabic deterministic route | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 44 | Client asking in simple Arabic | تغطية كلاسيك 3 | plan_core | Classic 3 | Arabic deterministic route | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 45 | Client asking in simple Arabic | هل كلاسيك 3 فيه direct billing؟ | plan_core | Classic 3 | Arabic deterministic route | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 46 | Client asking in simple Arabic | هل كلاسيك 3 يحتاج referral؟ | plan_core | Classic 3 | Arabic deterministic route | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 47 | Client asking in simple Arabic | ملخص Classic 2 | plan_summary | Classic 2 | Arabic deterministic route | intent=plan_summary, plan=Classic 2, behavior=supported_response | PASS | - |
| 48 | Client asking in simple Arabic | ليمت Classic 2 | plan_core | Classic 2 | Arabic deterministic route | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 49 | Client asking in simple Arabic | شبكة Classic 2 | plan_core | Classic 2 | Arabic deterministic route | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 50 | Client asking in simple Arabic | تغطية Classic 2 | plan_core | Classic 2 | Arabic deterministic route | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 51 | Client asking in simple Arabic | هل Classic 2 فيه direct billing؟ | plan_core | Classic 2 | Arabic deterministic route | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 52 | Client asking in simple Arabic | هل Classic 2 يحتاج referral؟ | plan_core | Classic 2 | Arabic deterministic route | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 53 | Mixed Arabic/English | classic 3 الشبكة | plan_core | Classic 3 | Mixed-language deterministic route | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 54 | Mixed Arabic/English | classic3 annual limit | plan_core | Classic 3 | Mixed-language deterministic route | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 55 | Mixed Arabic/English | كلاسيك 3 coverage | plan_core | Classic 3 | Mixed-language deterministic route | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 56 | Mixed Arabic/English | HN classic 3 ليمت | plan_core | Classic 3 | Mixed-language deterministic route | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 57 | Mixed Arabic/English | classic 2 الشبكة | plan_core | Classic 2 | Mixed-language deterministic route | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 58 | Mixed Arabic/English | HN classic 2 ليمت | plan_core | Classic 2 | Mixed-language deterministic route | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 59 | Typos and shorthand | classic3 limt | plan_core | Classic 3 | Typo-tolerant limit shorthand | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 60 | Typos and shorthand | classic-3 cash less | plan_core | Classic 3 | Cashless shorthand resolved | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 61 | Typos and shorthand | classic2 limt | plan_core | Classic 2 | Typo-tolerant limit shorthand | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 62 | Typos and shorthand | classic-2 cash less | plan_core | Classic 2 | Cashless shorthand resolved | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 63 | Typos and shorthand | classic3 summry | unsupported | unsupported | Safe unsupported fallback for typo summary | intent=unsupported, plan=Classic 3, behavior=safe_unsupported | PASS | - |
| 64 | Typos and shorthand | classic2 summry | unsupported | unsupported | Safe unsupported fallback for typo summary | intent=unsupported, plan=Classic 2, behavior=safe_unsupported | PASS | - |
| 65 | Network questions | What is the network for Classic 2? | plan_core | Classic 2 | Network questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 66 | Network questions | Classic 2 network | plan_core | Classic 2 | Network questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 67 | Network questions | network name Classic 2 | plan_core | Classic 2 | Network questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 68 | Network questions | What is the network for Classic 3? | plan_core | Classic 3 | Network questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 69 | Network questions | Classic 3 network | plan_core | Classic 3 | Network questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 70 | Network questions | network name Classic 3 | plan_core | Classic 3 | Network questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 71 | Annual limit questions | What is the annual limit for Classic 2? | plan_core | Classic 2 | Annual limit questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 72 | Annual limit questions | Classic 2 limit | plan_core | Classic 2 | Annual limit questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 73 | Annual limit questions | annual limit Classic 2 | plan_core | Classic 2 | Annual limit questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 74 | Annual limit questions | What is the annual limit for Classic 3? | plan_core | Classic 3 | Annual limit questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 75 | Annual limit questions | Classic 3 limit | plan_core | Classic 3 | Annual limit questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 76 | Annual limit questions | annual limit Classic 3 | plan_core | Classic 3 | Annual limit questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 77 | Coverage area questions | What is the area of coverage for Classic 2? | plan_core | Classic 2 | Coverage area questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 78 | Coverage area questions | Classic 2 coverage | plan_core | Classic 2 | Coverage area questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 79 | Coverage area questions | coverage area Classic 2 | plan_core | Classic 2 | Coverage area questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 80 | Coverage area questions | What is the area of coverage for Classic 3? | plan_core | Classic 3 | Coverage area questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 81 | Coverage area questions | Classic 3 coverage | plan_core | Classic 3 | Coverage area questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 82 | Coverage area questions | coverage area Classic 3 | plan_core | Classic 3 | Coverage area questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 83 | Direct billing questions | Is direct billing available for Classic 2? | plan_core | Classic 2 | Direct billing questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 84 | Direct billing questions | Classic 2 direct billing | plan_core | Classic 2 | Direct billing questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 85 | Direct billing questions | Classic 2 cashless? | plan_core | Classic 2 | Direct billing questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 86 | Direct billing questions | Is direct billing available for Classic 3? | plan_core | Classic 3 | Direct billing questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 87 | Direct billing questions | Classic 3 direct billing | plan_core | Classic 3 | Direct billing questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 88 | Direct billing questions | Classic 3 cashless? | plan_core | Classic 3 | Direct billing questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 89 | Referral questions | Does Classic 2 require referral? | plan_core | Classic 2 | Referral questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 90 | Referral questions | Classic 2 referral | plan_core | Classic 2 | Referral questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 91 | Referral questions | referral for Classic 2 | plan_core | Classic 2 | Referral questions deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 92 | Referral questions | Does Classic 3 require referral? | plan_core | Classic 3 | Referral questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 93 | Referral questions | Classic 3 referral | plan_core | Classic 3 | Referral questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 94 | Referral questions | referral for Classic 3 | plan_core | Classic 3 | Referral questions deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 95 | Unsupported-safe boundary questions | What is the dental coverage for Classic 2? | unsupported | unsupported | Safe unsupported fallback | intent=unsupported, plan=Classic 2, behavior=safe_unsupported | PASS | - |
| 96 | Unsupported-safe boundary questions | What is the dental coverage for Classic 3? | unsupported | unsupported | Safe unsupported fallback | intent=plan_core, plan=Classic 3, behavior=supported_response | FAIL | regression risk |
| 97 | Unsupported-safe boundary questions | Tell me about Classic 4 | unsupported | unsupported | Safe unsupported fallback | intent=unsupported, plan=None, behavior=safe_unsupported | PASS | - |
| 98 | Unsupported-safe boundary questions | هل فيه direct billing؟ | unsupported | unsupported | Safe unsupported fallback | intent=unsupported, plan=None, behavior=safe_unsupported | PASS | - |
| 99 | Unsupported-safe boundary questions | هل يحتاج referral؟ | unsupported | unsupported | Safe unsupported fallback | intent=unsupported, plan=None, behavior=safe_unsupported | PASS | - |
| 100 | Unsupported-safe boundary questions | classic2? | unsupported | unsupported | Safe unsupported fallback | intent=unsupported, plan=Classic 2, behavior=safe_unsupported | PASS | - |
| 101 | Unsupported-safe boundary questions | classic3? | unsupported | unsupported | Safe unsupported fallback | intent=unsupported, plan=Classic 3, behavior=safe_unsupported | PASS | - |
| 102 | Unsupported-safe boundary questions | Summarize Prime 1 | unsupported | unsupported | Safe unsupported fallback | intent=unsupported, plan=None, behavior=safe_unsupported | PASS | - |
| 103 | Data gap questions | What is the maternity cover for Classic 2? | unsupported | unsupported | Do not synthesize missing fields; safe fallback | intent=unsupported, plan=Classic 2, behavior=safe_unsupported | PASS | - |
| 104 | Data gap questions | What is the maternity cover for Classic 3? | unsupported | unsupported | Do not synthesize missing fields; safe fallback | intent=unsupported, plan=Classic 3, behavior=safe_unsupported | PASS | - |
| 105 | Data gap questions | What is pharmacy cover summary for Classic 2? | unsupported | unsupported | Do not synthesize missing fields; safe fallback | intent=plan_summary, plan=Classic 2, behavior=supported_response | FAIL | regression risk |
| 106 | Data gap questions | What is pharmacy cover summary for Classic 3? | unsupported | unsupported | Do not synthesize missing fields; safe fallback | intent=plan_summary, plan=Classic 3, behavior=supported_response | FAIL | regression risk |
| 107 | Data gap questions | What is physiotherapy cover summary for Classic 2? | unsupported | unsupported | Do not synthesize missing fields; safe fallback | intent=plan_summary, plan=Classic 2, behavior=supported_response | FAIL | regression risk |
| 108 | Data gap questions | What is physiotherapy cover summary for Classic 3? | unsupported | unsupported | Do not synthesize missing fields; safe fallback | intent=plan_summary, plan=Classic 3, behavior=supported_response | FAIL | regression risk |
| 109 | Demo-style questions | Summarize Classic 2 | plan_summary | Classic 2 | Demo-safe deterministic response | intent=plan_summary, plan=Classic 2, behavior=supported_response | PASS | - |
| 110 | Demo-style questions | Summarize Classic 3 | plan_summary | Classic 3 | Demo-safe deterministic response | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 111 | Demo-style questions | What is the annual limit for Classic 2? | plan_core | Classic 2 | Demo-safe deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 112 | Demo-style questions | What is the annual limit for Classic 3? | plan_core | Classic 3 | Demo-safe deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 113 | Demo-style questions | What is the network name for Classic 2? | plan_core | Classic 2 | Demo-safe deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 114 | Demo-style questions | What is the network name for Classic 3? | plan_core | Classic 3 | Demo-safe deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 115 | Existing Remedy comparison regression | compare Remedy 02 and Remedy 03 | plan_comparison | Remedy 02 vs Remedy 03 | Existing comparison should still work | intent=plan_comparison, plan=Remedy 02 vs Remedy 03, behavior=comparison_result | PASS | - |
| 116 | Existing Remedy comparison regression | compare Remedy 03 and Remedy 04 | plan_comparison | Remedy 03 vs Remedy 04 | Existing comparison should still work | intent=plan_comparison, plan=Remedy 03 vs Remedy 04, behavior=comparison_result | PASS | - |
| 117 | Existing Remedy comparison regression | compare Classic 3 and Remedy 04 | plan_comparison | blocked | Enhanced comparison stays blocked safely | intent=plan_comparison, plan=Remedy 04 vs Classic 3, behavior=comparison_blocked_safe | PASS | - |
| 118 | Broker asking quickly | Please share summary for Classic 2 | plan_summary | Classic 2 | Quick broker deterministic response | intent=plan_summary, plan=Classic 2, behavior=supported_response | PASS | - |
| 119 | Broker asking quickly | Need annual limit for Classic 2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 120 | Broker asking quickly | Need network for Classic 2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 121 | Broker asking quickly | Need area coverage for Classic 2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 122 | Broker asking quickly | Need direct billing for Classic 2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 123 | Broker asking quickly | Need referral status for Classic 2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 124 | Broker asking quickly | Please share summary for Classic 3 | plan_summary | Classic 3 | Quick broker deterministic response | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 125 | Broker asking quickly | Need annual limit for Classic 3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 126 | Broker asking quickly | Need network for Classic 3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 127 | Broker asking quickly | Need area coverage for Classic 3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 128 | Broker asking quickly | Need direct billing for Classic 3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 129 | Broker asking quickly | Need referral status for Classic 3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 130 | Broker asking quickly | Please share summary for classic2 | plan_summary | Classic 2 | Quick broker deterministic response | intent=plan_summary, plan=Classic 2, behavior=supported_response | PASS | - |
| 131 | Broker asking quickly | Need annual limit for classic2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 132 | Broker asking quickly | Need network for classic2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 133 | Broker asking quickly | Need area coverage for classic2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 134 | Broker asking quickly | Need direct billing for classic2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 135 | Broker asking quickly | Need referral status for classic2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 136 | Broker asking quickly | Please share summary for classic3 | plan_summary | Classic 3 | Quick broker deterministic response | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 137 | Broker asking quickly | Need annual limit for classic3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 138 | Broker asking quickly | Need network for classic3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 139 | Broker asking quickly | Need area coverage for classic3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 140 | Broker asking quickly | Need direct billing for classic3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 141 | Broker asking quickly | Need referral status for classic3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 142 | Broker asking quickly | Please share summary for HN Classic 2 | plan_summary | Classic 2 | Quick broker deterministic response | intent=plan_summary, plan=Classic 2, behavior=supported_response | PASS | - |
| 143 | Broker asking quickly | Need annual limit for HN Classic 2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 144 | Broker asking quickly | Need network for HN Classic 2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 145 | Broker asking quickly | Need area coverage for HN Classic 2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 146 | Broker asking quickly | Need direct billing for HN Classic 2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 147 | Broker asking quickly | Need referral status for HN Classic 2 | plan_core | Classic 2 | Quick broker deterministic response | intent=plan_core, plan=Classic 2, behavior=supported_response | PASS | - |
| 148 | Broker asking quickly | Please share summary for HN Classic 3 | plan_summary | Classic 3 | Quick broker deterministic response | intent=plan_summary, plan=Classic 3, behavior=supported_response | PASS | - |
| 149 | Broker asking quickly | Need annual limit for HN Classic 3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 150 | Broker asking quickly | Need network for HN Classic 3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 151 | Broker asking quickly | Need area coverage for HN Classic 3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 152 | Broker asking quickly | Need direct billing for HN Classic 3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |
| 153 | Broker asking quickly | Need referral status for HN Classic 3 | plan_core | Classic 3 | Quick broker deterministic response | intent=plan_core, plan=Classic 3, behavior=supported_response | PASS | - |

## Failed Cases
- #96 What is the dental coverage for Classic 3? -> regression risk ()
- #105 What is pharmacy cover summary for Classic 2? -> regression risk ()
- #106 What is pharmacy cover summary for Classic 3? -> regression risk ()
- #107 What is physiotherapy cover summary for Classic 2? -> regression risk ()
- #108 What is physiotherapy cover summary for Classic 3? -> regression risk ()
