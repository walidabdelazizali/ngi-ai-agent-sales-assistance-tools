# Professional Operational Simulation Results

## Run Context
- Source of questions: docs/operational_usage/professional_simulation_pack.md
- Execution path: python -m src.agent_entrypoint --json <query>
- Evaluation mode: documentation only (no runtime changes)

## Summary
- Total queries: 50
- GOOD: 33
- REVIEW: 8
- BLOCKED_OK: 5
- GAP: 4

## Detailed Results
### SECTION A — Broker Fast Questions
#### 1. classic2r limit
- Query: classic2r limit
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 2. cashless Classic 3?
- Query: cashless Classic 3?
- Intent: plan_core
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 3. Which plan is worldwide?
- Query: Which plan is worldwide?
- Intent: unsupported
- Plan: -
- Status: BLOCKED_OK
- Answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Reviewer notes: Recommendation/comparison style request is outside enabled deterministic boundary.

#### 4. Is referral required for Classic 2R?
- Query: Is referral required for Classic 2R?
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 5. Summarize Classic 2
- Query: Summarize Classic 2
- Intent: plan_summary
- Plan: Classic 2
- Status: GOOD
- Answer:
  Plan: Classic 2
  Code: HN_CLASSIC_2
  Network: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 6. Summarize Classic 2R
- Query: Summarize Classic 2R
- Intent: plan_summary
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  Network: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 7. Summarize Classic 3
- Query: Summarize Classic 3
- Intent: plan_summary
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  Network: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 8. Classic 2 network?
- Query: Classic 2 network?
- Intent: plan_core
- Plan: Classic 2
- Status: GOOD
- Answer:
  Plan: Classic 2
  Code: HN_CLASSIC_2
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 9. Classic 2R direct billing?
- Query: Classic 2R direct billing?
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 10. Classic 3 annual limit
- Query: Classic 3 annual limit
- Intent: plan_core
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

### SECTION B — HR Questions
#### 11. What is the area of coverage for Classic 2?
- Query: What is the area of coverage for Classic 2?
- Intent: plan_core
- Plan: Classic 2
- Status: GOOD
- Answer:
  Plan: Classic 2
  Code: HN_CLASSIC_2
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 12. What is the area of coverage for Classic 2R?
- Query: What is the area of coverage for Classic 2R?
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 13. What is the area of coverage for Classic 3?
- Query: What is the area of coverage for Classic 3?
- Intent: plan_core
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 14. Does Classic 2R support direct billing?
- Query: Does Classic 2R support direct billing?
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 15. Does Classic 3 support direct billing?
- Query: Does Classic 3 support direct billing?
- Intent: plan_core
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 16. What is the network name for Classic 2R?
- Query: What is the network name for Classic 2R?
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 17. What is the annual limit for Classic 2R?
- Query: What is the annual limit for Classic 2R?
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 18. Is referral required for Classic 3?
- Query: Is referral required for Classic 3?
- Intent: plan_core
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 19. Which network is better for Dubai?
- Query: Which network is better for Dubai?
- Intent: unsupported
- Plan: -
- Status: REVIEW
- Answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Reviewer notes: Unsupported query; requires manual triage for scope fit or phrasing support.

#### 20. Is there private room coverage for Classic 2R?
- Query: Is there private room coverage for Classic 2R?
- Intent: unsupported
- Plan: Classic 2R
- Status: REVIEW
- Answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Reviewer notes: Unsupported query; requires manual triage for scope fit or phrasing support.

### SECTION C — Client Questions
#### 21. ينفع استخدمها في مصر؟
- Query: ينفع استخدمها في مصر؟
- Intent: unsupported
- Plan: -
- Status: REVIEW
- Answer:
  عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
- Reviewer notes: Unsupported query; requires manual triage for scope fit or phrasing support.

#### 22. هل فيه كاشلس في كلاسيك 3؟
- Query: هل فيه كاشلس في كلاسيك 3؟
- Intent: plan_core
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 23. الشبكة قوية في كلاسيك 2R؟
- Query: الشبكة قوية في كلاسيك 2R؟
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 24. هل لازم referral في كلاسيك 3؟
- Query: هل لازم referral في كلاسيك 3؟
- Intent: plan_core
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 25. هل يغطي الطوارئ في كلاسيك 2R؟
- Query: هل يغطي الطوارئ في كلاسيك 2R؟
- Intent: unsupported
- Plan: Classic 2R
- Status: REVIEW
- Answer:
  عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
- Reviewer notes: Unsupported query; requires manual triage for scope fit or phrasing support.

#### 26. ملخص كلاسيك 2
- Query: ملخص كلاسيك 2
- Intent: unsupported
- Plan: -
- Status: REVIEW
- Answer:
  عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
- Reviewer notes: Unsupported query; requires manual triage for scope fit or phrasing support.

#### 27. ملخص كلاسيك 2R
- Query: ملخص كلاسيك 2R
- Intent: plan_summary
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  Network: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 28. ملخص كلاسيك 3
- Query: ملخص كلاسيك 3
- Intent: plan_summary
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  Network: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 29. ليمت كلاسيك 2R
- Query: ليمت كلاسيك 2R
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 30. تغطية كلاسيك 3
- Query: تغطية كلاسيك 3
- Intent: plan_core
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

### SECTION D — Mixed Arabic/English
#### 31. كلاسيك 2R network?
- Query: كلاسيك 2R network?
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 32. classic3 referral?
- Query: classic3 referral?
- Intent: plan_core
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 33. worldwide classic2?
- Query: worldwide classic2?
- Intent: unsupported
- Plan: Classic 2
- Status: REVIEW
- Answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Reviewer notes: Unsupported query; requires manual triage for scope fit or phrasing support.

#### 34. direct billing في كلاسيك 3؟
- Query: direct billing في كلاسيك 3؟
- Intent: plan_core
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 35. HN Classic 2R ليمت
- Query: HN Classic 2R ليمت
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 36. classic2r area of coverage
- Query: classic2r area of coverage
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 37. شبكة Classic 2R
- Query: شبكة Classic 2R
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 38. Summarize كلاسيك 3
- Query: Summarize كلاسيك 3
- Intent: plan_summary
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  Network: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 39. Classic 2R cashless?
- Query: Classic 2R cashless?
- Intent: plan_core
- Plan: Classic 2R
- Status: GOOD
- Answer:
  Plan: Classic 2R
  Code: HN_CLASSIC_2R
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

#### 40. كلاسيك 3 annual limit
- Query: كلاسيك 3 annual limit
- Intent: plan_core
- Plan: Classic 3
- Status: GOOD
- Answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Reviewer notes: Usable business answer within approved deterministic core scope.

### SECTION E — Boundary & Safety Tests
#### 41. Compare Classic 2R and Classic 3
- Query: Compare Classic 2R and Classic 3
- Intent: plan_comparison
- Plan: -
- Status: BLOCKED_OK
- Answer:
  Comparison is not supported or not available for one or both plans. Please specify two supported plans to compare.
- Reviewer notes: Comparison is intentionally blocked for enhanced plans in current deterministic boundary.

#### 42. maternity Classic 3
- Query: maternity Classic 3
- Intent: unsupported
- Plan: Classic 3
- Status: GAP
- Answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Reviewer notes: Requested benefit data is intentionally unsupported in runtime though present in source structures.

#### 43. pharmacy Classic 2R
- Query: pharmacy Classic 2R
- Intent: unsupported
- Plan: Classic 2R
- Status: GAP
- Answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Reviewer notes: Requested benefit data is intentionally unsupported in runtime though present in source structures.

#### 44. best enhanced plan overall
- Query: best enhanced plan overall
- Intent: unsupported
- Plan: -
- Status: REVIEW
- Answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Reviewer notes: Unsupported query; requires manual triage for scope fit or phrasing support.

#### 45. compare all plans
- Query: compare all plans
- Intent: unsupported
- Plan: -
- Status: BLOCKED_OK
- Answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Reviewer notes: Recommendation/comparison style request is outside enabled deterministic boundary.

#### 46. Compare Classic 2 and Classic 2R
- Query: Compare Classic 2 and Classic 2R
- Intent: plan_comparison
- Plan: Classic 2R vs Classic 2
- Status: BLOCKED_OK
- Answer:
  Sorry, comparison is not supported or not available for one or both plans.
- Reviewer notes: Comparison is intentionally blocked for enhanced plans in current deterministic boundary.

#### 47. Which enhanced plan should I offer?
- Query: Which enhanced plan should I offer?
- Intent: unsupported
- Plan: -
- Status: BLOCKED_OK
- Answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Reviewer notes: Recommendation/comparison style request is outside enabled deterministic boundary.

#### 48. pharmacy Classic 3
- Query: pharmacy Classic 3
- Intent: unsupported
- Plan: Classic 3
- Status: GAP
- Answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Reviewer notes: Requested benefit data is intentionally unsupported in runtime though present in source structures.

#### 49. maternity Classic 2R
- Query: maternity Classic 2R
- Intent: unsupported
- Plan: Classic 2R
- Status: GAP
- Answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Reviewer notes: Requested benefit data is intentionally unsupported in runtime though present in source structures.

#### 50. Tell me about Classic 4
- Query: Tell me about Classic 4
- Intent: unsupported
- Plan: -
- Status: REVIEW
- Answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Reviewer notes: Unsupported query; requires manual triage for scope fit or phrasing support.
