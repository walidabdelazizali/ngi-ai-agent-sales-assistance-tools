# Internal Rollout Validation Run #1 Results

## Method
All questions executed using:

    python -m src.agent_entrypoint --json "<question>"

## Results Table

| # | Question | Actual JSON Response (truncated/summary) | Detected Intent | Detected Plan | Pass/Partial/Fail | Issue Classification |
|---|----------|------------------------------------------|-----------------|---------------|-------------------|----------------------|
| 1 | What is the annual limit for Remedy 03? | ok: True, annual_limit: 150,000 | plan_core | Remedy 03 | Pass | - |
| 2 | What is the area of coverage for Remedy 04? | ok: True, area_of_coverage: UAE + GCC | plan_core | Remedy 04 | Pass | - |
| 3 | Does Remedy 05 require a referral? | ok: True, referral_required: True | plan_core | Remedy 05 | Pass | - |
| 4 | What is the network for Remedy 04? | ok: True, network_name: hn_premier | plan_core | Remedy 04 | Pass | - |
| 5 | What is the direct billing status for Remedy 05? | ok: True, direct_billing: True | plan_core | Remedy 05 | Pass | - |
| 6 | What are the reimbursement rules for Remedy 04? | ok: True, reimbursement_scope: emergency, GCC, prior approval | reimbursement_rules | Remedy 04 | Pass | - |
| 7 | Is reimbursement allowed outside UAE for Remedy 05? | ok: True, outside_uae_reimbursement: worldwide (excluding USA), emergency only | reimbursement_rules | Remedy 05 | Pass | - |
| 8 | What documents are required for reimbursement in Remedy 04? | ok: True, reimbursement_documents_required: invoices, medical reports | reimbursement_rules | Remedy 04 | Pass | - |
| 9 | What is the reimbursement basis for Remedy 05? | ok: True, reimbursement_basis: incurred cost/UCR | reimbursement_rules | Remedy 05 | Pass | - |
| 10 | Give me a summary of Remedy 03 | ok: True, summary_text: ... | plan_summary | Remedy 03 | Pass | - |
| 11 | Tell me about Remedy 04 | ok: True, summary_text: ... | plan_summary | Remedy 04 | Pass | - |
| 12 | Plan summary for Remedy 05 | ok: True, summary_text: ... | plan_summary | Remedy 05 | Pass | - |
| 13 | ما هو الحد السنوي لخطة ريميدي 03؟ | ok: True, annual_limit: 150,000 | plan_core | Remedy 03 | Pass | - |
| 14 | ما هي التغطية الجغرافية لخطة ريميدي 04؟ | ok: True, area_of_coverage: الإمارات + الخليج | plan_core | Remedy 04 | Pass | - |
| 15 | هل تتطلب ريميدي 05 إحالة؟ | ok: True, referral_required: True | plan_core | Remedy 05 | Pass | - |
| 16 | ما هي قواعد التعويض لخطة ريميدي 04؟ | ok: True, reimbursement_scope: الطوارئ فقط، الخليج، موافقة مسبقة | reimbursement_rules | Remedy 04 | Pass | - |
| 17 | ما هي المستندات المطلوبة للتعويض في ريميدي 05؟ | ok: True, reimbursement_documents_required: الفواتير، التقارير الطبية | reimbursement_rules | Remedy 05 | Pass | - |
| 18 | اعطني ملخص لخطة ريميدي 04 | ok: True, summary_text: (English text) | plan_summary | Remedy 04 | Partial | Wording issue (Arabic summary returns English text) |
| 19 | What is the dental coverage for Remedy 04? | ok: False, intent: unsupported | unsupported | unsupported | Pass | - |
| 20 | Tell me about Remedy 99 | ok: False, intent: unsupported | unsupported | unsupported | Pass | - |
| 21 | Compare Remedy 03 and Remedy 04 | ok: False, intent: unsupported | unsupported | unsupported | Pass | - |
| 22 | ما هو تغطية الأسنان في ريميدي 05؟ | ok: False, intent: unsupported | unsupported | unsupported | Pass | - |
| 23 | ما الفرق بين الريميدي 2 والريميدي 4؟ | ok: False, intent: unsupported | unsupported | unsupported | Pass | - |

## Summary
- Total questions executed: 23
- Pass: 22
- Partial: 1
- Fail: 0

### Top issue categories
- Wording issue: 1 (Arabic summary returns English summary_text)

### Baseline Acceptability
- Baseline is acceptable for controlled internal use: Yes
- Small patch batch recommended after validation: Yes (for improved Arabic summary wording only)
