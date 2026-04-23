def answer_plan_core(plan: dict) -> dict:
    def clean_annual_limit(val):
        if not val:
            return val
        v = str(val)
        v = v.replace("AED.", "").replace("AED", "").replace(".", "").strip()
        v = v.replace(",", "")
        v = v.replace("  ", " ")
        # Only keep digits and comma
        v = v.replace(" ", "")
        return f"AED {int(v):,}"

    def clean_network_name(val):
        if not val:
            return val
        # Extract base network name (first phrase, up to first paren or dash or 'with')
        import re
        m = re.match(r"([A-Za-z0-9\- ]+)", val)
        if m:
            base = m.group(1).strip()
            # Remove trailing 'with' or similar
            base = base.split("with")[0].strip()
            return base
        return val.split("with")[0].split("(")[0].strip()

    def clean_pharmacy(val):
        if not val:
            return val
        import re
        m = re.match(r"AED[ .]?([\d,]+)[^\d]*(\d{1,2})%", val)
        if m:
            amt = m.group(1).replace(",", "")
            pct = m.group(2)
            return f"AED {int(amt):,}/year; {pct}% payable"
        # fallback: just AED
        m2 = re.match(r"AED[ .]?([\d,]+)", val)
        if m2:
            amt = m2.group(1).replace(",", "")
            return f"AED {int(amt):,}/year"
        return val

    def clean_lab_rad(val):
        if not val:
            return val
        if "nil" in val.lower():
            return "Nil"
        import re
        m = re.search(r"(\d{1,2})%", val)
        if m:
            return f"{m.group(1)}% co-pay"
        return val.split()[0] if "%" in val else val

    def clean_physio(val):
        if not val:
            return val
        import re
        # Look for session count and co-pay
        session = re.search(r"(\d{1,2}) sessions", val)
        copay = re.search(r"(\d{1,2})%", val)
        if session and copay:
            return f"{session.group(1)} sessions/year; {copay.group(1)}% co-pay"
        elif session and "nil" in val.lower():
            return f"{session.group(1)} sessions/year; Nil co-pay"
        elif session:
            return f"{session.group(1)} sessions/year"
        return val

    result = {}
    for field in [
        "plan_name",
        "annual_limit",
        "network_name",
        "area_of_coverage",
        "specialist_access_model",
        "outpatient_consultation_cost_share",
        "laboratory_cost_share",
        "radiology_cost_share",
        "physiotherapy_limit_and_cost_share",
        "pharmacy_limit_and_cost_share",
    ]:
        value = plan.get(field)
        if value is not None:
            if field == "annual_limit":
                value = clean_annual_limit(value)
            elif field == "network_name":
                value = clean_network_name(value)
            elif field == "pharmacy_limit_and_cost_share":
                value = clean_pharmacy(value)
            elif field in ("laboratory_cost_share", "radiology_cost_share"):
                value = clean_lab_rad(value)
            elif field == "physiotherapy_limit_and_cost_share":
                value = clean_physio(value)
            else:
                value = value.strip() if isinstance(value, str) else value
            result[field] = value
    return result

def answer_reimbursement(plan: dict) -> dict:
    fields = [
        "plan_name",
        "reimbursement_outside_network",
        "reimbursement_outside_uae",
    ]
    result = {}
    for field in fields:
        value = plan.get(field)
        if value is not None:
            if isinstance(value, str):
                value = value.strip()
            result[field] = value
    return result

def answer_plan_summary(plan: dict) -> dict:
    lines = []
    def add_line(label, value):
        if value is not None:
            v = value.strip() if isinstance(value, str) else value
            lines.append(f"{label}: {v}")

    # Use the same cleaning as in core
    from src.v2_plan_answers import answer_plan_core
    core = answer_plan_core(plan)
    plan_name = core.get("plan_name")
    annual_limit = core.get("annual_limit")
    network_name = core.get("network_name")
    specialist_access_model = core.get("specialist_access_model")
    outpatient = core.get("outpatient_consultation_cost_share")
    lab = core.get("laboratory_cost_share")
    radiology = core.get("radiology_cost_share")
    physio = core.get("physiotherapy_limit_and_cost_share")
    pharmacy = core.get("pharmacy_limit_and_cost_share")
    reimb_uae = plan.get("reimbursement_outside_network")
    reimb_outside = plan.get("reimbursement_outside_uae")

    add_line("Annual limit", annual_limit)
    add_line("Network", network_name)
    if specialist_access_model:
        if specialist_access_model.lower() == "direct":
            lines.append("Specialist access: Direct")
        elif specialist_access_model.lower() == "referral":
            lines.append("Specialist access: Referral required")
        else:
            lines.append(f"Specialist access: {specialist_access_model}")
    add_line("Outpatient", outpatient)
    add_line("Lab", lab)
    add_line("Radiology", radiology)
    add_line("Physiotherapy", physio)
    add_line("Pharmacy", pharmacy)
    if reimb_uae is not None:
        add_line("Reimbursement (UAE)", reimb_uae)
    if reimb_outside is not None:
        add_line("Reimbursement (Outside UAE)", reimb_outside)

    return {
        "plan_name": plan_name.strip() if isinstance(plan_name, str) else plan_name,
        "summary_lines": lines
    }
