# Pilot User Guide: Internal Controlled Rollout

## Getting Started
- Activate environment: `source .venv/Scripts/activate` (bash) or `.venv\Scripts\Activate.ps1` (PowerShell)
- Entrypoint: `.venv/Scripts/python.exe -m src.query field <plan> <field>`
- Supported plans: Remedy 02, Remedy 03, Remedy 04 (minimal fields only)
- Supported fields: plan_name, plan_code, network_name (Remedy 04: only these)

## Example Queries
- `.venv/Scripts/python.exe -m src.query field "Remedy 04" "plan_name"`
- `.venv/Scripts/python.exe -m src.query field "Remedy 04" "network_name"`

## Known Limitations
- Only deterministic fields are supported for Remedy 04
- No UI, API, or batch mode
- Do not attempt unsupported fields or plans

## Issue Reporting
- Log all issues using the template in `docs/rollout/pilot_issue_log_template.md`
- Escalate urgent issues to rollout lead: [OWNER NAME/EMAIL TO FILL]
