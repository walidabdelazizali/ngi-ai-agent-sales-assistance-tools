# Deterministic Insurance Core

## 1) Purpose
This document describes the deterministic insurance decision core used for broker/demo/management use cases. The system is designed to return stable, explainable outputs with strict scope boundaries.

## 2) Canonical Source Layer
- Plan data is loaded from controlled source paths.
- Enhanced plan loading resolves canonical plan names through deterministic aliases.
- Source boundary controls prevent accidental trust in non-authoritative legacy artifacts.
- Source metadata is used internally for validation, not customer-facing output.

## 3) Validation Gates
- Plan payloads pass normalize + validate gates before customer-safe response routes.
- Approval gate enforces customer-facing readiness.
- Required field gate protects deterministic business answers.
- Missing/invalid readiness returns safe fallback, not guessed values.

## 4) Deterministic Routing Layer
- Query intent classification is pattern-based (fixed aliases and keywords).
- No probabilistic NLP model decides routing.
- No embedding similarity or semantic retrieval route selection.
- Supported paths include plan_summary, plan_core, reimbursement_rules, and bounded comparison behavior.

## 5) Enhanced Loader Boundary
- Enhanced plans are resolved by registry and aliases.
- Registry controls supported enhanced scope.
- No implicit expansion to new plan families without explicit integration.

## 6) Approval Boundary
- Only approved and validated plans are eligible for customer-safe outputs.
- Unapproved or out-of-scope requests return deterministic unsupported-safe envelopes.

## 7) No Hallucination Principle
- The system does not generate inferred insurance facts.
- If a supported field is unavailable, fallback behavior is deterministic and explicit.
- Internal metadata is not exposed in business-facing output.

## 8) Unsupported-Safe Fallback
- Unsupported or out-of-scope queries return a stable envelope:
  - ok=false
  - intent=unsupported
  - safe business message
- Plan-less Arabic shorthand remains intentionally unsupported to avoid unsafe plan inference.

## 9) Regression-First Workflow
- Changes are introduced as narrow deterministic patches.
- Focused tests are added for discovered routing/alias/Arabic edge cases.
- Full test suite validation is required before declaring stability.
- Evidence replay reports are used to confirm operational behavior under real phrasing.

## 10) Scope Boundaries
- No new plans unless explicitly integrated.
- No enhanced comparison expansion unless explicitly approved.
- No architecture refactor in stabilization/presentation tracks.
- No Telegram/CRM/RAG work in deterministic core hardening sprints.
