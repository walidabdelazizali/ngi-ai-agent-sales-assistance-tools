# Capability Matrix

## Current Presentation Scope

| Capability | Classic 2 | Classic 3 | Remedy 02-06 | Status | Notes |
|---|---|---|---|---|---|
| Plan summary | Yes | Yes | Yes | Stable | Deterministic summary routing and validated output |
| Annual limit lookup | Yes | Yes | Yes | Stable | Core plan field route |
| Network lookup | Yes | Yes | Yes | Stable | Core plan field route |
| Area of coverage | Yes | Yes | Yes | Stable | Core plan field route |
| Direct billing | Yes | Yes | Yes | Stable | Core plan field route |
| Referral detection | Yes | Yes | Yes | Stable | Core plan field route |
| Arabic support | Limited | Strong | Strong | Limited | Arabic is deterministic; plan-less shorthand safely unsupported |
| Shorthand broker support | Limited | Strong | Limited | Limited | Strongest coverage currently for Classic 3 hardening set |
| Comparison support | Limited | Intentionally unsupported for enhanced expansion | Supported for existing approved pairs | Limited | No comparison expansion for enhanced plans |
| Unsupported-safe fallback | Yes | Yes | Yes | Stable | Safe deterministic fallback envelope and wording |

## Status Legend
- Stable: production-demo ready behavior with regression coverage.
- Limited: supported in constrained deterministic patterns.
- Intentionally unsupported: blocked by current scope boundary.
- Future scope: explicit backlog area, not enabled now.

## Deterministic Guarantees
- No probabilistic matching layer.
- No RAG/semantic inference in routing.
- Approval and validation gates enforced before customer-facing answers.
- Internal field leakage blocked in customer-safe output paths.

## Future Scope (Not Enabled)
- Expanded enhanced-plan comparison.
- Broader free-form Arabic intent support without plan mention.
- Additional plan families beyond current approved list.
