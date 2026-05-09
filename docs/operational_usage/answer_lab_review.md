# Answer Lab Manual Review

## Scope
- Review target: docs/operational_usage/answer_lab_results.md
- Mode: documentation and evaluation only
- Runtime changes: none
- Comparison enablement: none

## Source Surfaces Reviewed
- Classic 2 source table: data/plans/raw/HN_CLASSIC_2/source_table.json
- Classic 3 source table: data/plans/raw/HN_CLASSIC_3/source_table.json
- Current approved core contract: src/tool_contract.py
- Enhanced plan parsing: src/tools/enhanced_plan_loader.py

## Review Summary
- Business-ready now: Classic 2 and Classic 3 core-field answers for annual limit, network, area of coverage, direct billing, and summary-level core display.
- Blocked intentionally: enhanced comparison involving Classic 3 remains correctly blocked.
- Future normalization candidates: Classic 3 pharmacy and maternity. Source evidence exists in the Classic 3 source table, but current routing and customer-safe contract do not expose those fields for these queries.
- Source limitation: Classic 2 source table currently contains only core fields, so no pharmacy or maternity answer should be expected from source-backed evidence today.

## Detailed Review

### 1. classic3 limit
- Query: classic3 limit
- System status: GOOD
- System answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Source evidence available?: Yes. Classic 3 source table includes annual_limit=AED 250,000, provider_network=HN Standard, area_of_coverage=UAE+Home country, and direct_billing marker.
- Review outcome: Correct
- Reviewer notes: The returned annual limit matches current normalized Classic 3 core fields.
- Recommended future action: None.

### 2. classic2 cashless?
- Query: classic2 cashless?
- System status: GOOD
- System answer:
  Plan: Classic 2
  Code: HN_CLASSIC_2
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Source evidence available?: Yes for direct billing and other core fields. Classic 2 source table contains Direct Billing Available=Yes, Provider Network=HN Standard Plus, Maximum Benefit Per Year=AED 250,000, and Area of Coverage=Worldwide Excluding USA and Canada.
- Review outcome: Correct
- Reviewer notes: "Cashless" is being answered through the approved direct-billing core field, which is consistent with current deterministic behavior.
- Recommended future action: None.

### 3. شبكة كلاسيك 3
- Query: شبكة كلاسيك 3
- System status: GOOD
- System answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Source evidence available?: Yes. Classic 3 source table contains provider_network=HN Standard, which normalizes to Standard.
- Review outcome: Correct
- Reviewer notes: The answer includes extra approved core fields, but the network value itself is correct.
- Recommended future action: None.

### 4. What is the area of coverage for Classic 2?
- Query: What is the area of coverage for Classic 2?
- System status: GOOD
- System answer:
  Plan: Classic 2
  Code: HN_CLASSIC_2
  الشبكة: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Source evidence available?: Yes. Classic 2 source table explicitly contains Area of Coverage=Worldwide Excluding USA and Canada.
- Review outcome: Correct
- Reviewer notes: The returned area value matches current source-backed Classic 2 core data.
- Recommended future action: None.

### 5. Compare Classic 3 and Remedy 04
- Query: Compare Classic 3 and Remedy 04
- System status: BLOCKED_OK
- System answer:
  Sorry, comparison is not supported or not available for one or both plans.
- Source evidence available?: Not applicable for answer correctness. This is a policy boundary, not a source-data lookup.
- Review outcome: Blocked OK
- Reviewer notes: Enhanced comparison remains intentionally blocked. This matches current system policy and should not be treated as a defect.
- Recommended future action: None unless comparison expansion is explicitly approved in a separate sprint.

### 6. Summarize Classic 3
- Query: Summarize Classic 3
- System status: GOOD
- System answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  Network: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Source evidence available?: Yes for network, annual limit, area of coverage, and direct billing. Referral is currently defaulted to No in the enhanced parser rather than extracted from an explicit Classic 3 source field.
- Review outcome: Correct
- Reviewer notes: Summary is correct for the currently approved core field set. Referral should be treated as contract-valid but source-light.
- Recommended future action: Add explicit referral sourcing only if a future source-backed field becomes available.

### 7. Summarize Classic 2
- Query: Summarize Classic 2
- System status: GOOD
- System answer:
  Plan: Classic 2
  Code: HN_CLASSIC_2
  Network: Standard Plus
  Annual limit: AED 250,000
  Area: Worldwide Excluding USA and Canada
  Direct billing: Yes
  Referral required: No
- Source evidence available?: Yes for network, annual limit, area of coverage, and direct billing. Referral is currently defaulted to No in the enhanced parser rather than extracted from an explicit Classic 2 source field.
- Review outcome: Correct
- Reviewer notes: Summary aligns with the current approved Classic 2 core contract.
- Recommended future action: Add explicit referral sourcing only if future source documentation supports it.

### 8. هل كلاسيك 3 يحتاج referral؟
- Query: هل كلاسيك 3 يحتاج referral؟
- System status: GOOD
- System answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Source evidence available?: Partial. The answer matches the current approved core contract, but the Classic 3 source table does not show an explicit referral field; the parser defaults referral_required to False.
- Review outcome: Partial
- Reviewer notes: Acceptable for internal demo/business review under the current contract, but this specific value would benefit from source-backed verification before being treated as fully evidenced.
- Recommended future action: Needs Source Verification for referral_required on Classic 3.

### 9. هل كلاسيك 3 فيه direct billing؟
- Query: هل كلاسيك 3 فيه direct billing؟
- System status: GOOD
- System answer:
  Plan: Classic 3
  Code: HN_CLASSIC_3
  الشبكة: Standard
  Annual limit: AED 250,000
  Area: UAE+Home country
  Direct billing: Yes
  Referral required: No
- Source evidence available?: Yes. Classic 3 source table includes direct_billing=Direct Billing Available.
- Review outcome: Correct
- Reviewer notes: The direct billing answer is supported by source and matches the approved core field contract.
- Recommended future action: None.

### 10. pharmacy Classic 3
- Query: pharmacy Classic 3
- System status: REVIEW
- System answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Source evidence available?: Yes. Classic 3 source table contains outpatient_benefits.pharmacy_limit=AED 10,000, pharmacy_copay=Nil Co Insurance, and pharmacy_type=Branded.
- Review outcome: Data Gap
- Reviewer notes: Source evidence exists, but the current routing/contract path does not expose Classic 3 pharmacy answers for this query. This is not a source absence; it is a normalization and exposure gap.
- Recommended future action: Candidate future normalization for Classic 3 pharmacy fields into a customer-safe answer path. Do not synthesize into runtime without an approved normalization sprint.

### 11. maternity Classic 3
- Query: maternity Classic 3
- System status: REVIEW
- System answer:
  Sorry, this query is not supported or not available. Please specify a supported plan or question.
- Source evidence available?: Yes. Classic 3 source table contains maternity inpatient and outpatient details, including normal_delivery_limit=AED 12,500 and c_section_complications_termination_limit=AED 15,000.
- Review outcome: Data Gap
- Reviewer notes: Source evidence exists, but the current routing/contract path does not expose Classic 3 maternity answers for this query. This is a future normalization candidate, not a runtime bug for the current approved scope.
- Recommended future action: Candidate future normalization for Classic 3 maternity fields into a customer-safe answer path. Do not synthesize into runtime without an approved normalization sprint.

## Ready For Business Use Now
- Classic 2 core answers: annual limit, network, area of coverage, direct billing, and summary-level core display.
- Classic 3 core answers: annual limit, network, area of coverage, direct billing, and summary-level core display.
- Classic 3 comparison boundary: blocked response is working as intended.

## Future Normalization Candidates
- Classic 3 pharmacy benefits
- Classic 3 maternity benefits
- Explicit source-backed referral verification for Classic 2 and Classic 3 if future source material exposes a definitive referral field