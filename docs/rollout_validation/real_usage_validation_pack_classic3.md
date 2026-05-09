# Real Usage Validation Pack: Classic 3

## Purpose
A realistic insurance-sales replay pack for operational evidence gathering. Covers Classic 3 routing, English and Arabic phrasing, mixed phrasing, short broker-style queries, typo tolerance, and safe unsupported behavior.

## Scope
- Plan: Classic 3 only
- Routing: plan_summary | plan_core | reimbursement_rules | unsupported
- Output: stable JSON envelope and business-friendly text
- No comparison, no new plans, no architecture changes

## Questions

| ID | Category | Question | Expected Intent | Expected Plan | Evidence Target |
|---|---|---|---|---|---|
| 1 | A Summary | classic3 summary | plan_summary | Classic 3 | summary text returned |
| 2 | A Summary | classic-3 summary | plan_summary | Classic 3 | alias resolves |
| 3 | A Summary | Classic 03 summary | plan_summary | Classic 3 | zero-padded alias resolves |
| 4 | A Summary | Summarize HN_CLASSIC_3 | plan_summary | Classic 3 | code alias resolves |
| 5 | A Summary | Summarize HN Classic 3 | plan_summary | Classic 3 | spaced code alias resolves |
| 6 | A Summary | Summarize كلاسيك 3 | plan_summary | Classic 3 | Arabic alias resolves |
| 7 | A Summary | Give me a summary of Classic 3 | plan_summary | Classic 3 | broker-style summary |
| 8 | A Summary | Tell me about Classic 3 | plan_summary | Classic 3 | short summary phrasing |
| 9 | A Summary | Classic 3 overview | plan_summary | Classic 3 | concise English phrasing |
| 10 | A Summary | Plan summary for Classic 3 | plan_summary | Classic 3 | explicit summary query |

| 11 | B Annual Limit | classic3 limit | plan_core | Classic 3 | annual limit returned |
| 12 | B Annual Limit | classic-3 annual limit | plan_core | Classic 3 | alias resolves |
| 13 | B Annual Limit | Classic 03 limit | plan_core | Classic 3 | zero-padded alias resolves |
| 14 | B Annual Limit | What is the annual limit for Classic 3? | plan_core | Classic 3 | exact answer |
| 15 | B Annual Limit | HN_CLASSIC_3 annual limit | plan_core | Classic 3 | code alias resolves |
| 16 | B Annual Limit | HN Classic 3 limit | plan_core | Classic 3 | spaced code alias resolves |
| 17 | B Annual Limit | ليمت كلاسيك 3 | plan_core | Classic 3 | Arabic term maps to annual limit |
| 18 | B Annual Limit | Annual limit Classic 3 | plan_core | Classic 3 | short broker phrasing |
| 19 | B Annual Limit | How much is Classic 3 annual limit? | plan_core | Classic 3 | informal phrasing |
| 20 | B Annual Limit | What is the plan limit for Classic 3? | plan_core | Classic 3 | synonym phrasing |

| 21 | C Network | classic3 network | plan_core | Classic 3 | network returned |
| 22 | C Network | classic-3 network | plan_core | Classic 3 | alias resolves |
| 23 | C Network | Classic 03 network name | plan_core | Classic 3 | zero-padded alias resolves |
| 24 | C Network | What is the network name for Classic 3? | plan_core | Classic 3 | direct query |
| 25 | C Network | شبكة كلاسيك 3 | plan_core | Classic 3 | Arabic network phrasing |
| 26 | C Network | HN_CLASSIC_3 network | plan_core | Classic 3 | code alias resolves |
| 27 | C Network | HN Classic 3 network | plan_core | Classic 3 | mixed alias resolves |
| 28 | C Network | What network is Classic 3 on? | plan_core | Classic 3 | broker-style phrasing |
| 29 | C Network | classic 3 الشبكة | plan_core | Classic 3 | mixed Arabic/English |
| 30 | C Network | Network for Classic 3 | plan_core | Classic 3 | short phrasing |

| 31 | D Area of Coverage | classic3 coverage area | plan_core | Classic 3 | area returned |
| 32 | D Area of Coverage | classic-3 area of coverage | plan_core | Classic 3 | alias resolves |
| 33 | D Area of Coverage | Classic 03 coverage | plan_core | Classic 3 | zero-padded alias resolves |
| 34 | D Area of Coverage | What is the area of coverage for Classic 3? | plan_core | Classic 3 | direct query |
| 35 | D Area of Coverage | تغطية كلاسيك 3 | plan_core | Classic 3 | Arabic coverage phrasing |
| 36 | D Area of Coverage | Classic 3 coverage area | plan_core | Classic 3 | mixed phrasing |
| 37 | D Area of Coverage | HN_CLASSIC_3 coverage | plan_core | Classic 3 | code alias resolves |
| 38 | D Area of Coverage | HN Classic 3 area of coverage | plan_core | Classic 3 | mixed code alias resolves |
| 39 | D Area of Coverage | What countries are covered by Classic 3? | plan_core | Classic 3 | practical sales phrasing |
| 40 | D Area of Coverage | Is Classic 3 valid in UAE and home country? | plan_core | Classic 3 | natural question |

| 41 | E Direct Billing | does classic 3 have direct billing? | plan_core | Classic 3 | direct billing returned |
| 42 | E Direct Billing | classic3 direct billing | plan_core | Classic 3 | alias resolves |
| 43 | E Direct Billing | classic-3 direct billing available? | plan_core | Classic 3 | alias resolves |
| 44 | E Direct Billing | هل فيه direct billing؟ | plan_core | Classic 3 | Arabic mixed phrase |
| 45 | E Direct Billing | هل كلاسيك 3 فيه direct billing؟ | plan_core | Classic 3 | Arabic mixed phrase |
| 46 | E Direct Billing | HN_CLASSIC_3 direct billing | plan_core | Classic 3 | code alias resolves |
| 47 | E Direct Billing | HN Classic 3 direct billing | plan_core | Classic 3 | spaced alias resolves |
| 48 | E Direct Billing | direct billing Classic 3 | plan_core | Classic 3 | short broker phrasing |
| 49 | E Direct Billing | Is direct billing available for Classic 3? | plan_core | Classic 3 | explicit phrasing |
| 50 | E Direct Billing | Classic 3 cashless? | plan_core | Classic 3 | broker shorthand |

| 51 | F Referral | does classic 3 require referral? | plan_core | Classic 3 | referral returned |
| 52 | F Referral | classic3 referral | plan_core | Classic 3 | alias resolves |
| 53 | F Referral | classic-3 referral required? | plan_core | Classic 3 | alias resolves |
| 54 | F Referral | هل يحتاج referral؟ | plan_core | Classic 3 | Arabic mixed phrase |
| 55 | F Referral | هل كلاسيك 3 يحتاج referral؟ | plan_core | Classic 3 | Arabic mixed phrase |
| 56 | F Referral | HN_CLASSIC_3 referral | plan_core | Classic 3 | code alias resolves |
| 57 | F Referral | HN Classic 3 needs referral? | plan_core | Classic 3 | mixed code alias resolves |
| 58 | F Referral | referral for Classic 3 | plan_core | Classic 3 | short broker phrasing |
| 59 | F Referral | Is referral needed for Classic 3? | plan_core | Classic 3 | explicit phrasing |
| 60 | F Referral | Classic 3 need approval referral? | plan_core | Classic 3 | broker shorthand |

| 61 | G Arabic-only | ملخص كلاسيك 3 | plan_summary | Classic 3 | Arabic summary |
| 62 | G Arabic-only | ما هو الحد السنوي لكلاسيك 3؟ | plan_core | Classic 3 | Arabic annual limit |
| 63 | G Arabic-only | ما هي الشبكة لكلاسيك 3؟ | plan_core | Classic 3 | Arabic network |
| 64 | G Arabic-only | ما هي التغطية لكلاسيك 3؟ | plan_core | Classic 3 | Arabic coverage |
| 65 | G Arabic-only | هل فيه دفع مباشر لكلاسيك 3؟ | plan_core | Classic 3 | Arabic direct billing |
| 66 | G Arabic-only | هل يحتاج إحالة كلاسيك 3؟ | plan_core | Classic 3 | Arabic referral |

| 67 | H Mixed Arabic/English | classic 3 الشبكة | plan_core | Classic 3 | mixed routing |
| 68 | H Mixed Arabic/English | classic3 annual limit | plan_core | Classic 3 | mixed routing |
| 69 | H Mixed Arabic/English | كلاسيك 3 coverage | plan_core | Classic 3 | mixed routing |
| 70 | H Mixed Arabic/English | HN classic 3 ليمت | plan_core | Classic 3 | mixed routing |
| 71 | H Mixed Arabic/English | classic 3 summary | plan_summary | Classic 3 | mixed summary |
| 72 | H Mixed Arabic/English | classic 3 direct billing | plan_core | Classic 3 | mixed routing |

| 73 | I Short Broker-style | classic3? | plan_summary | Classic 3 | short broker intent |
| 74 | I Short Broker-style | Classic 3 limit please | plan_core | Classic 3 | brief ask |
| 75 | I Short Broker-style | Classic 3 network pls | plan_core | Classic 3 | brief ask |
| 76 | I Short Broker-style | Classic 3 coverage pls | plan_core | Classic 3 | brief ask |
| 77 | I Short Broker-style | Classic 3 direct billing pls | plan_core | Classic 3 | brief ask |
| 78 | I Short Broker-style | Classic 3 referral pls | plan_core | Classic 3 | brief ask |

| 79 | J Typo Tolerance | classic 3 summary | plan_summary | Classic 3 | spaced alias |
| 80 | J Typo Tolerance | classic 03 summary | plan_summary | Classic 3 | zero-padded alias |
| 81 | J Typo Tolerance | classic3 summry | unsupported | unsupported | typo failure recorded |
| 82 | J Typo Tolerance | classic-3 limt | plan_core | Classic 3 | typo-tolerant core phrase |
| 83 | J Typo Tolerance | كلاسيك3 ليمت | plan_core | Classic 3 | Arabic no-space alias |
| 84 | J Typo Tolerance | كلاسيك 03 ملخص | plan_summary | Classic 3 | Arabic zero-padded alias |

## Negative Controls
| ID | Question | Expected Intent | Expected Plan | Notes |
|---|---|---|---|---|
| 85 | What is the dental coverage for Classic 3? | unsupported | Classic 3 | should fail safely |
| 86 | Compare Classic 3 and Remedy 04 | unsupported | unsupported | comparison must stay blocked |
| 87 | Tell me about Classic 4 | unsupported | unsupported | no new plans |
| 88 | What is the annual limit for Remedy 99? | unsupported | unsupported | safe fallback |

## Expected Evidence Targets
- Correct plan resolution: Classic 3 for supported variations
- Correct intent routing: plan_summary or plan_core as appropriate
- No unsupported failures for supported queries
- Safe unsupported behavior for negative controls
- No raw/internal leakage
- Business-friendly wording
- Stable JSON envelope
- No hallucinated values

## Notes
- This pack is intentionally focused on real sales phrasing and operational evidence.
- Comparison is intentionally excluded.
- Maternity normalization is not synthesized.
