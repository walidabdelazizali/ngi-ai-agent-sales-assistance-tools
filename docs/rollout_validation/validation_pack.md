# Internal Rollout Validation Pack: NGI AI Agent Sales Assistance Tools

## Purpose
A practical, real-usage validation pack for internal controlled rollout. Covers all supported plans/intents, English/Arabic phrasing, and unsupported/out-of-scope queries.

## Structure
- [1] Plan Core Questions
- [2] Reimbursement Rules Questions
- [3] Plan Summary Questions
- [4] Arabic Phrasing Variation
- [5] Unsupported/Out-of-Scope Behavior

For each question:
- **Question**: (as user would ask)
- **Intent**: plan_core | reimbursement_rules | plan_summary | unsupported
- **Plan**: Remedy 03 | Remedy 04 | Remedy 05 | unsupported
- **Expected Good Answer**: (key content/behavior)

---

## [1] Plan Core Questions (English)

| # | Question | Intent | Plan | Expected Good Answer |
|---|----------|--------|------|---------------------|
| 1 | What is the annual limit for Remedy 03? | plan_core | Remedy 03 | Should state annual limit (e.g., "150,000") |
| 2 | What is the area of coverage for Remedy 04? | plan_core | Remedy 04 | Should mention "UAE + GCC" |
| 3 | Does Remedy 05 require a referral? | plan_core | Remedy 05 | Should confirm referral required (True/Yes) |
| 4 | What is the network for Remedy 04? | plan_core | Remedy 04 | Should mention "hn_premier" |
| 5 | What is the direct billing status for Remedy 05? | plan_core | Remedy 05 | Should confirm direct billing (True/Yes) |

## [2] Reimbursement Rules Questions (English)

| # | Question | Intent | Plan | Expected Good Answer |
|---|----------|--------|------|---------------------|
| 1 | What are the reimbursement rules for Remedy 04? | reimbursement_rules | Remedy 04 | Should mention emergency-only, GCC, prior approval, invoices |
| 2 | Is reimbursement allowed outside UAE for Remedy 05? | reimbursement_rules | Remedy 05 | Should mention worldwide (excluding USA), emergency only |
| 3 | What documents are required for reimbursement in Remedy 04? | reimbursement_rules | Remedy 04 | Should mention invoices, medical reports |
| 4 | What is the reimbursement basis for Remedy 05? | reimbursement_rules | Remedy 05 | Should mention incurred cost/UCR |

## [3] Plan Summary Questions (English)

| # | Question | Intent | Plan | Expected Good Answer |
|---|----------|--------|------|---------------------|
| 1 | Give me a summary of Remedy 03 | plan_summary | Remedy 03 | Should provide a summary text with plan name, code, and key fields |
| 2 | Tell me about Remedy 04 | plan_summary | Remedy 04 | Should provide a summary text with plan name, code, and key fields |
| 3 | Plan summary for Remedy 05 | plan_summary | Remedy 05 | Should provide a summary text with plan name, code, and key fields |

## [4] Arabic Phrasing Variation

| # | Question | Intent | Plan | Expected Good Answer |
|---|----------|--------|------|---------------------|
| 1 | ما هو الحد السنوي لخطة ريميدي 03؟ | plan_core | Remedy 03 | Should state annual limit in Arabic |
| 2 | ما هي التغطية الجغرافية لخطة ريميدي 04؟ | plan_core | Remedy 04 | Should mention "الإمارات + الخليج" |
| 3 | هل تتطلب ريميدي 05 إحالة؟ | plan_core | Remedy 05 | Should confirm referral required (True/Yes) in Arabic |
| 4 | ما هي قواعد التعويض لخطة ريميدي 04؟ | reimbursement_rules | Remedy 04 | Should mention emergency-only, GCC, prior approval, invoices in Arabic |
| 5 | ما هي المستندات المطلوبة للتعويض في ريميدي 05؟ | reimbursement_rules | Remedy 05 | Should mention invoices, medical reports in Arabic |
| 6 | اعطني ملخص لخطة ريميدي 04 | plan_summary | Remedy 04 | Should provide summary text in Arabic |

## [5] Unsupported/Out-of-Scope Behavior

| # | Question | Intent | Plan | Expected Good Answer |
|---|----------|--------|------|---------------------|
| 1 | What is the dental coverage for Remedy 04? | unsupported | Remedy 04 | Should return unsupported/"not available" message |
| 2 | Tell me about Remedy 99 | unsupported | unsupported | Should return unsupported/"not available" message |
| 3 | Compare Remedy 03 and Remedy 04 | unsupported | unsupported | Should return unsupported/"not available" message |
| 4 | ما هو تغطية الأسنان في ريميدي 05؟ | unsupported | Remedy 05 | Should return unsupported/"not available" message in Arabic |
| 5 | ما الفرق بين الريميدي 2 والريميدي 4؟ | unsupported | unsupported | Should return unsupported/"not available" message in Arabic |

---

## Totals
- English questions: 12
- Arabic questions: 6
- Unsupported/out-of-scope: 5

See issue template for classification guidance.
