def compare_two_plans(plan_a: dict, plan_b: dict) -> dict:
    fields = [
        "annual_limit",
        "network_name",
        "specialist_access_model",
        "outpatient_consultation_cost_share",
        "laboratory_cost_share",
        "radiology_cost_share",
        "physiotherapy_limit_and_cost_share",
        "pharmacy_limit_and_cost_share",
        "reimbursement_outside_network",
        "reimbursement_outside_uae",
    ]
    plan_a_name = plan_a.get("plan_name", "Plan A")
    plan_b_name = plan_b.get("plan_name", "Plan B")
    field_differences = []
    summary_lines = []

    def clean_network_name(val):
        if not val:
            return None
        # Extract base name (e.g., "HN Basic Plus")
        import re
        match = re.search(r"HN [A-Za-z ]+", val)
        if match:
            return match.group(0).strip()
        # fallback: first 24 chars or up to first paren
        if '(' in val:
            return val.split('(')[0].strip()
        return val[:24].strip()

    def clean_pharmacy(val):
        if not val:
            return None
        import re
        # AED 3,000 30% -> AED 3,000/year; 30% payable
        m = re.match(r"AED\s*([\d,]+)\s*(\d{1,2})%", val.replace(",", ""))
        if m:
            return f"AED {int(m.group(1)):,}/year; {m.group(2)}% payable"
        # AED3,000 30%
        m = re.match(r"AED([\d,]+)\s*(\d{1,2})%", val.replace(",", ""))
        if m:
            return f"AED {int(m.group(1)):,}/year; {m.group(2)}% payable"
        # AED 3,000 only
        m = re.match(r"AED\s*([\d,]+)", val.replace(",", ""))
        if m:
            return f"AED {int(m.group(1)):,}/year"
        return val

    def clean_physiotherapy(val):
        if not val:
            return None
        import re
        # 12 sessions/year; 15% co-pay
        m = re.match(r".*?(\d{1,3}) sessions.*?(\d{1,2})%", val)
        if m:
            return f"{m.group(1)} sessions/year; {m.group(2)}% co-pay"
        # 12 sessions/year; NIL co-pay
        m = re.match(r".*?(\d{1,3}) sessions.*?NIL", val, re.I)
        if m:
            return f"{m.group(1)} sessions/year; Nil co-pay"
        return val

    def clean_lab_rad(val):
        if not val:
            return None
        if val.strip().lower() == "nil":
            return "Nil"
        import re
        m = re.search(r"(\d{1,2})%", val)
        if m:
            return f"{m.group(1)}% co-pay"
        return val

    for field in fields:
        a_val = plan_a.get(field)
        b_val = plan_b.get(field)
        # Clean values for summary output only
        a_val_clean = a_val
        b_val_clean = b_val
        if field == "network_name":
            a_val_clean = clean_network_name(a_val)
            b_val_clean = clean_network_name(b_val)
            # If cleaned network names are equal, skip this field entirely
            if a_val_clean == b_val_clean:
                continue
        elif field == "pharmacy_limit_and_cost_share":
            a_val_clean = clean_pharmacy(a_val)
            b_val_clean = clean_pharmacy(b_val)
        elif field == "physiotherapy_limit_and_cost_share":
            a_val_clean = clean_physiotherapy(a_val)
            b_val_clean = clean_physiotherapy(b_val)
        elif field in ("laboratory_cost_share", "radiology_cost_share"):
            a_val_clean = clean_lab_rad(a_val)
            b_val_clean = clean_lab_rad(b_val)
        if a_val != b_val:
            field_differences.append({
                "field": field,
                "plan_a": a_val,
                "plan_b": b_val
            })
            # Deterministic summary patterns
            if field == "specialist_access_model":
                if a_val == "referral" and b_val == "direct":
                    summary_lines.append(f"{plan_b_name} offers direct specialist access, {plan_a_name} requires referral.")
                elif a_val == "direct" and b_val == "referral":
                    summary_lines.append(f"{plan_b_name} requires referral for specialist access, {plan_a_name} offers direct access.")
                else:
                    summary_lines.append(f"Specialist access differs.")
            elif field == "pharmacy_limit_and_cost_share":
                summary_lines.append(f"Pharmacy: {a_val_clean} vs {b_val_clean}")
            elif field == "laboratory_cost_share":
                summary_lines.append(f"Lab: {a_val_clean} vs {b_val_clean}")
            elif field == "radiology_cost_share":
                summary_lines.append(f"Radiology: {a_val_clean} vs {b_val_clean}")
            elif field == "outpatient_consultation_cost_share":
                summary_lines.append(f"Outpatient consult cost share differs.")
            elif field == "network_name":
                summary_lines.append(f"Network: {a_val_clean} vs {b_val_clean}")
            elif field == "annual_limit":
                summary_lines.append(f"Annual limit differs.")
            elif field == "physiotherapy_limit_and_cost_share":
                summary_lines.append(f"Physio: {a_val_clean} vs {b_val_clean}")
            elif field == "reimbursement_outside_network":
                summary_lines.append(f"Reimbursement (UAE) differs.")
            elif field == "reimbursement_outside_uae":
                summary_lines.append(f"Reimbursement (Outside UAE) differs.")
    if not field_differences:
        summary_lines = ["Compared fields are the same."]
    return {
        "plan_a_name": plan_a_name,
        "plan_b_name": plan_b_name,
        "field_differences": field_differences,
        "summary_lines": summary_lines
    }
