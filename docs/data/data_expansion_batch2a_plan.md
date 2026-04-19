# Data Expansion Batch 2A: Remedy 04 Core Deterministic Fields

## Scope
- Deepen Remedy 04 with high-business-value deterministic fields only
- No new plans, no broad expansion

## Selected Fields
- annual_limit
- area_of_coverage
- referral_required
- direct_billing

## Rationale
- These fields are present in the source Table of Benefits for Remedy 04
- All are required for core business queries and are deterministic
- No unsupported or invented values

## Validation
- Each new field must return a deterministic answer for Remedy 04
- No regression for existing plans
