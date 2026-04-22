"""
Agent Adapter: Minimal deterministic integration surface for agent system.
"""
from typing import Any, Dict, Union
from src.agent_wrapper import run_agent_wrapper

# Human-readable formatting logic (aligns with entrypoint)
def _format_human_readable(result: dict) -> str:
    normalized = result.get("normalized")
    answer = None
    if normalized and isinstance(normalized, dict):
        answer = normalized.get("answer")
    intent = result.get("intent")
    plan = result.get("plan_name")
    # Language detection: Arabic if any Arabic Unicode character, else English
    user_query = result.get("user_query") or result.get("_user_query") or ""
    lang = "ar" if any("\u0600" <= c <= "\u06FF" or "\u0750" <= c <= "\u077F" or "\u08A0" <= c <= "\u08FF" or "\uFB50" <= c <= "\uFDFF" or "\uFE70" <= c <= "\uFEFF" for c in user_query) else "en"

    # English formatting (default)
    def format_english():
        def clean_plan_name(val):
            if not val:
                return val
            return str(val).replace("�", "").replace("  ", " ").strip()
        if intent == "plan_core" and isinstance(answer, dict):
            lines = []
            plan_clean = clean_plan_name(plan)
            annual_limit = answer.get("annual_limit")
            if annual_limit:
                # Remove duplicate AED if present
                val = str(annual_limit)
                val = val.replace("AED AED.", "AED.").replace("AED AED", "AED").replace("AED. AED.", "AED.")
                val = val.replace("AED. ", "").replace("AED ", "") if val.startswith("AED") and val.count("AED") > 1 else val
                lines.append(f"The annual limit for {plan_clean} is AED {val}.")
            if answer.get("area_of_coverage"):
                lines.append(f"Area of coverage: {answer['area_of_coverage']}.")
            if answer.get("direct_billing") is not None:
                lines.append(f"Direct billing: {'Yes' if answer['direct_billing'] else 'No'}.")
            if answer.get("network_name"):
                lines.append(f"Network: {answer['network_name']}.")
            if answer.get("plan_code"):
                lines.append(f"Plan code: {answer['plan_code']}.")
            if answer.get("referral_required") is not None:
                lines.append(f"Referral required: {'Yes' if answer['referral_required'] else 'No'}.")
            return "\n".join(lines) if lines else result.get("message")
        elif intent == "reimbursement_rules" and isinstance(answer, dict):
            lines = []
            if answer.get("reimbursement_allowed") is not None:
                lines.append(f"Reimbursement allowed: {'Yes' if answer['reimbursement_allowed'] else 'No'}.")
            if answer.get("reimbursement_scope"):
                lines.append(f"Scope: {answer['reimbursement_scope']}.")
            if answer.get("outside_network_reimbursement"):
                lines.append(f"Outside network reimbursement: {answer['outside_network_reimbursement']}.")
            if answer.get("outside_uae_reimbursement"):
                lines.append(f"Outside UAE reimbursement: {answer['outside_uae_reimbursement']}.")
            if answer.get("reimbursement_basis"):
                lines.append(f"Basis: {answer['reimbursement_basis']}")
            if answer.get("reimbursement_conditions"):
                lines.append(f"Conditions: {answer['reimbursement_conditions']}")
            if answer.get("reimbursement_documents_required"):
                lines.append(f"Documents required: {answer['reimbursement_documents_required']}.")
            return "\n".join(lines) if lines else result.get("message")
        elif intent == "plan_summary" and isinstance(answer, dict):
            def clean(val):
                if not val:
                    return val
                return str(val).replace("�", "").replace("  ", " ").strip()
            lines = []
            # Always show plan name and code if present
            if answer.get("plan_name"):
                lines.append(f"Plan: {clean(answer['plan_name'])}")
            if answer.get("plan_code"):
                lines.append(f"Code: {clean(answer['plan_code'])}")
            # Show all real data fields
            if answer.get("network_name"):
                lines.append(f"Network: {clean(answer['network_name'])}")
            if answer.get("annual_limit"):
                val = str(answer['annual_limit'])
                val = val.replace("AED AED.", "AED.").replace("AED AED", "AED").replace("AED. AED.", "AED.")
                val = val.replace("AED. ", "").replace("AED ", "") if val.startswith("AED") and val.count("AED") > 1 else val
                lines.append(f"Annual limit: {val}")
            if answer.get("area_of_coverage"):
                lines.append(f"Area: {clean(answer['area_of_coverage'])}")
            if answer.get("direct_billing") is not None:
                lines.append(f"Direct billing: {'Yes' if answer['direct_billing'] else 'No'}")
            if answer.get("referral_required") is not None:
                lines.append(f"Referral required: {'Yes' if answer['referral_required'] else 'No'}")
            if answer.get("maternity_cover"):
                lines.append(f"Maternity cover: {clean(answer['maternity_cover'])}")
            if answer.get("pharmacy_cover"):
                lines.append(f"Pharmacy cover: {clean(answer['pharmacy_cover'])}")
            if answer.get("key_exclusions"):
                lines.append(f"Key exclusions: {answer['key_exclusions']}")
            # Add summary_text highlights if present and not already included
            summary = answer.get("summary_text", "")
            import re
            field_patterns = [
                ("Network", r"Network: (.+)"),
                ("Annual limit", r"Annual Limit: ([^\n]+)"),
                ("Area", r"Area of Coverage: ([^\n]+)"),
                ("Direct billing", r"Direct Billing: (Yes|No|Not available)"),
                ("Referral required", r"Referral Required: (Yes|No|Not available)"),
                ("Maternity cover", r"Maternity Cover: ([^\n]+)"),
                ("Pharmacy cover", r"Pharmacy Cover: ([^\n]+)"),
                ("Key exclusions", r"Key Exclusions: (\d+ listed|\d+)")
            ]
            for label, pat in field_patterns:
                m = re.search(pat, summary)
                if m:
                    val = m.group(1)
                    # Only add if not already present
                    line = f"{label}: {val}"
                    if not any(line.startswith(label) for line in lines):
                        lines.append(line)
            return "\n".join(lines) if lines else result.get("message")
        elif intent == "plan_comparison" and result.get("message"):
            # For English, just clean plan names and fix AED AED
            msg = result["message"]
            def clean(val):
                if not val:
                    return val
                return str(val).replace("�", "").replace("  ", " ").strip()
            lines = msg.splitlines()
            out = []
            import re
            header_pat = re.compile(r"Comparison between (.+) and (.+):")
            for i, line in enumerate(lines):
                if i == 0:
                    m = header_pat.match(line)
                    if m:
                        p1, p2 = clean(m.group(1)), clean(m.group(2))
                        out.append(f"Comparison between {p1} and {p2}:")
                    else:
                        out.append(clean(line))
                elif ":" in line and "|" in line:
                    label, rest = line.split(":", 1)
                    label = label.strip()
                    vals = rest.split("|")
                    if len(vals) == 2:
                        v1 = vals[0].split(":", 1)[-1].strip()
                        v2 = vals[1].split(":", 1)[-1].strip()
                        # Remove duplicate AED
                        v1 = v1.replace("AED AED.", "AED.").replace("AED AED", "AED").replace("AED. AED.", "AED.")
                        v2 = v2.replace("AED AED.", "AED.").replace("AED AED", "AED").replace("AED. AED.", "AED.")
                        out.append(f"{label}: {v1} | {v2}")
                    else:
                        out.append(clean(line))
                else:
                    out.append(clean(line))
            return "\n".join(out)
        return result.get("message")

    # Arabic formatting
    def format_arabic():
        # Arabic label/value maps
        ar_labels = {
            "plan_name": "اسم الخطة",
            "plan_code": "رمز الخطة",
            "network_name": "الشبكة",
            "annual_limit": "الحد السنوي",
            "area_of_coverage": "نطاق التغطية",
            "direct_billing": "الدفع المباشر",
            "referral_required": "الإحالة مطلوبة",
            "maternity_cover": "تغطية الأمومة",
            "pharmacy_cover": "تغطية الصيدلية",
            "key_exclusions": "الاستثناءات الأساسية",
            "reimbursement_allowed": "التعويض متاح",
            "reimbursement_scope": "نطاق التعويض",
            "outside_network_reimbursement": "تعويض خارج الشبكة",
            "outside_uae_reimbursement": "تعويض خارج الإمارات",
            "reimbursement_basis": "أساس التعويض",
            "reimbursement_conditions": "شروط التعويض",
            "reimbursement_documents_required": "المستندات المطلوبة",
        }
        ar_yesno = {True: "نعم", False: "لا", None: "غير متوفر"}
        if intent == "plan_core" and isinstance(answer, dict):
            def clean(val):
                if not val:
                    return val
                return str(val).replace("�", "").replace("  ", " ").strip()
            lines = []
            for k in ["plan_name", "plan_code", "network_name", "annual_limit", "area_of_coverage", "direct_billing", "referral_required"]:
                v = answer.get(k)
                if v is not None:
                    if k in ["direct_billing", "referral_required"]:
                        lines.append(f"{ar_labels[k]}: {ar_yesno.get(bool(v), 'غير متوفر')}")
                    else:
                        lines.append(f"{ar_labels[k]}: {clean(v)}")
            return "\n".join(lines) if lines else result.get("message")
        elif intent == "reimbursement_rules" and isinstance(answer, dict):
            lines = []
            for k in ["reimbursement_allowed", "reimbursement_scope", "outside_network_reimbursement", "outside_uae_reimbursement", "reimbursement_basis", "reimbursement_conditions", "reimbursement_documents_required"]:
                v = answer.get(k)
                if v is not None:
                    if k == "reimbursement_allowed":
                        lines.append(f"{ar_labels[k]}: {ar_yesno.get(bool(v), 'غير متوفر')}")
                    else:
                        lines.append(f"{ar_labels[k]}: {v}")
            return "\n".join(lines) if lines else result.get("message")
        elif intent == "plan_summary" and isinstance(answer, dict):
            # Always show all key fields, not just summary_text
            def clean(val):
                if not val:
                    return val
                return str(val).replace("�", "").replace("  ", " ").strip()
            lines = []
            for k in ["plan_name", "plan_code", "network_name", "annual_limit", "area_of_coverage", "direct_billing", "referral_required", "maternity_cover", "pharmacy_cover", "key_exclusions"]:
                v = answer.get(k)
                if v is not None:
                    if k in ["direct_billing", "referral_required"]:
                        lines.append(f"{ar_labels[k]}: {ar_yesno.get(bool(v), 'غير متوفر')}")
                    else:
                        lines.append(f"{ar_labels[k]}: {clean(v)}")
            return "\n".join(lines) if lines else result.get("message")
        elif intent == "plan_comparison" and result.get("message"):
            # Parse English comparison and render clean Arabic
            msg = result["message"]
            lines = msg.splitlines()
            if not lines:
                return msg
            import re
            header = lines[0]
            m = re.match(r"Comparison between (.+) and (.+):", header)
            if not m:
                return msg  # fallback
            plan1, plan2 = m.group(1).strip().replace("�", ""), m.group(2).strip().replace("�", "")
            ar_field_map = {
                "Annual Limit": "الحد السنوي",
                "Network": "الشبكة",
                "Area of Coverage": "نطاق التغطية",
                "Direct Billing": "الدفع المباشر",
                "Reimbursement Allowed": "التعويض"
            }
            ar_yesno = {"Yes": "نعم", "No": "لا"}
            out = [f"مقارنة بين {plan1} و {plan2}:"]
            for line in lines[1:]:
                if ":" in line and "|" in line:
                    label, rest = line.split(":", 1)
                    label = label.strip()
                    ar_label = ar_field_map.get(label, label)
                    vals = rest.split("|")
                    if len(vals) == 2:
                        v1 = vals[0].split(":", 1)[-1].strip().replace("�", "")
                        v2 = vals[1].split(":", 1)[-1].strip().replace("�", "")
                        if label in ["Direct Billing", "Reimbursement Allowed"]:
                            v1 = ar_yesno.get(v1, v1)
                            v2 = ar_yesno.get(v2, v2)
                        out.append(f"{ar_label}: {plan1}: {v1} | {plan2}: {v2}")
            return "\n".join(out) if len(out) > 1 else msg
        return result.get("message")

    # Route by language
    if lang == "ar":
        return format_arabic()
    else:
        return format_english()

def handle_user_query(user_query: str, output_mode: str = "dict") -> Union[Dict[str, Any], str]:
    result = run_agent_wrapper(user_query)
    if output_mode == "dict":
        return result
    elif output_mode == "text":
        return _format_human_readable(result)
    else:
        return {
            "ok": False,
            "intent": "unsupported",
            "plan_name": None,
            "tool_name": None,
            "data": None,
            "message": f"Invalid output_mode: {output_mode}. Supported: 'dict', 'text'."
        }
