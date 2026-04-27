# Demo Readiness Pack

## 1. Current Stable Baseline
- **Branch:** stage2-live
- **Tag:** v1-stage2-quality-guard
- **Tests:** 448 passed, 2 skipped

## 2. What the System Can Safely Demo
- Deterministic Q&A for approved Remedy plans (02, 03, 04, 05, 06)
- 10 core business questions for approved plans only
- Plan core, reimbursement, and summary queries (English/Arabic)
- Plan comparison for supported pairs
- Consistent, safe, and repeatable answers (no AI, no RAG)
- Robust handling of unsupported or unapproved queries
- Telegram bot startup logic (if dependency installed)

## 3. What the System Must Not Demo Yet
- Any unapproved/draft plan answers
- Unvalidated or AI-generated content
- Custom plan uploads or editing
- Unstable or experimental features
- Telegram bot if python-telegram-bot is not installed
- Any code or feature not covered by tests

## 4. 10 Approved Demo Questions
1. What is the annual limit for Remedy 02?
2. What is the network name for Remedy 03?
3. Is direct billing available in Remedy 04?
4. Is a referral required for Remedy 05?
5. What is the area of coverage for Remedy 06?
6. What are the reimbursement rules for Remedy 02?
7. What documents are required for reimbursement in Remedy 03?
8. Give me a summary of Remedy 04.
9. قارن ريميدي 02 و ريميدي 03
10. ما هي التغطية في ريميدي 05؟

## 5. Safe Fallback Examples
- "Sorry, this plan is not available for customer-facing answers."
- "Sorry, this query is not supported or not available. Please specify a supported plan or question."
- "يرجى تحديد خطتين للمقارنة."
- "هذه الخطة غير متاحة حالياً للإجابة على العملاء."

## 6. Demo Operator Script
1. Confirm you are on branch `stage2-live` and tag `v1-stage2-quality-guard`.
2. Run: `python -m pytest -q` (expect 448 passed, 2 skipped)
3. Open the agent interface (CLI or Telegram, if available)
4. Ask each of the 10 approved demo questions and verify correct, safe, and consistent answers.
5. For unsupported or unapproved queries, verify fallback messages are shown.
6. If Telegram demo is required, ensure `python-telegram-bot` is installed and token is set.
7. Do not attempt any unapproved, upload, or experimental features.

## 7. Rollback Instruction
To restore the stable demo baseline:
```sh
git checkout v1-stage2-quality-guard
```
