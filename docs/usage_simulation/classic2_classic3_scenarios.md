# Classic 2 + Classic 3 Usage Simulation Scenarios

## Scope
- Plans: Classic 2, Classic 3
- Comparison: existing Remedy comparison regression checks only
- Mode: simulation and evidence only

## Total Scenarios
- Count: 153

| ID | Category | Query | Expected Intent | Expected Plan | Expected Behavior |
|---|---|---|---|---|---|
| 1 | Broker asking quickly | Classic 2 summary | plan_summary | Classic 2 | Fast summary answer |
| 2 | Broker asking quickly | Classic 2 limit | plan_core | Classic 2 | Annual limit returned |
| 3 | Broker asking quickly | classic2 summary | plan_summary | Classic 2 | Fast summary answer |
| 4 | Broker asking quickly | classic2 limit | plan_core | Classic 2 | Annual limit returned |
| 5 | Broker asking quickly | classic-2 summary | plan_summary | Classic 2 | Fast summary answer |
| 6 | Broker asking quickly | classic-2 limit | plan_core | Classic 2 | Annual limit returned |
| 7 | Broker asking quickly | Classic 02 summary | plan_summary | Classic 2 | Fast summary answer |
| 8 | Broker asking quickly | Classic 02 limit | plan_core | Classic 2 | Annual limit returned |
| 9 | Broker asking quickly | HN_CLASSIC_2 summary | plan_summary | Classic 2 | Fast summary answer |
| 10 | Broker asking quickly | HN_CLASSIC_2 limit | plan_core | Classic 2 | Annual limit returned |
| 11 | Broker asking quickly | HN Classic 2 summary | plan_summary | Classic 2 | Fast summary answer |
| 12 | Broker asking quickly | HN Classic 2 limit | plan_core | Classic 2 | Annual limit returned |
| 13 | Broker asking quickly | Classic 3 summary | plan_summary | Classic 3 | Fast summary answer |
| 14 | Broker asking quickly | Classic 3 limit | plan_core | Classic 3 | Annual limit returned |
| 15 | Broker asking quickly | classic3 summary | plan_summary | Classic 3 | Fast summary answer |
| 16 | Broker asking quickly | classic3 limit | plan_core | Classic 3 | Annual limit returned |
| 17 | Broker asking quickly | classic-3 summary | plan_summary | Classic 3 | Fast summary answer |
| 18 | Broker asking quickly | classic-3 limit | plan_core | Classic 3 | Annual limit returned |
| 19 | Broker asking quickly | Classic 03 summary | plan_summary | Classic 3 | Fast summary answer |
| 20 | Broker asking quickly | Classic 03 limit | plan_core | Classic 3 | Annual limit returned |
| 21 | Broker asking quickly | HN_CLASSIC_3 summary | plan_summary | Classic 3 | Fast summary answer |
| 22 | Broker asking quickly | HN_CLASSIC_3 limit | plan_core | Classic 3 | Annual limit returned |
| 23 | Broker asking quickly | HN Classic 3 summary | plan_summary | Classic 3 | Fast summary answer |
| 24 | Broker asking quickly | HN Classic 3 limit | plan_core | Classic 3 | Annual limit returned |
| 25 | Broker asking quickly | كلاسيك 3 summary | plan_summary | Classic 3 | Fast summary answer |
| 26 | Broker asking quickly | كلاسيك 3 limit | plan_core | Classic 3 | Annual limit returned |
| 27 | Broker asking quickly | كلاسيك3 summary | plan_summary | Classic 3 | Fast summary answer |
| 28 | Broker asking quickly | كلاسيك3 limit | plan_core | Classic 3 | Annual limit returned |
| 29 | HR asking formally | Could you provide a summary for Classic 2? | plan_summary | Classic 2 | Formal deterministic answer |
| 30 | HR asking formally | What is the annual limit for Classic 2? | plan_core | Classic 2 | Formal deterministic answer |
| 31 | HR asking formally | What is the network name for Classic 2? | plan_core | Classic 2 | Formal deterministic answer |
| 32 | HR asking formally | What is the area of coverage for Classic 2? | plan_core | Classic 2 | Formal deterministic answer |
| 33 | HR asking formally | Is direct billing available for Classic 2? | plan_core | Classic 2 | Formal deterministic answer |
| 34 | HR asking formally | Does Classic 2 require referral? | plan_core | Classic 2 | Formal deterministic answer |
| 35 | HR asking formally | Could you provide a summary for Classic 3? | plan_summary | Classic 3 | Formal deterministic answer |
| 36 | HR asking formally | What is the annual limit for Classic 3? | plan_core | Classic 3 | Formal deterministic answer |
| 37 | HR asking formally | What is the network name for Classic 3? | plan_core | Classic 3 | Formal deterministic answer |
| 38 | HR asking formally | What is the area of coverage for Classic 3? | plan_core | Classic 3 | Formal deterministic answer |
| 39 | HR asking formally | Is direct billing available for Classic 3? | plan_core | Classic 3 | Formal deterministic answer |
| 40 | HR asking formally | Does Classic 3 require referral? | plan_core | Classic 3 | Formal deterministic answer |
| 41 | Client asking in simple Arabic | ملخص كلاسيك 3 | plan_summary | Classic 3 | Arabic deterministic route |
| 42 | Client asking in simple Arabic | ليمت كلاسيك 3 | plan_core | Classic 3 | Arabic deterministic route |
| 43 | Client asking in simple Arabic | شبكة كلاسيك 3 | plan_core | Classic 3 | Arabic deterministic route |
| 44 | Client asking in simple Arabic | تغطية كلاسيك 3 | plan_core | Classic 3 | Arabic deterministic route |
| 45 | Client asking in simple Arabic | هل كلاسيك 3 فيه direct billing؟ | plan_core | Classic 3 | Arabic deterministic route |
| 46 | Client asking in simple Arabic | هل كلاسيك 3 يحتاج referral؟ | plan_core | Classic 3 | Arabic deterministic route |
| 47 | Client asking in simple Arabic | ملخص Classic 2 | plan_summary | Classic 2 | Arabic deterministic route |
| 48 | Client asking in simple Arabic | ليمت Classic 2 | plan_core | Classic 2 | Arabic deterministic route |
| 49 | Client asking in simple Arabic | شبكة Classic 2 | plan_core | Classic 2 | Arabic deterministic route |
| 50 | Client asking in simple Arabic | تغطية Classic 2 | plan_core | Classic 2 | Arabic deterministic route |
| 51 | Client asking in simple Arabic | هل Classic 2 فيه direct billing؟ | plan_core | Classic 2 | Arabic deterministic route |
| 52 | Client asking in simple Arabic | هل Classic 2 يحتاج referral؟ | plan_core | Classic 2 | Arabic deterministic route |
| 53 | Mixed Arabic/English | classic 3 الشبكة | plan_core | Classic 3 | Mixed-language deterministic route |
| 54 | Mixed Arabic/English | classic3 annual limit | plan_core | Classic 3 | Mixed-language deterministic route |
| 55 | Mixed Arabic/English | كلاسيك 3 coverage | plan_core | Classic 3 | Mixed-language deterministic route |
| 56 | Mixed Arabic/English | HN classic 3 ليمت | plan_core | Classic 3 | Mixed-language deterministic route |
| 57 | Mixed Arabic/English | classic 2 الشبكة | plan_core | Classic 2 | Mixed-language deterministic route |
| 58 | Mixed Arabic/English | HN classic 2 ليمت | plan_core | Classic 2 | Mixed-language deterministic route |
| 59 | Typos and shorthand | classic3 limt | plan_core | Classic 3 | Typo-tolerant limit shorthand |
| 60 | Typos and shorthand | classic-3 cash less | plan_core | Classic 3 | Cashless shorthand resolved |
| 61 | Typos and shorthand | classic2 limt | plan_core | Classic 2 | Typo-tolerant limit shorthand |
| 62 | Typos and shorthand | classic-2 cash less | plan_core | Classic 2 | Cashless shorthand resolved |
| 63 | Typos and shorthand | classic3 summry | unsupported | unsupported | Safe unsupported fallback for typo summary |
| 64 | Typos and shorthand | classic2 summry | unsupported | unsupported | Safe unsupported fallback for typo summary |
| 65 | Network questions | What is the network for Classic 2? | plan_core | Classic 2 | Network questions deterministic response |
| 66 | Network questions | Classic 2 network | plan_core | Classic 2 | Network questions deterministic response |
| 67 | Network questions | network name Classic 2 | plan_core | Classic 2 | Network questions deterministic response |
| 68 | Network questions | What is the network for Classic 3? | plan_core | Classic 3 | Network questions deterministic response |
| 69 | Network questions | Classic 3 network | plan_core | Classic 3 | Network questions deterministic response |
| 70 | Network questions | network name Classic 3 | plan_core | Classic 3 | Network questions deterministic response |
| 71 | Annual limit questions | What is the annual limit for Classic 2? | plan_core | Classic 2 | Annual limit questions deterministic response |
| 72 | Annual limit questions | Classic 2 limit | plan_core | Classic 2 | Annual limit questions deterministic response |
| 73 | Annual limit questions | annual limit Classic 2 | plan_core | Classic 2 | Annual limit questions deterministic response |
| 74 | Annual limit questions | What is the annual limit for Classic 3? | plan_core | Classic 3 | Annual limit questions deterministic response |
| 75 | Annual limit questions | Classic 3 limit | plan_core | Classic 3 | Annual limit questions deterministic response |
| 76 | Annual limit questions | annual limit Classic 3 | plan_core | Classic 3 | Annual limit questions deterministic response |
| 77 | Coverage area questions | What is the area of coverage for Classic 2? | plan_core | Classic 2 | Coverage area questions deterministic response |
| 78 | Coverage area questions | Classic 2 coverage | plan_core | Classic 2 | Coverage area questions deterministic response |
| 79 | Coverage area questions | coverage area Classic 2 | plan_core | Classic 2 | Coverage area questions deterministic response |
| 80 | Coverage area questions | What is the area of coverage for Classic 3? | plan_core | Classic 3 | Coverage area questions deterministic response |
| 81 | Coverage area questions | Classic 3 coverage | plan_core | Classic 3 | Coverage area questions deterministic response |
| 82 | Coverage area questions | coverage area Classic 3 | plan_core | Classic 3 | Coverage area questions deterministic response |
| 83 | Direct billing questions | Is direct billing available for Classic 2? | plan_core | Classic 2 | Direct billing questions deterministic response |
| 84 | Direct billing questions | Classic 2 direct billing | plan_core | Classic 2 | Direct billing questions deterministic response |
| 85 | Direct billing questions | Classic 2 cashless? | plan_core | Classic 2 | Direct billing questions deterministic response |
| 86 | Direct billing questions | Is direct billing available for Classic 3? | plan_core | Classic 3 | Direct billing questions deterministic response |
| 87 | Direct billing questions | Classic 3 direct billing | plan_core | Classic 3 | Direct billing questions deterministic response |
| 88 | Direct billing questions | Classic 3 cashless? | plan_core | Classic 3 | Direct billing questions deterministic response |
| 89 | Referral questions | Does Classic 2 require referral? | plan_core | Classic 2 | Referral questions deterministic response |
| 90 | Referral questions | Classic 2 referral | plan_core | Classic 2 | Referral questions deterministic response |
| 91 | Referral questions | referral for Classic 2 | plan_core | Classic 2 | Referral questions deterministic response |
| 92 | Referral questions | Does Classic 3 require referral? | plan_core | Classic 3 | Referral questions deterministic response |
| 93 | Referral questions | Classic 3 referral | plan_core | Classic 3 | Referral questions deterministic response |
| 94 | Referral questions | referral for Classic 3 | plan_core | Classic 3 | Referral questions deterministic response |
| 95 | Unsupported-safe boundary questions | What is the dental coverage for Classic 2? | unsupported | unsupported | Safe unsupported fallback |
| 96 | Unsupported-safe boundary questions | What is the dental coverage for Classic 3? | unsupported | unsupported | Safe unsupported fallback |
| 97 | Unsupported-safe boundary questions | Tell me about Classic 4 | unsupported | unsupported | Safe unsupported fallback |
| 98 | Unsupported-safe boundary questions | هل فيه direct billing؟ | unsupported | unsupported | Safe unsupported fallback |
| 99 | Unsupported-safe boundary questions | هل يحتاج referral؟ | unsupported | unsupported | Safe unsupported fallback |
| 100 | Unsupported-safe boundary questions | classic2? | unsupported | unsupported | Safe unsupported fallback |
| 101 | Unsupported-safe boundary questions | classic3? | unsupported | unsupported | Safe unsupported fallback |
| 102 | Unsupported-safe boundary questions | Summarize Prime 1 | unsupported | unsupported | Safe unsupported fallback |
| 103 | Data gap questions | What is the maternity cover for Classic 2? | unsupported | unsupported | Do not synthesize missing fields; safe fallback |
| 104 | Data gap questions | What is the maternity cover for Classic 3? | unsupported | unsupported | Do not synthesize missing fields; safe fallback |
| 105 | Data gap questions | What is pharmacy cover summary for Classic 2? | unsupported | unsupported | Do not synthesize missing fields; safe fallback |
| 106 | Data gap questions | What is pharmacy cover summary for Classic 3? | unsupported | unsupported | Do not synthesize missing fields; safe fallback |
| 107 | Data gap questions | What is physiotherapy cover summary for Classic 2? | unsupported | unsupported | Do not synthesize missing fields; safe fallback |
| 108 | Data gap questions | What is physiotherapy cover summary for Classic 3? | unsupported | unsupported | Do not synthesize missing fields; safe fallback |
| 109 | Demo-style questions | Summarize Classic 2 | plan_summary | Classic 2 | Demo-safe deterministic response |
| 110 | Demo-style questions | Summarize Classic 3 | plan_summary | Classic 3 | Demo-safe deterministic response |
| 111 | Demo-style questions | What is the annual limit for Classic 2? | plan_core | Classic 2 | Demo-safe deterministic response |
| 112 | Demo-style questions | What is the annual limit for Classic 3? | plan_core | Classic 3 | Demo-safe deterministic response |
| 113 | Demo-style questions | What is the network name for Classic 2? | plan_core | Classic 2 | Demo-safe deterministic response |
| 114 | Demo-style questions | What is the network name for Classic 3? | plan_core | Classic 3 | Demo-safe deterministic response |
| 115 | Existing Remedy comparison regression | compare Remedy 02 and Remedy 03 | plan_comparison | Remedy 02 vs Remedy 03 | Existing comparison should still work |
| 116 | Existing Remedy comparison regression | compare Remedy 03 and Remedy 04 | plan_comparison | Remedy 03 vs Remedy 04 | Existing comparison should still work |
| 117 | Existing Remedy comparison regression | compare Classic 3 and Remedy 04 | plan_comparison | blocked | Enhanced comparison stays blocked safely |
| 118 | Broker asking quickly | Please share summary for Classic 2 | plan_summary | Classic 2 | Quick broker deterministic response |
| 119 | Broker asking quickly | Need annual limit for Classic 2 | plan_core | Classic 2 | Quick broker deterministic response |
| 120 | Broker asking quickly | Need network for Classic 2 | plan_core | Classic 2 | Quick broker deterministic response |
| 121 | Broker asking quickly | Need area coverage for Classic 2 | plan_core | Classic 2 | Quick broker deterministic response |
| 122 | Broker asking quickly | Need direct billing for Classic 2 | plan_core | Classic 2 | Quick broker deterministic response |
| 123 | Broker asking quickly | Need referral status for Classic 2 | plan_core | Classic 2 | Quick broker deterministic response |
| 124 | Broker asking quickly | Please share summary for Classic 3 | plan_summary | Classic 3 | Quick broker deterministic response |
| 125 | Broker asking quickly | Need annual limit for Classic 3 | plan_core | Classic 3 | Quick broker deterministic response |
| 126 | Broker asking quickly | Need network for Classic 3 | plan_core | Classic 3 | Quick broker deterministic response |
| 127 | Broker asking quickly | Need area coverage for Classic 3 | plan_core | Classic 3 | Quick broker deterministic response |
| 128 | Broker asking quickly | Need direct billing for Classic 3 | plan_core | Classic 3 | Quick broker deterministic response |
| 129 | Broker asking quickly | Need referral status for Classic 3 | plan_core | Classic 3 | Quick broker deterministic response |
| 130 | Broker asking quickly | Please share summary for classic2 | plan_summary | Classic 2 | Quick broker deterministic response |
| 131 | Broker asking quickly | Need annual limit for classic2 | plan_core | Classic 2 | Quick broker deterministic response |
| 132 | Broker asking quickly | Need network for classic2 | plan_core | Classic 2 | Quick broker deterministic response |
| 133 | Broker asking quickly | Need area coverage for classic2 | plan_core | Classic 2 | Quick broker deterministic response |
| 134 | Broker asking quickly | Need direct billing for classic2 | plan_core | Classic 2 | Quick broker deterministic response |
| 135 | Broker asking quickly | Need referral status for classic2 | plan_core | Classic 2 | Quick broker deterministic response |
| 136 | Broker asking quickly | Please share summary for classic3 | plan_summary | Classic 3 | Quick broker deterministic response |
| 137 | Broker asking quickly | Need annual limit for classic3 | plan_core | Classic 3 | Quick broker deterministic response |
| 138 | Broker asking quickly | Need network for classic3 | plan_core | Classic 3 | Quick broker deterministic response |
| 139 | Broker asking quickly | Need area coverage for classic3 | plan_core | Classic 3 | Quick broker deterministic response |
| 140 | Broker asking quickly | Need direct billing for classic3 | plan_core | Classic 3 | Quick broker deterministic response |
| 141 | Broker asking quickly | Need referral status for classic3 | plan_core | Classic 3 | Quick broker deterministic response |
| 142 | Broker asking quickly | Please share summary for HN Classic 2 | plan_summary | Classic 2 | Quick broker deterministic response |
| 143 | Broker asking quickly | Need annual limit for HN Classic 2 | plan_core | Classic 2 | Quick broker deterministic response |
| 144 | Broker asking quickly | Need network for HN Classic 2 | plan_core | Classic 2 | Quick broker deterministic response |
| 145 | Broker asking quickly | Need area coverage for HN Classic 2 | plan_core | Classic 2 | Quick broker deterministic response |
| 146 | Broker asking quickly | Need direct billing for HN Classic 2 | plan_core | Classic 2 | Quick broker deterministic response |
| 147 | Broker asking quickly | Need referral status for HN Classic 2 | plan_core | Classic 2 | Quick broker deterministic response |
| 148 | Broker asking quickly | Please share summary for HN Classic 3 | plan_summary | Classic 3 | Quick broker deterministic response |
| 149 | Broker asking quickly | Need annual limit for HN Classic 3 | plan_core | Classic 3 | Quick broker deterministic response |
| 150 | Broker asking quickly | Need network for HN Classic 3 | plan_core | Classic 3 | Quick broker deterministic response |
| 151 | Broker asking quickly | Need area coverage for HN Classic 3 | plan_core | Classic 3 | Quick broker deterministic response |
| 152 | Broker asking quickly | Need direct billing for HN Classic 3 | plan_core | Classic 3 | Quick broker deterministic response |
| 153 | Broker asking quickly | Need referral status for HN Classic 3 | plan_core | Classic 3 | Quick broker deterministic response |
