# Data Expansion Batch 1: Remedy 04 (Premier)

## Scope
- Add Remedy 04 plan family (Premier)
- Add to plan_network_mapping.csv
- Add minimal network mapping for Remedy 04 (hn_premier)
- No broad schema or parser changes

## Rationale
- Highest business value: Premier plan is a common upsell and requested by brokers
- Smallest safe scope: Only one plan, no mass ingestion
- Easiest validation: Follows existing plan structure
- Fits current runtime/query design

## Data Sources
- Plan code: HN-REMEDY-4
- Plan name: Remedy 04
- Network: hn_premier
- Table of Benefits: [pending full doc extraction]

## Validation
- Plan appears in plan_network_mapping.csv
- Queries for Remedy 04 return correct network
- No regression for existing plans
