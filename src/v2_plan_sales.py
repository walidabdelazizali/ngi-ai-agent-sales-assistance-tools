from src.v2_plan_compare import compare_two_plans

def build_plan_sales_summary(plan: dict) -> dict:
    name = plan.get("plan_name", "Plan")
    lines = []
    # Annual limit
    if plan.get("annual_limit"):
        amt = str(plan['annual_limit']).replace("AED", "").replace(".", "").strip()
        lines.append(f"Annual limit: AED {amt}")
    # Network
    if plan.get("network_name"):
        net = plan["network_name"].split("(")[0].strip()
        lines.append(f"{net} network")
    # Specialist access
    if plan.get("specialist_access_model") == "direct":
        lines.append("Direct specialist access")
    elif plan.get("specialist_access_model") == "referral":
        lines.append("Referral-based specialist access")
    # Lab/radiology
    lab = plan.get("laboratory_cost_share")
    rad = plan.get("radiology_cost_share")
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
    lab_clean = clean_lab_rad(lab)
    rad_clean = clean_lab_rad(rad)
    if lab_clean == "Nil" and rad_clean == "Nil":
        lines.append("No lab or radiology co-pay")
    elif lab_clean or rad_clean:
        if lab_clean and lab_clean != "Nil":
            lines.append(f"Lab co-pay: {lab_clean}")
        if rad_clean and rad_clean != "Nil":
            lines.append(f"Radiology co-pay: {rad_clean}")
    # Physiotherapy
    physio = plan.get("physiotherapy_limit_and_cost_share")
    def clean_physio(val):
        if not val:
            return None
        import re
        m = re.match(r".*?(\d{1,3}) sessions.*?(\d{1,2})%", val)
        if m:
            return f"{m.group(1)} sessions/year; {m.group(2)}% co-pay"
        m = re.match(r".*?(\d{1,3}) sessions.*?NIL", val, re.I)
        if m:
            return f"{m.group(1)} sessions/year; Nil co-pay"
        return val
    physio_clean = clean_physio(physio)
    if physio_clean:
        lines.append(f"Physiotherapy: {physio_clean}")
    # Pharmacy
    pharm = plan.get("pharmacy_limit_and_cost_share")
    if pharm:
        import re
        m = re.match(r"AED ?([\d,]+)[^\d]*(\d{1,2})%", pharm.replace(",", ""))
        if m:
            lines.append(f"Pharmacy cover up to AED {int(m.group(1)):,}/year with {m.group(2)}% payable")
        elif "Nil" in pharm or "nil" in pharm:
            lines.append("Pharmacy with Nil co-pay")
        else:
            lines.append(f"Pharmacy: {pharm}")
    # Reimbursement
    if plan.get("reimbursement_outside_network") or plan.get("reimbursement_outside_uae"):
        if plan.get("reimbursement_outside_network"):
            lines.append("Reimbursement available within UAE")
        if plan.get("reimbursement_outside_uae"):
            lines.append("Reimbursement available outside UAE")
    # Headline
    if plan.get("specialist_access_model") == "direct":
        headline = "Stronger outpatient value with direct specialist access"
    elif plan.get("specialist_access_model") == "referral":
        headline = "Balanced essential cover with referral-based access"
    else:
        headline = "Balanced essential cover"
    return {
        "plan_name": name,
        "headline": headline,
        "sales_lines": lines
    }

def build_plan_upgrade_pitch(plan_a: dict, plan_b: dict) -> dict:
    from_plan = plan_a.get("plan_name", "Plan A")
    to_plan = plan_b.get("plan_name", "Plan B")
    comparison = compare_two_plans(plan_a, plan_b)
    lines = []
    # Specialist access
    if plan_a.get("specialist_access_model") == "referral" and plan_b.get("specialist_access_model") == "direct":
        lines.append("Direct specialist access instead of referral-based access")
    # Pharmacy
    pa = plan_a.get("pharmacy_limit_and_cost_share")
    pb = plan_b.get("pharmacy_limit_and_cost_share")
    import re
    def extract_pharm(val):
        if not val:
            return (None, None)
        m = re.match(r"AED ?([\d,]+)[^\d]*(\d{1,2})%", val.replace(",", ""))
        if m:
            return (int(m.group(1)), int(m.group(2)))
        return (None, None)
    lim_a, pct_a = extract_pharm(pa)
    lim_b, pct_b = extract_pharm(pb)
    if lim_a and lim_b and (lim_b > lim_a or (pct_a and pct_b and pct_b < pct_a)):
        if lim_b > lim_a and pct_b < pct_a:
            lines.append(f"Improved pharmacy cover from AED {lim_a:,}/year at {pct_a}% payable to AED {lim_b:,}/year at {pct_b}% payable")
        elif lim_b > lim_a:
            lines.append(f"Pharmacy cover increased from AED {lim_a:,}/year to AED {lim_b:,}/year")
        elif pct_b < pct_a:
            lines.append(f"Pharmacy payable reduced from {pct_a}% to {pct_b}%")
    # Lab/radiology
    la = plan_a.get("laboratory_cost_share")
    lb = plan_b.get("laboratory_cost_share")
    ra = plan_a.get("radiology_cost_share")
    rb = plan_b.get("radiology_cost_share")
    if la != lb and lb == "Nil":
        lines.append("Nil lab co-pay instead of percentage co-pay")
    if ra != rb and rb == "Nil":
        lines.append("Nil radiology co-pay instead of percentage co-pay")
    # Physio
    phya = plan_a.get("physiotherapy_limit_and_cost_share")
    phyb = plan_b.get("physiotherapy_limit_and_cost_share")
    if phya and phyb and "Nil" in phyb and "Nil" not in phya:
        lines.append("Physiotherapy now with Nil co-pay")
    # Reimbursement
    if plan_a.get("reimbursement_outside_uae") != plan_b.get("reimbursement_outside_uae") and plan_b.get("reimbursement_outside_uae"):
        lines.append("International reimbursement now available")
    # Headline
    if lines:
        headline = f"Clear outpatient upgrade from {from_plan} to {to_plan}"
    else:
        headline = f"No significant upgrade from {from_plan} to {to_plan}"
        lines = ["No major improvements detected."]
    return {
        "from_plan": from_plan,
        "to_plan": to_plan,
        "headline": headline,
        "upgrade_lines": lines
    }

def build_plan_difference_pitch(comparison: dict) -> dict:
    lines = []
    for s in comparison.get("summary_lines", []):
        # Transform summary lines to business-friendly pitch
        if "direct specialist access" in s and "requires referral" in s:
            lines.append("Direct specialist access vs referral-based access")
        elif "Lab:" in s or "lab" in s:
            lines.append("Lower day-to-day lab cost share")
        elif "Radiology:" in s or "radiology" in s:
            lines.append("Lower day-to-day radiology cost share")
        elif "Physio:" in s or "physio" in s:
            lines.append("Improved physiotherapy benefit")
        elif "Pharmacy:" in s or "pharmacy" in s:
            lines.append("Stronger pharmacy benefit with higher annual limit and lower payable share")
        elif "reimbursement" in s.lower():
            lines.append("Reimbursement benefit difference")
        elif "outpatient consult" in s.lower():
            lines.append("Outpatient consultation cost share difference")
        elif "annual limit" in s.lower():
            lines.append("Annual limit difference")
        elif "no major improvements" in s.lower():
            lines.append("No significant differences detected")
        elif "specialist access differs" in s.lower():
            lines.append("Specialist access model difference")
    if not lines:
        lines = ["No significant differences detected"]
    headline = "Key differences between the two plans"
    return {
        "headline": headline,
        "pitch_lines": lines
    }
