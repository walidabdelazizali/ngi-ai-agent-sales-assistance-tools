# Data Expansion Batch 2B Plan

## Selected Plan
- Remedy 05 (Elite)

## Scope
- Add Remedy 05 with deterministic, source-supported fields only.
- Fields: plan_name, plan_code, medical_network, annual_limit, area_of_coverage, referral_required, direct_billing

## Data Sources
- output/HN-REMEDY-5.json (structured plan data)
- data/plans/plan_network_mapping.csv (plan to network mapping)

## Validation Steps
- Validate deterministic CLI queries for all fields
- Run smoke test and pytest for regression safety
- Update data_coverage_matrix.md and data_validation_notes.md

## Approval Criteria
- All new fields return deterministic values
- No errors or regressions in smoke test or pytest
- Documentation and mapping updated

## Status
- [ ] Validated
- [ ] Regression-safe
- [ ] Ready for next batch
