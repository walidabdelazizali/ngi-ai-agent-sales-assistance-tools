from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "docs" / "operational_usage"
PACK_PATH = OUTPUT_DIR / "operational_pressure_200_pack.md"
RESULTS_PATH = OUTPUT_DIR / "operational_pressure_200_results.md"
DELTA_PATH = OUTPUT_DIR / "operational_pressure_200_delta.md"
PREVIOUS_RESULTS_PATH = OUTPUT_DIR / "real_usage_evidence_pack_100_results.md"

SECTION_TITLES = {
    "remedy_core_pressure": "Remedy/Core Plan Questions",
    "provider_network_pressure": "Provider/Network Lookup",
    "enhanced_baseline_classic2r": "Enhanced Baseline (Classic 2R)",
    "comparison_pressure": "Comparison Pressure",
    "recommendation_oos_pressure": "Recommendation / Out-of-Scope Pressure",
    "broker_style_arabic_pressure": "Real Broker-Style Arabic Phrasing",
}

EXPECTED_SECTION_COUNTS = {
    "remedy_core_pressure": 40,
    "provider_network_pressure": 50,
    "enhanced_baseline_classic2r": 40,
    "comparison_pressure": 30,
    "recommendation_oos_pressure": 20,
    "broker_style_arabic_pressure": 20,
}

SUPPORTED_OK_INTENTS = {
    "plan_core",
    "plan_summary",
    "reimbursement_rules",
    "network_lookup",
    "plan_comparison",
    "plan_network_city_type",
}

SAFE_BLOCK_TERMS = (
    "not supported",
    "not available",
    "provider not found",
    "ambiguous provider",
    "supported plan",
    "supported question",
    "غير مدعوم",
    "غير متاح",
    "المزود غير موجود",
    "مزود غير محدد",
    "يرجى تحديد",
)


@dataclass(frozen=True)
class PressureCase:
    section: str
    query: str
    expected: str
    theme: str
    tags: tuple[str, ...]


def supported(query: str, theme: str, *tags: str) -> dict:
    return {"query": query, "expected": "supported", "theme": theme, "tags": tags}


def blocked(query: str, theme: str, *tags: str) -> dict:
    return {"query": query, "expected": "blocked", "theme": theme, "tags": tags}


def ambiguity_safe(query: str, theme: str, *tags: str) -> dict:
    return {"query": query, "expected": "ambiguity_safe", "theme": theme, "tags": tags}


def not_found_safe(query: str, theme: str, *tags: str) -> dict:
    return {"query": query, "expected": "not_found_safe", "theme": theme, "tags": tags}


def build_cases(section: str, entries: list[dict]) -> list[PressureCase]:
    return [
        PressureCase(
            section=section,
            query=entry["query"],
            expected=entry["expected"],
            theme=entry["theme"],
            tags=tuple(entry.get("tags", ())),
        )
        for entry in entries
    ]


REMEDY_CORE_CASES = build_cases(
    "remedy_core_pressure",
    [
        supported("Summarize Remedy 02", "summary"),
        supported("Give me a summary of Remedy 03", "summary"),
        supported("Summary Remedy 05", "summary"),
        supported("Summarize Remedy 6", "summary"),
        supported("What is the annual limit for Remedy 02?", "annual_limit"),
        supported("annual limit Remedy 03", "annual_limit"),
        supported("Remedy 05 limit", "annual_limit"),
        supported("limit for Remedy 6", "annual_limit"),
        supported("What is the network for Remedy 02?", "network"),
        supported("Remedy 03 network", "network"),
        supported("network Remedy 05", "network"),
        supported("which network for Remedy 6", "network"),
        supported("Does Remedy 02 need referral?", "referral"),
        supported("referral Remedy 03", "referral"),
        supported("is referral required for Remedy 05?", "referral"),
        supported("Remedy 6 referral?", "referral"),
        supported("Is there direct billing for Remedy 02?", "direct_billing"),
        supported("direct billing Remedy 03", "direct_billing"),
        supported("Remedy 05 cashless?", "direct_billing"),
        supported("cashless Remedy 6", "direct_billing"),
        supported("What is the area of coverage for Remedy 02?", "area_of_coverage"),
        supported("area of coverage Remedy 03", "area_of_coverage"),
        supported("coverage area Remedy 05", "area_of_coverage"),
        supported("Remedy 6 coverage area", "area_of_coverage"),
        supported("What are the reimbursement rules for Remedy 02?", "reimbursement"),
        supported("reimbursement Remedy 03", "reimbursement"),
        supported("reimbursement rules Remedy 05", "reimbursement"),
        supported("Remedy 6 reimbursement", "reimbursement"),
        supported("هل ريميدي 02 فيه كاشلس؟", "direct_billing", "arabic"),
        supported("شبكة ريميدي 03", "network", "arabic"),
        supported("ليمت ريميدي 05", "annual_limit", "arabic"),
        supported("ملخص ريميدي 06", "summary", "arabic"),
        supported("هل ريميدي 02 يحتاج referral؟", "referral", "arabic", "mixed"),
        supported("direct billing في Remedy 03؟", "direct_billing", "arabic", "mixed"),
        supported("ما هي منطقة التغطية لخطة Remedy 05؟", "area_of_coverage", "arabic", "mixed"),
        supported("ما هي شروط التعويض لخطة Remedy 06؟", "reimbursement", "arabic", "mixed"),
        supported("Remedy 02 summary", "summary"),
        supported("هل خطة Remedy 03 فيها direct billing؟", "direct_billing", "arabic", "mixed"),
        supported("annual limit for Remedy 05 please", "annual_limit"),
        supported("Does Remedy 06 cover reimbursement outside network?", "reimbursement"),
    ],
)

PROVIDER_NETWORK_CASES = build_cases(
    "provider_network_pressure",
    [
        supported("Burjeel Abu Dhabi in which network?", "provider_alias", "provider"),
        supported("Burjeel AUH in which network?", "provider_alias", "provider"),
        supported("في أي شبكة Burjeel Abu Dhabi", "provider_alias", "provider", "arabic", "mixed"),
        supported("في أي شبكة Burjeel AUH", "provider_alias", "provider", "arabic", "mixed"),
        supported("Aster Qusais in which network?", "provider_alias", "provider"),
        supported("Aster Al Qusais in which network?", "provider_alias", "provider"),
        supported("في أي شبكة Aster Qusais", "provider_alias", "provider", "arabic", "mixed"),
        supported("Mediclinic Qusais in which network?", "provider_alias", "provider"),
        supported("في أي شبكة Mediclinic Qusais", "provider_alias", "provider", "arabic", "mixed"),
        supported("Burjeel Hospital network tiers?", "network_tier", "provider"),
        supported("Which network tiers is Burjeel Hospital available in?", "network_tier", "provider"),
        supported("NMC Royal in which network?", "provider_alias", "provider"),
        supported("Providers in Dubai Remedy 6", "city_query", "provider", "city"),
        supported("Dubai providers Remedy 6", "city_query", "provider", "city"),
        supported("Remedy 6 Dubai providers", "city_query", "provider", "city"),
        supported("Sharjah hospitals Remedy 6", "city_type_query", "provider", "city", "type"),
        supported("Abu Dhabi labs Remedy 6", "city_type_query", "provider", "city", "type"),
        supported("diagnostic centers in Dubai Remedy 6", "city_type_query", "provider", "city", "type"),
        supported("labs in Abu Dhabi Remedy 6", "city_type_query", "provider", "city", "type"),
        supported("What type of provider is Burjeel Abu Dhabi?", "provider_type", "provider", "type"),
        supported("What type of provider is Aster Qusais?", "provider_type", "provider", "type"),
        supported("What type of provider is Mediclinic Qusais?", "provider_type", "provider", "type"),
        supported("هل Aster Qusais داخل الشبكة؟", "provider_lookup", "provider", "arabic", "mixed"),
        supported("هل Mediclinic Qusais داخل الشبكة؟", "provider_lookup", "provider", "arabic", "mixed"),
        supported("هل Burjeel Abu Dhabi داخل الشبكة؟", "provider_lookup", "provider", "arabic", "mixed"),
        supported("providers in Dubai for Remedy 06", "city_query", "provider", "city"),
        supported("Remedy 06 Abu Dhabi labs", "city_type_query", "provider", "city", "type"),
        supported("Dubai diagnostic providers Remedy 6", "city_type_query", "provider", "city", "type"),
        supported("Which network is Aster Al Qusais in?", "provider_alias", "provider"),
        supported("Which network is Burjeel Specialty Hospital Sharjah in?", "provider_alias", "provider"),
        supported("في أي شبكة Burjeel Specialty Hospital Sharjah", "provider_alias", "provider", "arabic", "mixed"),
        supported("Burjeel AUH في أي شبكة؟", "provider_alias", "provider", "arabic", "mixed"),
        supported("Aster Qusais network ايه؟", "provider_alias", "provider", "arabic", "mixed"),
        supported("Remedy 6 Dubai labs", "city_type_query", "provider", "city", "type"),
        supported("Remedy 6 Sharjah hospitals", "city_type_query", "provider", "city", "type"),
        supported("Which network tiers for Burjeel Abu Dhabi?", "network_tier", "provider"),
        ambiguity_safe("Is Burjeel Hospital in the network?", "provider_ambiguity", "provider", "ambiguous"),
        ambiguity_safe("هل Burjeel Hospital داخل الشبكة؟", "provider_ambiguity", "provider", "ambiguous", "arabic", "mixed"),
        ambiguity_safe("Which network tiers for NMC Royal?", "provider_ambiguity", "provider", "ambiguous"),
        ambiguity_safe("في أي شبكة NMC Royal", "provider_ambiguity", "provider", "ambiguous", "arabic", "mixed"),
        ambiguity_safe("Is Royal Hospital in the network?", "provider_ambiguity", "provider", "ambiguous"),
        ambiguity_safe("هل Royal Hospital داخل الشبكة؟", "provider_ambiguity", "provider", "ambiguous", "arabic", "mixed"),
        ambiguity_safe("Which network is Aster Hospital in?", "provider_ambiguity", "provider", "ambiguous"),
        ambiguity_safe("في أي شبكة Aster Hospital", "provider_ambiguity", "provider", "ambiguous", "arabic", "mixed"),
        not_found_safe("Is Unknown Future Hospital in the network?", "provider_not_found", "provider"),
        not_found_safe("هل Unknown Future Hospital داخل الشبكة؟", "provider_not_found", "provider", "arabic", "mixed"),
        not_found_safe("Which network is Imaginary Clinic in?", "provider_not_found", "provider"),
        not_found_safe("في أي شبكة Imaginary Clinic", "provider_not_found", "provider", "arabic", "mixed"),
        not_found_safe("Does Nonexistent Lab belong to the network?", "provider_not_found", "provider"),
        not_found_safe("هل هذه المستشفى ضمن الشبكة؟", "provider_not_found", "provider", "arabic"),
    ],
)

ENHANCED_BASELINE_CASES = build_cases(
    "enhanced_baseline_classic2r",
    [
        supported("Summarize Classic 2R", "summary", "enhanced"),
        supported("classic2r limit", "annual_limit", "enhanced"),
        supported("What is the annual limit for Classic 2R?", "annual_limit", "enhanced"),
        supported("What is the network name for Classic 2R?", "network", "enhanced"),
        supported("Does Classic 2R support direct billing?", "direct_billing", "enhanced"),
        supported("Is referral required for Classic 2R?", "referral", "enhanced"),
        supported("Classic 2R cashless?", "direct_billing", "enhanced"),
        supported("area of coverage Classic 2R", "area_of_coverage", "enhanced"),
        supported("coverage Classic 2R", "area_of_coverage", "enhanced"),
        supported("HN Classic 2R limit", "annual_limit", "enhanced"),
        supported("شبكة Classic 2R", "network", "enhanced", "arabic", "mixed"),
        supported("ملخص كلاسيك 2R", "summary", "enhanced", "arabic"),
        supported("هل فيه كاشلس في كلاسيك 2R؟", "direct_billing", "enhanced", "arabic"),
        supported("هل لازم referral في كلاسيك 2R؟", "referral", "enhanced", "arabic", "mixed"),
        supported("direct billing في كلاسيك 2R؟", "direct_billing", "enhanced", "arabic", "mixed"),
        supported("كلاسيك 2R network?", "network", "enhanced", "arabic", "mixed"),
        supported("كلاسيك 2R annual limit", "annual_limit", "enhanced", "arabic", "mixed"),
        supported("summarize hn_classic_2r", "summary", "enhanced"),
        supported("هل كلاسيك 2R فيه direct billing؟", "direct_billing", "enhanced", "arabic", "mixed"),
        supported("ما هي منطقة التغطية لخطة Classic 2R؟", "area_of_coverage", "enhanced", "arabic", "mixed"),
        supported("what countries are covered by Classic 2R?", "area_of_coverage", "enhanced"),
        supported("Classic 2R summary", "summary", "enhanced"),
        supported("HN_CLASSIC_2R network", "network", "enhanced"),
        supported("Classic 2R referral?", "referral", "enhanced"),
        supported("Classic 2R direct billing?", "direct_billing", "enhanced"),
        supported("شبكة كلاسيك2R", "network", "enhanced", "arabic"),
        blocked("maternity Classic 2R", "unsupported_benefit", "enhanced", "blocked_benefit"),
        blocked("pharmacy Classic 2R", "unsupported_benefit", "enhanced", "blocked_benefit"),
        blocked("dental Classic 2R", "unsupported_benefit", "enhanced", "blocked_benefit"),
        blocked("optical Classic 2R", "unsupported_benefit", "enhanced", "blocked_benefit"),
        blocked("emergency benefit Classic 2R", "unsupported_benefit", "enhanced", "blocked_benefit"),
        blocked("private room Classic 2R", "unsupported_benefit", "enhanced", "blocked_benefit"),
        blocked("chronic condition cover Classic 2R", "unsupported_benefit", "enhanced", "blocked_benefit"),
        blocked("هل كلاسيك 2R يغطي maternity؟", "unsupported_benefit", "enhanced", "blocked_benefit", "arabic", "mixed"),
        blocked("هل في pharmacy في كلاسيك 2R؟", "unsupported_benefit", "enhanced", "blocked_benefit", "arabic", "mixed"),
        blocked("هل يغطي dental في كلاسيك 2R؟", "unsupported_benefit", "enhanced", "blocked_benefit", "arabic", "mixed"),
        blocked("optical benefit في Classic 2R؟", "unsupported_benefit", "enhanced", "blocked_benefit", "arabic", "mixed"),
        blocked("لو عنده chronic condition في Classic 2R؟", "unsupported_benefit", "enhanced", "blocked_benefit", "arabic", "mixed"),
        blocked("inpatient room benefit Classic 2R", "unsupported_benefit", "enhanced", "blocked_benefit"),
        blocked("does Classic 2R cover physiotherapy?", "unsupported_benefit", "enhanced", "blocked_benefit"),
    ],
)

COMPARISON_CASES = build_cases(
    "comparison_pressure",
    [
        supported("Compare Classic 2 and Classic 3", "comparison_supported", "comparison"),
        supported("قارن بين Classic 2 و Classic 3", "comparison_supported", "comparison", "arabic", "mixed"),
        supported("compare Remedy 02 and Remedy 05", "comparison_supported", "comparison"),
        supported("compare Remedy 03 and Remedy 06", "comparison_supported", "comparison"),
        supported("Compare Remedy 02 and Remedy 06", "comparison_supported", "comparison"),
        supported("قارن بين Remedy 02 و Remedy 05", "comparison_supported", "comparison", "arabic", "mixed"),
        supported("Compare Classic 3 and Classic 2", "comparison_supported", "comparison"),
        supported("compare Remedy 05 and Remedy 06", "comparison_supported", "comparison"),
        supported("Compare Remedy 02 و Remedy 05", "comparison_supported", "comparison", "arabic", "mixed"),
        supported("قارن Classic 2 and Classic 3", "comparison_supported", "comparison", "arabic", "mixed"),
        blocked("Compare Classic 2R and Classic 3", "comparison_blocked", "comparison", "enhanced"),
        blocked("قارن بين Classic 2R و Classic 3", "comparison_blocked", "comparison", "enhanced", "arabic", "mixed"),
        blocked("compare all plans", "comparison_blocked", "comparison"),
        blocked("Can you compare all enhanced plans?", "comparison_blocked", "comparison", "enhanced"),
        blocked("compare Classic 2 and Remedy 99", "comparison_blocked", "comparison"),
        blocked("Compare Classic 2R and Remedy 05", "comparison_blocked", "comparison", "enhanced"),
        blocked("دي احسن ولا دي؟", "comparison_malformed", "comparison", "arabic"),
        blocked("compare two best plans", "comparison_malformed", "comparison"),
        blocked("قارن", "comparison_malformed", "comparison", "arabic"),
        blocked("compare Classic 2", "comparison_malformed", "comparison"),
        blocked("هل Classic 2R احسن من Classic 3؟", "comparison_blocked", "comparison", "enhanced", "arabic", "mixed"),
        blocked("compare Remedy and Classic", "comparison_malformed", "comparison"),
        blocked("قارن بين Plan A و Plan B", "comparison_malformed", "comparison", "arabic", "mixed"),
        blocked("Compare Classic 2R and Classic 2", "comparison_blocked", "comparison", "enhanced"),
        blocked("Compare Classic 2R and Classic 2R", "comparison_blocked", "comparison", "enhanced"),
        blocked("دي احسن ولا Classic 2؟", "comparison_malformed", "comparison", "arabic", "mixed"),
        blocked("Which is better, Remedy 02 or Remedy 05?", "comparison_malformed", "comparison"),
        blocked("انهي افضل Remedy 02 ولا Remedy 05؟", "comparison_malformed", "comparison", "arabic", "mixed"),
        blocked("compare Remedy 05 with unknown plan", "comparison_blocked", "comparison"),
        blocked("قارن بين كل الخطط", "comparison_blocked", "comparison", "arabic"),
    ],
)

RECOMMENDATION_CASES = build_cases(
    "recommendation_oos_pressure",
    [
        blocked("Which plan should I recommend to a family?", "recommendation", "recommendation"),
        blocked("Recommend one plan for outpatient heavy usage", "recommendation", "recommendation"),
        blocked("best enhanced plan overall", "recommendation", "recommendation", "enhanced"),
        blocked("What is the best value plan?", "recommendation", "recommendation"),
        blocked("Which plan do brokers usually sell most?", "recommendation", "recommendation"),
        blocked("تنصحني باي خطة؟", "recommendation", "recommendation", "arabic"),
        blocked("أفضل خطة بشكل عام؟", "recommendation", "recommendation", "arabic"),
        blocked("محتاج توصية لخطة مناسبة للعميل ده", "recommendation", "recommendation", "arabic"),
        blocked("لو عنده chronic condition أنصحه بإيه؟", "recommendation", "recommendation", "arabic", "mixed"),
        blocked("هل دي تنفع لعيلة؟", "recommendation", "recommendation", "arabic"),
        blocked("What is the price of Classic 2R?", "pricing", "recommendation", "pricing", "enhanced"),
        blocked("pricing for Remedy 05", "pricing", "recommendation", "pricing"),
        blocked("how much premium for Classic 3", "pricing", "recommendation", "pricing"),
        blocked("quote me for a 45-year-old diabetic", "underwriting", "recommendation", "underwriting"),
        blocked("underwriting requirements for maternity case", "underwriting", "recommendation", "underwriting"),
        blocked("what is the commission on Remedy 06", "business_advice", "recommendation"),
        blocked("which plan is better for diabetes?", "recommendation", "recommendation", "underwriting"),
        blocked("recommend a low-cost plan with strong network", "recommendation", "recommendation"),
        blocked("can you advise on underwriting acceptance?", "underwriting", "recommendation", "underwriting"),
        blocked("Which plan is cheapest with direct billing?", "recommendation", "recommendation", "pricing"),
    ],
)

BROKER_ARABIC_CASES = build_cases(
    "broker_style_arabic_pressure",
    [
        blocked("العميل ده ينفعله ايه؟", "broker_recommendation", "arabic", "recommendation"),
        blocked("الشبكة دي قوية؟", "broker_vague", "arabic"),
        blocked("فيها كاشلس؟", "broker_vague", "arabic"),
        blocked("دي أفضل ولا التانية؟", "broker_comparison_vague", "arabic", "comparison"),
        blocked("لو عنده chronic condition؟", "broker_recommendation", "arabic", "underwriting"),
        blocked("تنفع لعيلة؟", "broker_recommendation", "arabic"),
        not_found_safe("المستشفى دي تبع انهي شبكة؟", "broker_provider_vague", "arabic", "provider"),
        supported("ليمت كلاسيك 2R", "annual_limit", "arabic", "enhanced"),
        supported("ملخص ريميدي 05", "summary", "arabic"),
        supported("Remedy 6 في دبي فيها providers ايه؟", "city_query", "arabic", "mixed", "provider", "city"),
        supported("برجيل أبوظبي في أي شبكة؟", "provider_alias", "arabic", "mixed", "provider"),
        supported("أستر القصيص في أي شبكة؟", "provider_alias", "arabic", "provider"),
        supported("هل ريميدي 06 فيها direct billing؟", "direct_billing", "arabic", "mixed"),
        supported("كلاسيك 2 cashless؟", "direct_billing", "arabic", "mixed"),
        supported("مقارنة Classic 2 مع Classic 3", "comparison_supported", "arabic", "mixed", "comparison"),
        blocked("Classic 2R ولا Classic 3؟", "comparison_blocked", "arabic", "mixed", "comparison", "enhanced"),
        blocked("عايز سعر كلاسيك 3", "pricing", "arabic", "pricing"),
        blocked("لو عميل عنده سكر اطلعله انهي خطة؟", "broker_recommendation", "arabic", "underwriting"),
        ambiguity_safe("الشبكة دي تبع برجيل ولا لا؟", "broker_provider_ambiguity", "arabic", "provider", "ambiguous"),
        supported("هل ميديكلينيك القصيص في الشبكة؟", "provider_lookup", "arabic", "provider"),
    ],
)

CASES = (
    REMEDY_CORE_CASES
    + PROVIDER_NETWORK_CASES
    + ENHANCED_BASELINE_CASES
    + COMPARISON_CASES
    + RECOMMENDATION_CASES
    + BROKER_ARABIC_CASES
)


def validate_pack() -> None:
    counts = Counter(case.section for case in CASES)
    if len(CASES) != 200:
        raise ValueError(f"Expected 200 cases, found {len(CASES)}")
    for section, expected_count in EXPECTED_SECTION_COUNTS.items():
        actual_count = counts.get(section, 0)
        if actual_count != expected_count:
            raise ValueError(f"Section {section} expected {expected_count} cases, found {actual_count}")
    queries = [case.query for case in CASES]
    if len(set(queries)) != len(queries):
        duplicates = [query for query, count in Counter(queries).items() if count > 1]
        raise ValueError(f"Duplicate queries found: {duplicates}")


def run_query(query: str) -> dict:
    cmd = [sys.executable, "-m", "src.agent_entrypoint", "--json", query]
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip() or "Entrypoint execution failed."
        return {
            "ok": False,
            "intent": "error",
            "plan_name": None,
            "tool_name": None,
            "message": message,
            "normalized": {"status": "error", "tool": None, "answer": None, "errors": [message]},
            "_execution_error": True,
        }
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        message = f"Invalid JSON output: {exc}"
        return {
            "ok": False,
            "intent": "error",
            "plan_name": None,
            "tool_name": None,
            "message": message,
            "normalized": {"status": "error", "tool": None, "answer": None, "errors": [message]},
            "_execution_error": True,
        }
    return payload


def message_text(result: dict) -> str:
    return str(result.get("message") or "")


def message_has(text: str, needles: tuple[str, ...]) -> bool:
    lowered = text.casefold()
    return any(needle.casefold() in lowered for needle in needles)


def is_safe_block(result: dict) -> bool:
    if bool(result.get("ok")):
        return False
    intent = result.get("intent")
    if intent in {"unsupported", "plan_comparison"}:
        return True
    if intent == "network_lookup":
        return message_has(message_text(result), SAFE_BLOCK_TERMS)
    return message_has(message_text(result), SAFE_BLOCK_TERMS)


def failure_pattern(case: PressureCase, result: dict, classification: str) -> str | None:
    if classification == "BLOCKED_OK":
        if case.expected == "ambiguity_safe":
            return "safe_provider_ambiguity_block"
        if case.expected == "not_found_safe":
            return "safe_provider_not_found_block"
        if case.section == "recommendation_oos_pressure":
            return f"safe_{case.theme}_block"
        if case.section == "enhanced_baseline_classic2r" and "blocked_benefit" in case.tags:
            return "safe_enhanced_unsupported_benefit_block"
        if case.section == "comparison_pressure":
            return "safe_comparison_block"
        if case.section == "broker_style_arabic_pressure":
            return "safe_broker_vague_block"
        return f"safe_{case.theme}_block"

    if classification == "GOOD":
        return None

    if result.get("_execution_error"):
        return "entrypoint_execution_failure"

    msg = message_text(result)
    intent = str(result.get("intent") or "")

    if case.section == "provider_network_pressure" or "provider" in case.tags:
        if message_has(msg, ("ambiguous provider", "مزود غير محدد")):
            return "provider_ambiguity_weakness"
        if message_has(msg, ("provider not found", "المزود غير موجود")):
            return "provider_alias_or_dataset_weakness"
        if intent == "unsupported":
            return "provider_query_routed_to_unsupported"
        return "provider_lookup_review"

    if case.section == "comparison_pressure" or "comparison" in case.tags:
        if intent == "unsupported":
            return "comparison_routed_to_unsupported"
        if intent == "plan_comparison" and not bool(result.get("ok")):
            return "comparison_extraction_or_policy_block"
        return "comparison_review"

    if case.section == "enhanced_baseline_classic2r" or "enhanced" in case.tags:
        if bool(result.get("ok")):
            return "enhanced_baseline_response_review"
        return "enhanced_baseline_routing_or_blocking_weakness"

    if case.section == "recommendation_oos_pressure" or "recommendation" in case.tags:
        if bool(result.get("ok")):
            return "unsafe_out_of_scope_answer"
        return "out_of_scope_block_review"

    if "arabic" in case.tags or "mixed" in case.tags:
        return "arabic_or_mixed_normalization_weakness"

    if intent == "unsupported":
        return "supported_query_fell_to_unsupported"
    if intent == "network_lookup" and not bool(result.get("ok")):
        return "network_lookup_resolution_weakness"
    return "supported_query_review"


def classify_case(case: PressureCase, result: dict) -> tuple[str, str, str | None]:
    ok = bool(result.get("ok"))
    intent = str(result.get("intent") or "")
    msg = message_text(result)

    if result.get("_execution_error"):
        return "GAP", "Entrypoint execution failed or returned invalid JSON.", "entrypoint_execution_failure"

    if case.expected == "supported":
        if ok and intent in SUPPORTED_OK_INTENTS:
            return "GOOD", "Deterministic supported response returned.", None
        return "REVIEW", "Supported query did not return the expected deterministic supported path.", failure_pattern(case, result, "REVIEW")

    if case.expected == "blocked":
        if is_safe_block(result):
            return "BLOCKED_OK", "Safe blocking preserved for unsupported or out-of-scope behavior.", failure_pattern(case, result, "BLOCKED_OK")
        if ok:
            return "GAP", "Blocked probe returned a substantive answer.", "unsafe_block_boundary_exposure"
        return "REVIEW", "Blocked probe needs manual review.", failure_pattern(case, result, "REVIEW")

    if case.expected == "ambiguity_safe":
        if not ok and message_has(msg, ("ambiguous provider", "مزود غير محدد")):
            return "BLOCKED_OK", "Ambiguous provider was surfaced safely without hallucination.", failure_pattern(case, result, "BLOCKED_OK")
        if ok:
            return "REVIEW", "Ambiguous provider probe resolved to a substantive answer and needs review.", "provider_ambiguity_weakness"
        return "REVIEW", "Ambiguous provider probe did not return the expected safe ambiguity signal.", "provider_ambiguity_weakness"

    if case.expected == "not_found_safe":
        if not ok and message_has(msg, ("provider not found", "المزود غير موجود", "مزود غير محدد", "ambiguous provider")):
            return "BLOCKED_OK", "Safe provider not-found or ambiguity response returned without hallucination.", failure_pattern(case, result, "BLOCKED_OK")
        if ok:
            return "REVIEW", "Provider not-found probe returned a substantive answer and needs review.", "provider_alias_or_dataset_weakness"
        return "REVIEW", "Provider not-found probe did not return the expected safe signal.", "provider_alias_or_dataset_weakness"

    return "REVIEW", "Unknown expected classification path.", "classification_workflow_gap"


def parse_previous_counts() -> dict[str, int]:
    if not PREVIOUS_RESULTS_PATH.exists():
        return {}
    text = PREVIOUS_RESULTS_PATH.read_text(encoding="utf-8")
    counts = {}
    for label in ("GOOD", "REVIEW", "BLOCKED_OK", "GAP"):
        match = re.search(rf"- total {label}: (\d+)", text)
        if match:
            counts[label] = int(match.group(1))
    return counts


def render_pack(cases: list[PressureCase]) -> str:
    lines = [
        "# Operational Pressure 200 Pack",
        "",
        "## Scope",
        "- Mode: operational pressure sprint evidence only",
        "- Execution path: `python -m src.agent_entrypoint --json <query>`",
        "- Boundaries: no feature expansion, no RAG, no embeddings, no recommendation AI, no pricing engine",
        "- Total questions: 200",
        "",
        "## Composition",
    ]
    counts = Counter(case.section for case in cases)
    for section, title in SECTION_TITLES.items():
        lines.append(f"- {title}: {counts[section]}")
    for section, title in SECTION_TITLES.items():
        section_cases = [case for case in cases if case.section == section]
        lines.extend(["", f"## {title}"])
        for index, case in enumerate(section_cases, start=1):
            lines.append(f"- {index}. {case.query}")
    return "\n".join(lines) + "\n"


def render_results(cases: list[PressureCase], records: list[dict], counts: Counter[str]) -> str:
    lines = [
        "# Operational Pressure 200 Results",
        "",
        "## Run Context",
        "- Mode: OPERATIONAL PRESSURE SPRINT",
        "- Execution path: `python -m src.agent_entrypoint --json <query>`",
        "- Scope: evidence and deterministic classification only",
        "- Total questions: 200",
        "",
        "## Summary",
        f"- total GOOD: {counts['GOOD']}",
        f"- total REVIEW: {counts['REVIEW']}",
        f"- total BLOCKED_OK: {counts['BLOCKED_OK']}",
        f"- total GAP: {counts['GAP']}",
    ]
    for section, title in SECTION_TITLES.items():
        section_records = [record for record in records if record["case"].section == section]
        section_counts = Counter(record["classification"] for record in section_records)
        lines.extend(
            [
                "",
                f"## {title}",
                f"- GOOD: {section_counts['GOOD']}",
                f"- REVIEW: {section_counts['REVIEW']}",
                f"- BLOCKED_OK: {section_counts['BLOCKED_OK']}",
                f"- GAP: {section_counts['GAP']}",
            ]
        )
        for index, record in enumerate(section_records, start=1):
            case = record["case"]
            result = record["result"]
            lines.extend(
                [
                    "",
                    f"### {index}. {case.query}",
                    f"- intent: {result.get('intent')}",
                    f"- tool: {result.get('tool_name') or 'None'}",
                    f"- plan: {result.get('plan_name') or 'None'}",
                    f"- classification: {record['classification']}",
                    f"- reason: {record['reason']}",
                    "- output:",
                    "```text",
                    message_text(result) or "",
                    "```",
                ]
            )
    return "\n".join(lines) + "\n"


def top_items(counter: Counter[str], limit: int = 10) -> list[tuple[str, int]]:
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:limit]


def recommend_next_sprint(review_patterns: Counter[str], gap_patterns: Counter[str]) -> str:
    dominant = top_items(review_patterns + gap_patterns, limit=3)
    if not dominant:
        return "Keep the same evidence pack and focus the next sprint on replay automation and routine reruns."
    names = ", ".join(name for name, _ in dominant)
    return (
        "Prioritize a narrow hardening sprint for the dominant failure patterns: "
        f"{names}. Keep it routing and normalization only, and replay this same 200-pack afterward."
    )


def render_delta(records: list[dict], counts: Counter[str]) -> str:
    previous_counts = parse_previous_counts()
    review_patterns = Counter(
        record["pattern"]
        for record in records
        if record["classification"] == "REVIEW" and record["pattern"]
    )
    gap_patterns = Counter(
        record["pattern"]
        for record in records
        if record["classification"] == "GAP" and record["pattern"]
    )
    blocked_patterns = Counter(
        record["pattern"]
        for record in records
        if record["classification"] == "BLOCKED_OK" and record["pattern"]
    )
    provider_records = [record for record in records if record["case"].section == "provider_network_pressure"]
    provider_counts = Counter(record["classification"] for record in provider_records)
    enhanced_records = [record for record in records if record["case"].section == "enhanced_baseline_classic2r"]
    enhanced_counts = Counter(record["classification"] for record in enhanced_records)
    recommendation_records = [record for record in records if record["case"].section == "recommendation_oos_pressure"]
    recommendation_counts = Counter(record["classification"] for record in recommendation_records)
    arabic_weaknesses = [
        record for record in records
        if record["classification"] in {"REVIEW", "GAP"} and any(tag in {"arabic", "mixed"} for tag in record["case"].tags)
    ]
    provider_ambiguity_weaknesses = [
        record for record in provider_records
        if record["classification"] in {"REVIEW", "GAP"} and "ambiguous" in record["case"].tags
    ]
    enhanced_weaknesses = [
        record for record in enhanced_records if record["classification"] in {"REVIEW", "GAP"}
    ]
    routing_weaknesses = [
        record for record in records
        if record["pattern"] and "routed" in record["pattern"]
    ]
    all_failure_patterns = review_patterns + gap_patterns

    lines = ["# Operational Pressure 200 Delta", ""]
    if previous_counts:
        lines.extend(["## Count Delta vs Existing 100-Query Evidence Pack"])
        for label in ("GOOD", "REVIEW", "BLOCKED_OK", "GAP"):
            previous = previous_counts.get(label, 0)
            current = counts[label]
            delta = current - previous
            lines.append(f"- {label}: {previous} -> {current} (delta {delta:+d})")
    else:
        lines.extend([
            "## Count Delta",
            "- Previous 100-query evidence file not found; no numeric delta available.",
        ])

    lines.extend(
        [
            "",
            "## Provider-Specific Pressure Results",
            f"- GOOD: {provider_counts['GOOD']}",
            f"- REVIEW: {provider_counts['REVIEW']}",
            f"- BLOCKED_OK: {provider_counts['BLOCKED_OK']}",
            f"- GAP: {provider_counts['GAP']}",
            f"- top provider REVIEW patterns: {', '.join(f'{name} ({count})' for name, count in top_items(Counter(record['pattern'] for record in provider_records if record['classification'] == 'REVIEW' and record['pattern']), 5)) or 'None'}",
            "",
            "## Enhanced Baseline Pressure Results",
            f"- GOOD: {enhanced_counts['GOOD']}",
            f"- REVIEW: {enhanced_counts['REVIEW']}",
            f"- BLOCKED_OK: {enhanced_counts['BLOCKED_OK']}",
            f"- GAP: {enhanced_counts['GAP']}",
            f"- enhanced REVIEW/GAP queries: {len(enhanced_weaknesses)}",
            "",
            "## Unsupported Recommendation Safety Results",
            f"- GOOD: {recommendation_counts['GOOD']}",
            f"- REVIEW: {recommendation_counts['REVIEW']}",
            f"- BLOCKED_OK: {recommendation_counts['BLOCKED_OK']}",
            f"- GAP: {recommendation_counts['GAP']}",
        ]
    )

    lines.extend(["", "## Top REVIEW Clusters"])
    for name, count in top_items(review_patterns, 10):
        lines.append(f"- {name}: {count}")
    if not review_patterns:
        lines.append("- None")

    lines.extend(["", "## Top BLOCKED_OK Clusters"])
    for name, count in top_items(blocked_patterns, 10):
        lines.append(f"- {name}: {count}")
    if not blocked_patterns:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Repeated Routing Weaknesses",
            f"- total routing weakness records: {len(routing_weaknesses)}",
        ]
    )
    for record in routing_weaknesses[:10]:
        lines.append(f"- {record['case'].query}")
    if not routing_weaknesses:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Arabic Normalization Weaknesses",
            f"- count: {len(arabic_weaknesses)}",
        ]
    )
    for record in arabic_weaknesses[:10]:
        lines.append(f"- {record['case'].query}")
    if not arabic_weaknesses:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Provider Ambiguity Weaknesses",
            f"- count: {len(provider_ambiguity_weaknesses)}",
        ]
    )
    for record in provider_ambiguity_weaknesses[:10]:
        lines.append(f"- {record['case'].query}")
    if not provider_ambiguity_weaknesses:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Enhanced Baseline Weaknesses",
            f"- count: {len(enhanced_weaknesses)}",
        ]
    )
    for record in enhanced_weaknesses[:10]:
        lines.append(f"- {record['case'].query}")
    if not enhanced_weaknesses:
        lines.append("- None")

    lines.extend(["", "## Top 10 Operational Failure Patterns"])
    for name, count in top_items(all_failure_patterns, 10):
        lines.append(f"- {name}: {count}")
    if not all_failure_patterns:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Recommendation for Next Sprint",
            f"- {recommend_next_sprint(review_patterns, gap_patterns)}",
        ]
    )
    return "\n".join(lines) + "\n"


def execute(cases: list[PressureCase]) -> tuple[list[dict], Counter[str]]:
    records = []
    counts: Counter[str] = Counter()
    for case in cases:
        result = run_query(case.query)
        classification, reason, pattern = classify_case(case, result)
        counts[classification] += 1
        records.append(
            {
                "case": case,
                "result": result,
                "classification": classification,
                "reason": reason,
                "pattern": pattern,
            }
        )
    return records, counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the 200-query operational pressure pack.")
    parser.add_argument("--limit", type=int, default=None, help="Run only the first N queries for validation.")
    parser.add_argument("--no-write", action="store_true", help="Do not write markdown artifacts.")
    args = parser.parse_args()

    validate_pack()
    cases = CASES[: args.limit] if args.limit else CASES
    records, counts = execute(cases)

    if not args.no_write and len(cases) == len(CASES):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        PACK_PATH.write_text(render_pack(CASES), encoding="utf-8")
        RESULTS_PATH.write_text(render_results(CASES, records, counts), encoding="utf-8")
        DELTA_PATH.write_text(render_delta(records, counts), encoding="utf-8")

    print(json.dumps({"counts": counts, "executed": len(cases)}, ensure_ascii=False, indent=2, default=int))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())