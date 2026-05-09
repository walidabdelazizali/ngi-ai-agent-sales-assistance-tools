# Operational Pressure 200 Delta

## Count Delta vs Existing 100-Query Evidence Pack
- GOOD: 71 -> 111 (delta +40)
- REVIEW: 16 -> 22 (delta +6)
- BLOCKED_OK: 8 -> 66 (delta +58)
- GAP: 5 -> 1 (delta -4)

## Provider-Specific Pressure Results
- GOOD: 29
- REVIEW: 17
- BLOCKED_OK: 4
- GAP: 0
- top provider REVIEW patterns: provider_ambiguity_weakness (6), provider_query_routed_to_unsupported (6), provider_alias_or_dataset_weakness (5)

## Enhanced Baseline Pressure Results
- GOOD: 24
- REVIEW: 2
- BLOCKED_OK: 14
- GAP: 0
- enhanced REVIEW/GAP queries: 2

## Unsupported Recommendation Safety Results
- GOOD: 0
- REVIEW: 0
- BLOCKED_OK: 20
- GAP: 0

## Top REVIEW Clusters
- provider_ambiguity_weakness: 7
- provider_query_routed_to_unsupported: 7
- provider_alias_or_dataset_weakness: 6
- enhanced_baseline_routing_or_blocking_weakness: 2

## Top BLOCKED_OK Clusters
- safe_comparison_block: 19
- safe_enhanced_unsupported_benefit_block: 14
- safe_recommendation_block: 13
- safe_broker_vague_block: 9
- safe_pricing_block: 3
- safe_provider_ambiguity_block: 3
- safe_underwriting_block: 3
- safe_business_advice_block: 1
- safe_provider_not_found_block: 1

## Repeated Routing Weaknesses
- total routing weakness records: 7
- Burjeel Hospital network tiers?
- Sharjah hospitals Remedy 6
- Which network is Aster Al Qusais in?
- Which network is Burjeel Specialty Hospital Sharjah in?
- Aster Qusais network ايه؟
- Remedy 6 Sharjah hospitals
- Remedy 6 في دبي فيها providers ايه؟

## Arabic Normalization Weaknesses
- count: 8
- Aster Qusais network ايه؟
- هل Burjeel Hospital داخل الشبكة؟
- هل Royal Hospital داخل الشبكة؟
- هل Unknown Future Hospital داخل الشبكة؟
- في أي شبكة Imaginary Clinic
- المستشفى دي تبع انهي شبكة؟
- Remedy 6 في دبي فيها providers ايه؟
- الشبكة دي تبع برجيل ولا لا؟

## Provider Ambiguity Weaknesses
- count: 5
- Is Burjeel Hospital in the network?
- هل Burjeel Hospital داخل الشبكة؟
- Is Royal Hospital in the network?
- هل Royal Hospital داخل الشبكة؟
- Which network is Aster Hospital in?

## Enhanced Baseline Weaknesses
- count: 2
- coverage Classic 2R
- what countries are covered by Classic 2R?

## Top 10 Operational Failure Patterns
- provider_ambiguity_weakness: 7
- provider_query_routed_to_unsupported: 7
- provider_alias_or_dataset_weakness: 6
- enhanced_baseline_routing_or_blocking_weakness: 2
- unsafe_block_boundary_exposure: 1

## Recommendation for Next Sprint
- Prioritize a narrow hardening sprint for the dominant failure patterns: provider_ambiguity_weakness, provider_query_routed_to_unsupported, provider_alias_or_dataset_weakness. Keep it routing and normalization only, and replay this same 200-pack afterward.
