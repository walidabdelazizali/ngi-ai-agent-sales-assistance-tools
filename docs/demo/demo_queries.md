# Demo Query Pack

Use this pack for broker, executive, and technical demos. All prompts are deterministic-scope prompts with expected route targets.

## A) Executive Demo Queries

| # | Query | Expected Intent | Expected Plan |
|---|---|---|---|
| 1 | Summarize Classic 3 | plan_summary | Classic 3 |
| 2 | What is the annual limit for Classic 3? | plan_core | Classic 3 |
| 3 | What is the network name for Classic 3? | plan_core | Classic 3 |
| 4 | What is the area of coverage for Classic 3? | plan_core | Classic 3 |
| 5 | Is direct billing available for Classic 3? | plan_core | Classic 3 |
| 6 | Does Classic 3 require referral? | plan_core | Classic 3 |

## B) Broker Demo Queries

| # | Query | Expected Intent | Expected Plan |
|---|---|---|---|
| 1 | classic3 summary | plan_summary | Classic 3 |
| 2 | classic3 limit | plan_core | Classic 3 |
| 3 | HN Classic 3 limit | plan_core | Classic 3 |
| 4 | Classic 3 cashless? | plan_core | Classic 3 |
| 5 | classic3 limt | plan_core | Classic 3 |
| 6 | classic-3 limt | plan_core | Classic 3 |

## C) Arabic Demo Queries

| # | Query | Expected Intent | Expected Plan |
|---|---|---|---|
| 1 | ملخص كلاسيك 3 | plan_summary | Classic 3 |
| 2 | ليمت كلاسيك 3 | plan_core | Classic 3 |
| 3 | شبكة كلاسيك 3 | plan_core | Classic 3 |
| 4 | تغطية كلاسيك 3 | plan_core | Classic 3 |
| 5 | هل كلاسيك 3 فيه direct billing؟ | plan_core | Classic 3 |
| 6 | هل كلاسيك 3 يحتاج referral؟ | plan_core | Classic 3 |

## D) Mixed-Language Demo Queries

| # | Query | Expected Intent | Expected Plan |
|---|---|---|---|
| 1 | classic 3 الشبكة | plan_core | Classic 3 |
| 2 | classic3 annual limit | plan_core | Classic 3 |
| 3 | كلاسيك 3 coverage | plan_core | Classic 3 |
| 4 | HN classic 3 ليمت | plan_core | Classic 3 |

## E) Safety-Boundary Examples

| # | Query | Expected Intent | Expected Plan | Expected Behavior |
|---|---|---|---|---|
| 1 | Compare Classic 3 and Remedy 04 | plan_comparison | blocked | Comparison boundary message |
| 2 | Tell me about Classic 4 | unsupported | unsupported | Safe unsupported response |
| 3 | What is the annual limit for Remedy 99? | unsupported | unsupported | Safe unsupported response |

## F) Unsupported-Safe Examples

| # | Query | Expected Intent | Expected Plan | Expected Behavior |
|---|---|---|---|---|
| 1 | هل فيه direct billing؟ | unsupported | unsupported | No plan inference |
| 2 | هل يحتاج referral؟ | unsupported | unsupported | No plan inference |
| 3 | classic3? | unsupported | unsupported | Deterministic fallback |
| 4 | classic3 summry | unsupported | unsupported | Typo-safe fallback |

## Demo Validation Notes
- For supported prompts: `ok=true`, expected `intent`, expected `plan_name`, and no internal leakage fields.
- For unsupported-safe prompts: `intent=unsupported` with stable fallback envelope.
