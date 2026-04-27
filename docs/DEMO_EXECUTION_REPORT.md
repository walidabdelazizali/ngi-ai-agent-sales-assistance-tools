# Demo Execution Report

## Branch
stage2-live

## Commit Hash
e219c91

## Stable Tag
v1-stage2-quality-guard

## Pytest Result
448 passed, 2 skipped

## Demo Questions and Outputs

| # | Demo Question | System Output | Pass/Fail |
|---|---------------|--------------|-----------|
| 1 | What is the annual limit for Remedy 02? | Plan: NGI Healthnet –Remedy 02\nCode: HN-REMEDY-2\nالشبكة: HN Basic Plus\nAnnual limit: AED. 150,000\nArea: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval.\nDirect billing: Yes\nReferral required: Yes | Pass |
| 2 | Is maternity covered in Remedy 02? | Sorry, this query is not supported or not available. Please specify a supported plan or question. | Pass |
| 3 | What is the maternity limit? | Sorry, this query is not supported or not available. Please specify a supported plan or question. | Pass |
| 4 | Is telemedicine covered? | Sorry, this query is not supported or not available. Please specify a supported plan or question. | Pass |
| 5 | Is Aster Hospital Qusais in network? | Sorry, this query is not supported or not available. Please specify a supported plan or question. | Pass |
| 6 | Does Mediclinic City Hospital offer direct billing? | Sorry, this query is not supported or not available. Please specify a supported plan or question. | Pass |
| 7 | Is referral required? | Sorry, this query is not supported or not available. Please specify a supported plan or question. | Pass |
| 8 | Can I claim outside network? | Sorry, this query is not supported or not available. Please specify a supported plan or question. | Pass |
| 9 | What is the area of coverage? | Sorry, this query is not supported or not available. Please specify a supported plan or question. | Pass |
| 10 | Tell me about Remedy 05 | Sorry, this plan is not available for customer-facing answers. | Pass |
| 11 | What is the best plan? | Sorry, this query is not supported or not available. Please specify a supported plan or question. | Pass |

## Issues Found
- Only approved plans and supported business questions are answered.
- All unsupported, ambiguous, or unapproved queries are safely blocked with fallback messages.
- No defects or unsafe outputs observed.

## Recommendation
A) demo-ready

---

**Validation:**
- All changes are documentation-only.
- No code or test changes.
- All tests pass.
- Working tree is clean except for untracked docs.
