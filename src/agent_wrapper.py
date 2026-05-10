PLAN_CORE_FIELDS = [
    "plan name", "plan_name", "plan code", "plan_code", "network", "network name", "network_name",
    "annual limit", "annual_limit", "area of coverage", "area", "area_of_coverage",
    "direct billing", "direct_billing", "cashless", "cash less",
    "referral required", "referral", "referral_required",
    "limit", "limt",
    "اسم الخطة", "رمز الخطة", "الشبكة", "شبكة", "الشبكه", "الحد السنوي",
    "التغطية", "تغطية", "ليمت", "الدفع المباشر", "الإحالة", "تحويل", "ريفرال", "كاشلس", "كاش ليس"
]
"""
Deterministic agent-ready wrapper for the validated runtime.
Phase 1: intent classification, plan extraction, and tool-contract routing.
No AI, LLM, RAG, or fuzzy logic.
"""
from typing import Dict, Any, Optional
from src.tool_contract import get_plan_core, get_reimbursement_rules, get_plan_summary

SUPPORTED_PLANS = {
    # Remedy 02
    "remedy 02": "Remedy 02",
    "remedy 2": "Remedy 02",
    "hn-remedy-2": "Remedy 02",
    "ريميدي 2": "Remedy 02",
    "ريميدي 02": "Remedy 02",
    # Remedy 03
    "remedy 03": "Remedy 03",
    "remedy 3": "Remedy 03",
    "hn-remedy-3": "Remedy 03",
    "ريميدي 3": "Remedy 03",
    "ريميدي 03": "Remedy 03",
    # Remedy 04
    "remedy 04": "Remedy 04",
    "remedy 4": "Remedy 04",
    "hn-remedy-4": "Remedy 04",
    "ريميدي 4": "Remedy 04",
    "ريميدي 04": "Remedy 04",
    # Remedy 05
    "remedy 05": "Remedy 05",
    "remedy 5": "Remedy 05",
    "hn-remedy-5": "Remedy 05",
    "ريميدي 5": "Remedy 05",
    "ريميدي 05": "Remedy 05",
    # Remedy 06
    "remedy 06": "Remedy 06",
    "remedy 6": "Remedy 06",
    "hn-remedy-6": "Remedy 06",
    "ريميدي 6": "Remedy 06",
    "ريميدي 06": "Remedy 06",
    # Classic 2 (plan_core only)
    "classic 2": "Classic 2",
    "classic2": "Classic 2",
    "classic-2": "Classic 2",
    "classic 02": "Classic 2",
    "hnclassic2": "Classic 2",
    "hn_classic_2": "Classic 2",
    "hn-classic-2": "Classic 2",
    "hn classic 2": "Classic 2",
    # Classic 2R
    "classic 2r": "Classic 2R",
    "classic2r": "Classic 2R",
    "classic-2r": "Classic 2R",
    "hn_classic_2r": "Classic 2R",
    "hn-classic-2r": "Classic 2R",
    "hn classic 2r": "Classic 2R",
    "كلاسيك 2r": "Classic 2R",
    # Classic 3
    "classic 3": "Classic 3",
    "classic3": "Classic 3",
    "classic-3": "Classic 3",
    "classic 03": "Classic 3",
    "hnclassic3": "Classic 3",
    "hn_classic_3": "Classic 3",
    "hn-classic-3": "Classic 3",
    "hn classic 3": "Classic 3",
    "كلاسيك 3": "Classic 3",
    "كلاسيك 03": "Classic 3",
    "كلاسيك3": "Classic 3",
    # Prime 1
    "prime 1": "Prime 1",
    "prime1": "Prime 1",
    "prime-1": "Prime 1",
    "hn_prime_1": "Prime 1",
    "hn-prime-1": "Prime 1",
    "hn prime 1": "Prime 1",
    # Prime 2
    "prime 2": "Prime 2",
    "prime2": "Prime 2",
    "prime-2": "Prime 2",
    "hn_prime_2": "Prime 2",
    "hn-prime-2": "Prime 2",
    "hn prime 2": "Prime 2",
    # Classic 1
    "classic 1": "Classic 1",
    "classic1": "Classic 1",
    "classic-1": "Classic 1",
    "classic 01": "Classic 1",
    "hn_classic_1": "Classic 1",
    "hn-classic-1": "Classic 1",
    "hn classic 1": "Classic 1",
    "كلاسيك 1": "Classic 1",
    "كلاسيك 01": "Classic 1",
    # Classic 1R
    "classic 1r": "Classic 1R",
    "classic1r": "Classic 1R",
    "classic-1r": "Classic 1R",
    "hn_classic_1r": "Classic 1R",
    "hn-classic-1r": "Classic 1R",
    "hn classic 1r": "Classic 1R",
    "كلاسيك 1r": "Classic 1R",
    # Classic 4
    "classic 4": "Classic 4",
    "classic4": "Classic 4",
    "classic-4": "Classic 4",
    "classic 04": "Classic 4",
    "hn_classic_4": "Classic 4",
    "hn-classic-4": "Classic 4",
    "hn classic 4": "Classic 4",
    "كلاسيك 4": "Classic 4",
    "كلاسيك 04": "Classic 4",
}

import re

ARABIC_INDIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
EXT_ARABIC_INDIC_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")

COMPARISON_ALIASES = [
    "compare",
    "قارن",
    "مقارنة",
    "الفرق بين",
    "ايه الفرق",
    "فرق",
]

RECOMMENDATION_STYLE_COMPARISON_TERMS = [
    # English
    "better",
    "best",
    "recommend",
    "should i choose",
    "which plan should i choose",
    "should i buy",
    "most suitable",
    "best option",
    # Arabic
    "أفضل",
    "احسن",
    "أحسن",
    "أنسب",
    "تنصح",
    "تنصحني",
    "اختار ايه",
    "اختار إيه",
    "أختار ايه",
    "أختار إيه",
    "الافضل",
    "الأفضل",
]

NORMALIZATION_REPLACEMENTS = {
    "برجيل": "burjeel",
    "بيسك بلس": "basic plus",
    "شبكة بيسك بلس": "basic plus",
    "كاشلس": "direct billing",
    "كاش ليس": "direct billing",
    "ليمت": "annual limit",
    "ريفرال": "referral",
    "الشبكة": "network",
    "شبكه": "network",
    "شبكة": "network",
}

NETWORK_LOOKUP_PATTERNS = [
    r"is .+ in the network",
    r"which network tiers is .+ available in",
    r"which network tiers for .+",
    r"which network is .+ available in",
    r"what city is .+ located in",
    r"what city for .+",
    r"what type of provider is .+",
    r"what type is .+",
    r".+ in which network",
    r"is .+ in (basic plus|hn basic plus)",
    r"show (hospitals|clinics|labs|pharmacies|medical centers?) in [a-z\s]+",
    r"(providers in|dubai providers|remedy\s?0?6 dubai providers)",
    r"هل .+ داخل الشبكة",
    r"هل .+ داخل network",
    r"هل .+ في الشبكة",
    r"هل .+ في network",
    r"هل .+ ضمن الشبكة",
    r"هل .+ ضمن network",
    r"هل .+ في (?:شبكة )?بيسك بلس",
    r"هل .+ في basic plus",
    r"هل يوجد direct billing في هذه (?:العيادة|المستشفى|المركز)",
    r"(هاتلي )?(مستشفيات|عيادات|تحاليل|مراكز أشعة) في .+",
    r"عيادات في .+",
    r"في أي شبكة .+",
    r".+ في أي شبكة",
    r"في اي شبكة .+",
    r".+ في اي شبكة",
    r"في أي network .+",
    r".+ في أي network",
    r"في اي network .+",
    r".+ في اي network",
    r"ما نوع المزود .+",
    r"في أي مدينة يقع .+",
]

CITY_ALIASES = {
    "dubai": "Dubai",
    "دبي": "Dubai",
    "abu dhabi": "Abu Dhabi",
    "abudhabi": "Abu Dhabi",
    "abu-dhabi": "Abu Dhabi",
    "ابوظبي": "Abu Dhabi",
    "أبوظبي": "Abu Dhabi",
    "ابو ظبي": "Abu Dhabi",
    "أبو ظبي": "Abu Dhabi",
    "sharjah": "Sharjah",
    "الشارقة": "Sharjah",
    "شارقة": "Sharjah",
    "ajman": "Ajman",
    "عجمان": "Ajman",
}

PROVIDER_TYPE_ALIASES = {
    "hospital": "hospital",
    "hospitals": "hospital",
    "مستشفى": "hospital",
    "مستشفيات": "hospital",
    "clinic": "clinic",
    "clinics": "clinic",
    "medical center": "clinic",
    "medical centers": "clinic",
    "عيادة": "clinic",
    "عيادات": "clinic",
    "مركز طبي": "clinic",
    "مراكز طبية": "clinic",
    "pharmacy": "pharmacy",
    "pharmacies": "pharmacy",
    "صيدلية": "pharmacy",
    "صيدليات": "pharmacy",
    "lab": "lab",
    "labs": "lab",
    "laboratory": "lab",
    "laboratories": "lab",
    "diagnostic center": "lab",
    "diagnostic centers": "lab",
    "مختبر": "lab",
    "مختبرات": "lab",
    "تحليل": "lab",
    "تحاليل": "lab",
}

NETWORK_LABELS = {
    "hn_basic_plus": "HN Basic Plus",
    "hn_standard_plus": "HN Standard Plus",
    "hn_standard": "HN Standard",
    "hn_premier": "HN Premier",
    "hn_advantage": "HN Advantage",
    "hn_exclusive": "HN Exclusive",
    "hn_basic": "HN Basic",
}


def _normalize_query_text(text: str) -> str:
    normalized = (text or "").lower().translate(ARABIC_INDIC_DIGITS).translate(EXT_ARABIC_INDIC_DIGITS)
    normalized = normalized.replace("؟", "?")
    # Canonical spacing for known plan tokens.
    normalized = re.sub(r"classic\s*([0-9]+)\s*r", r"classic \1r", normalized)
    normalized = re.sub(r"classic\s*([0-9]+)", r"classic \1", normalized)
    normalized = re.sub(r"remedy\s*([0-9]+)", r"remedy \1", normalized)
    normalized = re.sub(r"كلاسيك\s*([0-9]+)\s*r", r"كلاسيك \1r", normalized)
    normalized = re.sub(r"كلاسيك\s*([0-9]+)", r"كلاسيك \1", normalized)
    normalized = re.sub(r"ريميدي\s*([0-9]+)", r"ريميدي \1", normalized)
    # Minimal Arabic plan alias normalization for mixed routing.
    normalized = re.sub(r"\bريميدي\b", "remedy", normalized)
    normalized = re.sub(r"\bريمدي\b", "remedy", normalized)
    normalized = re.sub(r"\bكلاسيك\b", "classic", normalized)
    for src, dst in NORMALIZATION_REPLACEMENTS.items():
        normalized = normalized.replace(src, dst)
    # Minimal separator normalization for comparison parsing.
    normalized = re.sub(r"\bversus\b", "vs", normalized)
    normalized = re.sub(r"\breferral\?", "referral", normalized)
    normalized = re.sub(r"([0-9])(referral|network|annual|limit|direct)", r"\1 \2", normalized)
    normalized = re.sub(r"\band\b", " and ", normalized)
    normalized = re.sub(r"\s+و\s+", " and ", normalized)
    return " ".join(normalized.split())


def _has_comparison_alias(text: str) -> bool:
    lowered = _normalize_query_text(text)
    return any(alias in lowered for alias in COMPARISON_ALIASES)


def _is_recommendation_style_comparison_query(text: str) -> bool:
    lowered = _normalize_query_text(text)
    has_rec_term = any(term.lower() in lowered for term in RECOMMENDATION_STYLE_COMPARISON_TERMS)
    if not has_rec_term:
        return False
    plans = _extract_all_plan_names(lowered)
    if len(plans) >= 2:
        return True
    if _has_comparison_alias(lowered):
        return True
    # Also block broad recommendation-style plan selection prompts.
    return "which plan" in lowered or "خطة" in lowered


def _is_network_lookup_query(text: str) -> bool:
    lowered = _normalize_query_text(text)
    for pat in NETWORK_LOOKUP_PATTERNS:
        if re.search(pat, lowered, re.IGNORECASE):
            return True
    return False


def _contains_alias(text: str, key: str) -> bool:
    pattern = r"(^|[\s\-_/?:.,؛،!؟()\[\]{}])" + re.escape(key) + r"($|[\s\-_/?:.,؛،!؟()\[\]{}])"
    return re.search(pattern, text) is not None

PLAN_COMPARISON_PATTERNS = [
    r"compare (remedy|ريميدي) ?0?2 and (remedy|ريميدي) ?0?3",
    r"compare (remedy|ريميدي) ?0?2 and (remedy|ريميدي) ?0?4",
    r"compare (remedy|ريميدي) ?0?3 and (remedy|ريميدي) ?0?4",
    r"ما الفرق بين ريميدي 02 و ريميدي 04",
    r"ما الفرق بين ريميدي 02 و ريميدي 03",
    r"ما الفرق بين ريميدي 03 و ريميدي 04",
    r"قارن ريميدي 02 و ريميدي 04",
    r"قارن ريميدي 02 و ريميدي 03",
    r"قارن ريميدي 03 و ريميدي 04",
    r"compare remedy [0-9]+ and remedy [0-9]+",
    r"ما الفرق بين ريميدي [0-9]+ و ريميدي [0-9]+",
    r"قارن ريميدي [0-9]+ و ريميدي [0-9]+",
]

def _extract_comparison_plans(text: str) -> Optional[tuple[str, str]]:
    # Extract two plan names from the query (English or Arabic)
    # Accepts: compare Remedy 02 and Remedy 04, ما الفرق بين ريميدي 02 و ريميدي 04
    # Returns canonical names if both are supported
    text = _normalize_query_text(text)
    # English
    m = re.search(r"remedy ?0?(\d+)\s*(?:and|vs|بين)\s*remedy ?0?(\d+)", text)
    if m:
        p1, p2 = m.group(1), m.group(2)
        n1, n2 = f"Remedy 0{p1}" if len(p1)==1 else f"Remedy {p1}", f"Remedy 0{p2}" if len(p2)==1 else f"Remedy {p2}"
        if n1 in SUPPORTED_PLANS.values() and n2 in SUPPORTED_PLANS.values():
            return n1, n2
    # Generic extraction for mixed Arabic/English and Classic plans.
    has_separator = any(sep in text for sep in (" and ", " vs ", " بين "))
    all_plans = _extract_all_plan_names(text)
    if (has_separator or _has_comparison_alias(text)) and len(all_plans) >= 2:
        return all_plans[0], all_plans[1]
    return None

REIMBURSEMENT_FIELDS = [
    "reimbursement", "reimbursement allowed", "reimbursement scope", "outside network reimbursement",
    "outside uae reimbursement", "reimbursement basis", "reimbursement conditions",
    "reimbursement documents required", "documents required for reimbursement",
    "تعويض", "نطاق التعويض", "تعويض خارج الشبكة", "تعويض خارج الإمارات", "أساس التعويض", "شروط التعويض", "مستندات التعويض المطلوبة"
]

SUMMARY_PATTERNS = [
    "summarize", "summary", "overview", "give me a summary", "plan summary", "tell me about", "ملخص", "اعطني ملخص", "أعطني ملخص", "عرض ملخص", "لخص", "ملخص لخطة", "summary لخطة", "ملخص plan", "اعطني summary", "اعطني ملخص لخطة", "ملخص Remedy", "ملخص ريميدي"
]

def _extract_plan_name(text: str) -> Optional[str]:
    lowered = _normalize_query_text(text)
    found = []
    for key in sorted(SUPPORTED_PLANS.keys(), key=len, reverse=True):
        canonical = SUPPORTED_PLANS[key]
        if _contains_alias(lowered, key):
            found.append(canonical)
    if found:
        return found[0]
    return None

def _extract_all_plan_names(text: str) -> list[str]:
    lowered = _normalize_query_text(text)
    found = []
    for key in sorted(SUPPORTED_PLANS.keys(), key=len, reverse=True):
        canonical = SUPPORTED_PLANS[key]
        if _contains_alias(lowered, key) and canonical not in found:
            found.append(canonical)
    return found


def _extract_city_and_provider_type(text: str) -> tuple[Optional[str], Optional[str]]:
    lowered = _normalize_query_text(text)
    detected_city = None
    detected_type = None

    for alias, canonical in sorted(CITY_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if alias in lowered:
            detected_city = canonical
            break

    for alias, canonical in sorted(PROVIDER_TYPE_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if alias in lowered:
            detected_type = canonical
            break

    return detected_city, detected_type

# Patterns that signal a provider-in-plan membership query.
# These must be checked BEFORE the PLAN_CORE_FIELDS loop because "network" is in that list.
# All patterns are applied to the normalized (lowercased) query text.
import re as _re
_PROVIDER_MEMBERSHIP_PATTERNS = [
    # "Is X in Remedy Y network?" / "Is X in Classic Y network?"
    _re.compile(r"^is\s+(?!(?:direct\s+billing|annual\s+limit|network|limit|referral|maternity|dental|optical|vision|pharmacy|reimbursement|coverage|available|cashless|covered|provided|included|offered|accepted|the)\b)\S.+\s+in\s+(?:remedy|classic)\s*\S+\s+network\??$", _re.IGNORECASE),
    # "Is X in Remedy Y?" (without trailing "network")
    _re.compile(r"^is\s+(?!(?:direct\s+billing|annual\s+limit|network|limit|referral|maternity|dental|optical|vision|pharmacy|reimbursement|coverage|available|cashless|covered|provided|included|offered|accepted|the)\b)\S.+\s+in\s+(?:remedy|classic)\s*\S+\??$", _re.IGNORECASE),
    # "Provider X in Remedy Y network?"
    _re.compile(r"^provider\s+\S.+\s+in\s+(?:remedy|classic)\s*\S+\s+network\??$", _re.IGNORECASE),
    # "X - Remedy Y - network?"
    _re.compile(r"^(?!(?:what|summarize|summary|annual\s+limit|network|direct\s+billing|referral)\b)\S.+\s*-\s*(?:remedy|classic)\s*\S+\s*-\s*network\??$", _re.IGNORECASE),
    # "X Remedy Y network?"
    _re.compile(r"^(?!(?:what|summarize|summary|annual\s+limit|network|direct\s+billing|referral)\b)\S.+\s+(?:remedy|classic)\s*\S+\s+network\??$", _re.IGNORECASE),
    # Arabic (raw): "هل X في شبكة Remedy Y؟" or "هل X داخل شبكة Remedy Y؟"
    _re.compile(r"^هل\s+\S.+\s+(?:في شبكة|داخل شبكة|داخل)\s+(?:remedy|classic)\s*\S+\??$", _re.IGNORECASE),
    # Arabic (raw): "هل X في Remedy Y؟" or "هل X داخل Remedy Y؟"
    _re.compile(r"^هل\s+\S.+\s+(?:في|داخل)\s+(?:remedy|classic)\s*\S+\??$", _re.IGNORECASE),
    # Arabic (normalized: شبكة → network): "هل X في network Remedy Y؟" or "هل X داخل network Remedy Y؟"
    _re.compile(r"^هل\s+\S.+\s+(?:في|داخل)\s+network\s+(?:remedy|classic)\s*\S+\??$", _re.IGNORECASE),
]

def _is_provider_membership_query(lowered_text: str) -> bool:
    """Return True if the normalized query looks like a provider-in-plan membership check."""
    for pat in _PROVIDER_MEMBERSHIP_PATTERNS:
        if pat.match(lowered_text.strip()):
            return True
    return False

# Ordered extractors: try to pull the provider name from a membership query.
# Applied to raw query first, then to normalized query, stopping on first match.
_MEMBERSHIP_PROVIDER_EXTRACTORS = [
    # "Is PROVIDER in Remedy Y network?" / "Is PROVIDER in Classic Y network?"
    _re.compile(r"^is\s+(.+?)\s+in\s+(?:remedy|classic)\s*\S+(?:\s+network)?\??$", _re.IGNORECASE),
    # "Provider PROVIDER in Remedy Y network?"
    _re.compile(r"^provider\s+(.+?)\s+in\s+(?:remedy|classic)\s*\S+\s+network\??$", _re.IGNORECASE),
    # "PROVIDER - Remedy Y - network?"
    _re.compile(r"^(.+?)\s*-\s*(?:remedy|classic)\s*\S+\s*-\s*network\??$", _re.IGNORECASE),
    # "PROVIDER Remedy Y network?"
    _re.compile(r"^(.+?)\s+(?:remedy|classic)\s*\S+\s+network\??$", _re.IGNORECASE),
    # Arabic (raw): "هل PROVIDER في شبكة Plan؟" / "هل PROVIDER داخل شبكة Plan؟"
    _re.compile(r"^هل\s+(.+?)\s+(?:في شبكة|داخل شبكة|في|داخل)\s+(?:remedy|classic)\s*\S+\??$", _re.IGNORECASE),
    # Arabic (normalized: شبكة → network): "هل PROVIDER في network Plan؟"
    _re.compile(r"^هل\s+(.+?)\s+(?:في|داخل)\s+network\s+(?:remedy|classic)\s*\S+\??$", _re.IGNORECASE),
    # Shorthand: "PROVIDER Remedy N?" (last resort — least specific)
    _re.compile(r"^(.+?)\s+(?:remedy|classic)\s*\S+(?:\s+network)?\??$", _re.IGNORECASE),
]

_PLAN_KEYWORD_RE = _re.compile(r"^(?:is|what|list|show|هل|كم|ما|اعرض|remedy|classic)\b", _re.IGNORECASE)

def _extract_provider_from_membership_query(query: str) -> Optional[str]:
    """Extract provider name from a provider-in-plan membership query (raw or normalized)."""
    candidates = [query.strip(), _normalize_query_text(query).strip()]
    for q in candidates:
        for pat in _MEMBERSHIP_PROVIDER_EXTRACTORS:
            m = pat.match(q)
            if m:
                prov = m.group(1).strip().strip("؟?.,:-")
                # Reject if the extracted "provider" looks like a plan or routing keyword
                if prov and not _PLAN_KEYWORD_RE.match(prov):
                    return prov
    return None

def _intent_from_query(text: str) -> Optional[str]:
    lowered = _normalize_query_text(text)
    plan_name = _extract_plan_name(lowered)
    if _is_recommendation_style_comparison_query(lowered):
        return "recommendation_style_comparison"
    # Special-case: route explicit "maternity limit" with plan to plan_core
    if "maternity limit" in lowered:
        if plan_name:
            return "plan_core"
    # Classic 3 coverage phrasing is common in broker usage.
    if plan_name == "Classic 3" and any(token in lowered for token in ("coverage", "covered")):
        return "plan_core"
    # Keep Classic 2 coverage handling narrow to avoid broad unsupported/data-gap capture.
    if plan_name == "Classic 2" and lowered.strip() in {
        "classic 2 coverage",
        "classic2 coverage",
        "classic-2 coverage",
        "classic 02 coverage",
        "hn_classic_2 coverage",
        "hn classic 2 coverage",
    }:
        return "plan_core"
    # Comparison intent
    if _extract_comparison_plans(lowered):
        return "plan_comparison"
    # If two supported plans are mentioned with explicit comparison phrasing, treat as comparison.
    all_plans = _extract_all_plan_names(lowered)
    if _has_comparison_alias(lowered) and all_plans:
        return "plan_comparison"
    # Allow comparison intent when phrasing is explicit but one side is unsupported.
    if _has_comparison_alias(lowered) and ("remedy" in lowered or "classic" in lowered):
        return "plan_comparison"
    if _is_network_lookup_query(lowered) and not plan_name:
        return "network_lookup"
    # Provider membership check: must run BEFORE PLAN_CORE_FIELDS loop because "network" is in PLAN_CORE_FIELDS.
    # Detect "Is X in [plan] network?" and Arabic/shorthand equivalents.
    if plan_name and _is_provider_membership_query(lowered):
        return "plan_network_provider"
    # Plan core
    for field in PLAN_CORE_FIELDS:
        if field in lowered:
            return "plan_core"
    # Reimbursement
    for field in REIMBURSEMENT_FIELDS:
        if field in lowered:
            return "reimbursement_rules"
    # Summary
    for pat in SUMMARY_PATTERNS:
        if pat in lowered:
            return "plan_summary"
    # New: plan+city+type intent
    # e.g. "What hospitals are available in Sharjah for Remedy 6?"
    city_words = ["in ", "available in ", "located in ", "في "]
    # Add plural forms for robust detection
    type_words = [
        "hospital", "hospitals",
        "clinic", "clinics",
        "pharmacy", "pharmacies",
        "medical center", "medical centers",
        "laboratory", "laboratories",
        "lab", "labs",
        "diagnostic center", "diagnostic centers"
    ]
    type_words_arabic = [
        "مستشفى", "مستشفيات",
        "عيادة", "عيادات",
        "صيدلية", "صيدليات",
        "مركز طبي", "مراكز طبية",
        "مختبر", "مختبرات",
        "تحليل", "تحاليل",
    ]
    # Standard pattern
    if (
        any(t in lowered for t in type_words)
        or any(t in lowered for t in type_words_arabic)
    ) and any(c in lowered for c in city_words) and plan_name:
        return "plan_network_city_type"
    # If plan and city cues are present with a generic providers ask, route for safe clarification.
    if plan_name and any(c in lowered for c in city_words) and any(p in lowered for p in ["provider", "providers", "مزود", "مزودين", "مزوّد"]):
        return "plan_network_city_type"
    # Alias patterns for existing supported queries (no output/logic change)
    # e.g. "Dubai providers Remedy 6", "Providers in Dubai Remedy 6", "Remedy 6 Dubai providers", etc.
    city_aliases = ["dubai", "abu dhabi", "sharjah"]
    plan_aliases = ["remedy 6", "remedy 06"]
    provider_aliases = ["providers", "labs", "diagnostic centers", "diagnostic", "lab"]
    for city in city_aliases:
        for plan in plan_aliases:
            for prov in provider_aliases:
                # "Dubai providers Remedy 6"
                if city in lowered and prov in lowered and plan in lowered:
                    return "plan_network_city_type"
                # "Providers in Dubai Remedy 6"
                if prov in lowered and city in lowered and plan in lowered:
                    return "plan_network_city_type"
                # "Remedy 6 Dubai providers"
                if plan in lowered and city in lowered and prov in lowered:
                    return "plan_network_city_type"
    if _is_network_lookup_query(lowered):
        return "network_lookup"
    return None

def run_agent_wrapper(user_query: str) -> Dict[str, Any]:
    plan_name = _extract_plan_name(user_query)
    intent = _intent_from_query(user_query)
    is_arabic = any(c in user_query for c in '\u0627\u0623\u0625\u0622\u0628\u062a\u062b\u062c\u062d\u062e\u062d\u0632\u0631\u0632\u0633\u0634\u0635\u0636\u0637\u0638\u0639\u063a\u0641\u0642\u0643\u0644\u0645\u0646\u0647\u0648\u064a\u0621\u0649\u0629')

    if intent == "recommendation_style_comparison":
        msg = (
            "Recommendation-style plan selection is not supported in the deterministic assistant. "
            "Please use factual comparison phrasing like 'Compare X and Y'."
            if not is_arabic
            else "اختيار الخطة بصيغة التوصية غير مدعوم في المساعد الحتمي. يرجى استخدام صيغة مقارنة factual مثل: قارن بين X و Y."
        )
        return {
            "ok": False,
            "intent": "unsupported",
            "plan_name": None,
            "tool_name": None,
            "data": None,
            "message": msg,
            "normalized": {
                "status": "not_found",
                "tool": None,
                "answer": None,
                "errors": [msg]
            }
        }

    # New: plan_network_city_type intent
    if intent == "plan_network_city_type":
        from src.query.network_lookup import get_network_lookup
        from src.query.plan_network_lookup import resolve_plan_network

        city, provider_type = _extract_city_and_provider_type(user_query)
        if not city:
            msg = "City is unknown, unclear, or unsupported. Please specify one of: Dubai, Abu Dhabi, Sharjah, Ajman."
            return {
                "ok": False,
                "intent": intent,
                "plan_name": plan_name,
                "tool_name": None,
                "data": None,
                "message": msg,
                "normalized": {
                    "status": "not_found",
                    "tool": None,
                    "answer": None,
                    "errors": [msg],
                },
            }

        if not provider_type:
            msg = "Provider type is unclear or unsupported. Supported types: hospital, clinic, pharmacy, lab."
            return {
                "ok": False,
                "intent": intent,
                "plan_name": plan_name,
                "tool_name": None,
                "data": None,
                "message": msg,
                "normalized": {
                    "status": "not_found",
                    "tool": None,
                    "answer": None,
                    "errors": [msg],
                },
            }

        mapping = resolve_plan_network(plan_name or "")
        if not mapping.get("found"):
            msg = "Plan network mapping not available."
            return {
                "ok": False,
                "intent": intent,
                "plan_name": plan_name,
                "tool_name": None,
                "data": None,
                "message": msg,
                "normalized": {
                    "status": "not_found",
                    "tool": None,
                    "answer": None,
                    "errors": [msg],
                },
            }

        network_code = mapping["medical_network"]
        lookup = get_network_lookup()
        listing = lookup.list_providers_in_network(network_code=network_code, city=city, provider_type=provider_type, limit=25)

        if not listing.get("ok"):
            if listing.get("error") == "unknown_city":
                msg = "City is unknown, unclear, or unsupported. Please specify one of: Dubai, Abu Dhabi, Sharjah, Ajman."
            elif listing.get("error") == "unsupported_provider_type":
                msg = "Provider type is unclear or unsupported. Supported types: hospital, clinic, pharmacy, lab."
            else:
                msg = "Provider listing is not available for the resolved network."
            return {
                "ok": False,
                "intent": intent,
                "plan_name": plan_name,
                "tool_name": None,
                "data": None,
                "message": msg,
                "normalized": {
                    "status": "not_found",
                    "tool": None,
                    "answer": None,
                    "errors": [msg],
                },
            }

        display_network = NETWORK_LABELS.get(network_code, network_code.replace("_", " ").title())
        count = listing["count"]
        lines = [
            "[PROVIDER LIST]",
            f"Plan: {plan_name}",
            f"Resolved Network: {network_code} ({display_network})",
            f"City: {city}",
            f"Provider Type: {provider_type}",
            f"Count: {count}",
        ]

        if count == 0:
            lines.append("No matching providers found for this plan/network/city/provider type.")
        else:
            lines.append("Providers:")
            for name in listing["providers"]:
                lines.append(f"- {name}")
            if listing.get("truncated"):
                lines.append("Showing first 25 providers only.")

        result = "\n".join(lines)
        return {
            "ok": True,
            "intent": intent,
            "plan_name": plan_name,
            "tool_name": "list_basic_plus_providers",
            "data": None,
            "message": result,
            "normalized": {
                "status": "ok",
                "tool": "list_basic_plus_providers",
                "answer": result,
                "errors": [],
            },
        }
    if intent == "plan_network_provider":
        # Use plan_name already normalized by _extract_plan_name (e.g. "Remedy 06", not "Remedy 6").
        # Extract provider from raw query via deterministic patterns; then call resolve_plan_network + provider_in_network.
        provider = _extract_provider_from_membership_query(user_query)
        is_arabic = bool(_re.search(r"[\u0600-\u06FF]", user_query))
        if not provider:
            msg = "Could not determine provider name from query." if not is_arabic else "تعذّر استخراج اسم المزود من الاستعلام."
            return {
                "ok": False,
                "intent": "plan_network_provider",
                "plan_name": plan_name,
                "tool_name": None,
                "data": None,
                "message": msg,
                "normalized": {"status": "not_found", "tool": None, "answer": None, "errors": [msg]},
            }
        from src.query.plan_network_lookup import resolve_plan_network
        plan_info = resolve_plan_network(plan_name)
        if not plan_info.get("found"):
            msg = "Plan network mapping not available."
            return {
                "ok": False,
                "intent": "plan_network_provider",
                "plan_name": plan_name,
                "tool_name": None,
                "data": None,
                "message": msg,
                "normalized": {"status": "not_found", "tool": None, "answer": None, "errors": [msg]},
            }
        net_code = plan_info["medical_network"]
        from src.query.network_lookup import get_network_lookup
        lookup = get_network_lookup()
        details = lookup.provider_in_network(provider, net_code)
        if details.get("ambiguous"):
            msg = "Ambiguous provider match. Please specify the full provider name." if not is_arabic else "مزود غير محدد (غامض). يرجى تحديد الاسم الكامل للمزود."
            return {
                "ok": False,
                "intent": "plan_network_provider",
                "plan_name": plan_name,
                "tool_name": "provider_membership_lookup",
                "data": None,
                "message": msg,
                "normalized": {"status": "not_found", "tool": "provider_membership_lookup", "answer": None, "errors": [msg]},
            }
        if not details.get("found"):
            msg = "Provider not found." if not is_arabic else "المزود غير موجود."
            return {
                "ok": False,
                "intent": "plan_network_provider",
                "plan_name": plan_name,
                "tool_name": "provider_membership_lookup",
                "data": None,
                "message": msg,
                "normalized": {"status": "not_found", "tool": "provider_membership_lookup", "answer": None, "errors": [msg]},
            }
        in_net = details.get("in_network", False)
        prov_name = (details.get("provider_name") or provider).upper()
        canonical_plan = plan_info["plan_name"]
        if is_arabic:
            status_str = "داخل الشبكة" if in_net else "خارج الشبكة"
            res_msg = (
                f"[الشبكة]\nالمزود: {prov_name}\nالخطة: {canonical_plan}\n"
                f"الشبكة المطلوبة: {net_code}\nالحالة: {status_str}"
            )
        else:
            status_str = "In network" if in_net else "Out of network"
            res_msg = (
                f"[NETWORK]\nProvider: {prov_name}\nPlan: {canonical_plan}\n"
                f"Required Network: {net_code}\nStatus: {status_str}"
            )
        return {
            "ok": True,
            "intent": "plan_network_provider",
            "plan_name": plan_name,
            "tool_name": "provider_membership_lookup",
            "data": None,
            "message": res_msg,
            "normalized": {
                "status": "ok",
                "tool": "provider_membership_lookup",
                "answer": res_msg,
                "errors": [],
            },
        }
    if intent == "network_lookup":
        from src.query.network_lookup import get_network_lookup
        lookup = get_network_lookup()
        network_result = lookup.answer_query(user_query)
        lowered_result = str(network_result).lower()
        not_found = (
            "provider not found" in lowered_result
            or "المزود غير موجود" in str(network_result)
            or "no:" in lowered_result
            or "ambiguous provider" in lowered_result
            or "مزود غير محدد" in str(network_result)
        )
        status = "not_found" if not_found else "ok"
        return {
            "ok": not not_found,
            "intent": "network_lookup",
            "plan_name": None,
            "tool_name": "network_lookup",
            "data": None,
            "message": network_result,
            "normalized": {
                "status": status,
                "tool": "network_lookup",
                "answer": network_result if not not_found else None,
                "errors": [] if not not_found else [network_result],
            }
        }
    is_arabic = any(c in user_query for c in 'اأإآبتثجحخدذرزسشصضطظعغفقكلمنهويءىة')
    # Patch: Robust summary routing for mixed Arabic/English phrasing
    # If summary pattern is present and plan_name is present, force plan_summary intent
    if not intent and plan_name:
        for pat in SUMMARY_PATTERNS:
            if pat in user_query.lower():
                intent = "plan_summary"
                break
    # Comparison intent
    if intent == "plan_comparison":
        plans = _extract_comparison_plans(user_query)
        # Fallback: if not found, try all plan names in query
        if not plans:
            all_plans = _extract_all_plan_names(user_query)
            if len(all_plans) == 2:
                plans = (all_plans[0], all_plans[1])
        if not plans:
            msg = "Comparison is not supported or not available for one or both plans. Please specify two supported plans to compare." if not is_arabic else "يرجى تحديد خطتين مدعومتين للمقارنة."
            return {
                "ok": False,
                "intent": "plan_comparison",
                "plan_name": None,
                "tool_name": None,
                "data": None,
                "message": msg,
                "normalized": {
                    "status": "not_found",
                    "tool": None,
                    "answer": None,
                    "errors": [msg]
                }
            }
        plan1, plan2 = plans
        def _comparison_not_available():
            msg = (
                "Sorry, comparison is not supported or not available for one or both plans."
                if not is_arabic else
                "ط¹ط°ط±ط§ظ‹طŒ ط§ظ„ظ…ظ‚ط§ط±ظ†ط© ط؛ظٹط± ظ…ط¯ط¹ظˆظ…ط© ط£ظˆ ط؛ظٹط± ظ…طھط§ط­ط© ظ„ط®ط·ط© ط£ظˆ ط£ظƒط«ط±."
            )
            return {
                "ok": False,
                "intent": "plan_comparison",
                "plan_name": f"{plan1} vs {plan2}",
                "tool_name": None,
                "data": None,
                "message": msg,
                "normalized": {
                    "status": "not_found",
                    "tool": None,
                    "answer": None,
                    "errors": [msg]
                }
            }
        try:
            from src.tools.enhanced_plan_loader import is_enhanced_plan
            from src.query.plan_query import load_plan
            from src.validation.plan_validator import normalize_plan, validate_plan_ready
            allow_enhanced_pair = {plan1, plan2} == {"Classic 2", "Classic 3"}
            if (is_enhanced_plan(plan1) or is_enhanced_plan(plan2)) and not allow_enhanced_pair:
                return _comparison_not_available()
            for candidate in (plan1, plan2):
                norm_candidate = normalize_plan(load_plan(candidate))
                ok_candidate, _ = validate_plan_ready(norm_candidate)
                if not ok_candidate:
                    return _comparison_not_available()
        except Exception:
            return _comparison_not_available()
        try:
            from src.query.plan_query import compare_plans
            cmp = compare_plans(plan1, plan2)
        except Exception as ex:
            # Block unsupported/unknown plans and return safe message
            msg = (
                "Sorry, comparison is not supported or not available for one or both plans."
                if not is_arabic else
                "عذراً، المقارنة غير مدعومة أو غير متاحة لخطة أو أكثر."
            )
            return {
                "ok": False,
                "intent": "plan_comparison",
                "plan_name": f"{plan1} vs {plan2}",
                "tool_name": None,
                "data": None,
                "message": msg,
                "normalized": {
                    "status": "not_found",
                    "tool": None,
                    "answer": None,
                    "errors": [msg]
                }
            }
        # Only show key fields (no internal fields)
        key_fields = [
            ("annual_limit", "Annual Limit", "الحد السنوي"),
            ("pharmacy_cover_summary", "Pharmacy", "الصيدلة"),
            ("diagnostics_cover_summary", "Diagnostics", "التشخيص"),
            ("physiotherapy_cover_summary", "Physiotherapy", "العلاج الطبيعي"),
            ("direct_billing", "Direct Billing", "الدفع المباشر"),
            ("reimbursement_allowed", "Reimbursement Allowed", "التعويض"),
            ("referral_required", "Referral Required", "الإحالة"),
            ("area_of_coverage", "Area of Coverage", "نطاق التغطية"),
            ("network_name", "Network", "الشبكة"),
        ]
        lines = []
        if is_arabic:
            lines.append(f"مقارنة بين {plan1} و {plan2}:")
        else:
            lines.append(f"Comparison between {plan1} and {plan2}:")
        for field, label_en, label_ar in key_fields:
            v1 = cmp['differing'].get(field, {}).get('plan_a') if field in cmp['differing'] else None
            v2 = cmp['differing'].get(field, {}).get('plan_b') if field in cmp['differing'] else None
            if v1 is None and v2 is None:
                v1 = v2 = None
                for m in cmp['matched']:
                    if m['field'] == field:
                        v1 = v2 = m['value']
                        break
            if is_arabic:
                label = label_ar
            else:
                label = label_en
            if v1 is not None or v2 is not None:
                lines.append(f"{label}: {plan1}: {v1 if v1 is not None else '-'} | {plan2}: {v2 if v2 is not None else '-'}")
        # Old similarity/difference logic for fallback
        def score(plan):
            score = 0
            for field in ["pharmacy_cover_summary", "diagnostics_cover_summary", "physiotherapy_cover_summary"]:
                val = cmp['differing'].get(field, {}).get('plan_a' if plan == plan1 else 'plan_b')
                if val and isinstance(val, str) and ("unlimited" in val.lower() or "covered" in val.lower() or "yes" in val.lower()):
                    score += 2
                elif val:
                    score += 1
            direct = cmp['differing'].get("referral_required", {}).get('plan_a' if plan == plan1 else 'plan_b')
            if direct is False:
                score += 2
            return score
        s1 = score(plan1)
        s2 = score(plan2)
        if s1 == s2:
            diffs = []
            for field, label_en, _ in key_fields:
                v1 = cmp['differing'].get(field, {}).get('plan_a')
                v2 = cmp['differing'].get(field, {}).get('plan_b')
                if v1 != v2 and v1 is not None and v2 is not None:
                    diffs.append(f"{label_en}: {plan1}={v1}, {plan2}={v2}")
            if diffs:
                lines.append("")
                lines.append(f"Both plans are similar overall, but differ in: {', '.join(diffs)}.")
            else:
                lines.append("")
                lines.append("Both plans are very similar in their key benefits.")
        # Filter out internal fields from message (no approval_status, tests_passed, source_trace, raw dicts)
        msg = "\n".join(lines)
        forbidden = ["approval_status", "tests_passed", "source_trace", "status", "tool", "answer", "errors", "{", "}"]
        for key in forbidden:
            if key in msg:
                msg = msg.replace(key, "")
        return {
            "ok": True,
            "intent": "plan_comparison",
            "plan_name": f"{plan1} vs {plan2}",
            "tool_name": "compare_plans",
            "data": None,  # Do not expose raw cmp
            "message": msg,
            "normalized": {
                "status": "ok",
                "tool": "compare_plans",
                "answer": None,
                "errors": []
            }
        }
    # If no supported plan or no supported intent, always return unsupported-query message
    if not plan_name or intent not in ("plan_core", "reimbursement_rules", "plan_summary"):
        msg = (
            "Sorry, this query is not supported or not available. Please specify a supported plan or question."
            if not is_arabic else
            "عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم."
        )
        resp = {
            "ok": False,
            "intent": "unsupported",
            "plan_name": plan_name,
            "tool_name": None,
            "data": None,
            "message": msg,
            "normalized": {
                "status": "not_found",
                "tool": None,
                "answer": None,
                "errors": [msg]
            }
        }
        return resp
    from src.validation.plan_validator import normalize_plan, validate_plan_ready
    import re
    def _strip_internal_metadata(d):
        if isinstance(d, dict):
            d = dict(d)
            d.pop("approval_status", None)
            d.pop("tests_passed", None)
            d.pop("source_trace", None)
        return d
    if intent in ("plan_core", "reimbursement_rules", "plan_summary"):
        try:
            # Classic 2: use authoritative enhanced loader for readiness and data
            if plan_name == "Classic 2":
                from src.tools.internal_loader_hn_classic_2 import load_internal_hn_classic_2
                full_plan = load_internal_hn_classic_2()
            else:
                from src.query.plan_query import load_plan
                full_plan = load_plan(plan_name)
            norm_plan = normalize_plan(full_plan)
            ok, reason = validate_plan_ready(norm_plan)
            if not ok:
                msg = (
                    "هذه الخطة غير متاحة حالياً للإجابة على العملاء."
                    if is_arabic else
                    "Sorry, this plan is not available for customer-facing answers."
                )
                resp = {
                    "ok": False,
                    "intent": intent,
                    "plan_name": plan_name,
                    "tool_name": f"get_{intent}",
                    "data": None,
                    "message": msg
                }
                resp["normalized"] = {
                    "status": "not_ready",
                    "tool": f"get_{intent}",
                    "answer": None,
                    "errors": [reason]
                }
                return resp
            # If ready, return tool output as before
            if intent == "plan_core":
                data = get_plan_core(plan_name)
                plan = normalize_plan(data)
                plan = _strip_internal_metadata(plan)
                # Special-case: if query is for maternity limit and plan is Remedy 02, extract AED value from maternity_cover
                if "maternity limit" in user_query.lower() and plan_name == "Remedy 02":
                    maternity_cover = plan.get("maternity_cover")
                    aed_match = None
                    if maternity_cover:
                        m = re.search(r"AED[ .]*([0-9,]+)", maternity_cover)
                        if m:
                            aed_match = f"AED {m.group(1)}"
                    msg = f"Maternity limit: {aed_match if aed_match else 'Not available'}"
                    resp = {
                        "ok": True,
                        "intent": intent,
                        "plan_name": plan_name,
                        "tool_name": "get_plan_core",
                        "data": plan,
                        "message": msg
                    }
                    resp["normalized"] = {
                        "status": "ok",
                        "tool": "get_plan_core",
                        "answer": plan,
                        "errors": []
                    }
                    return resp
                # Default plan_core output
                lines = []
                lines.append(f"Plan: {plan.get('plan_name')}")
                lines.append(f"Code: {plan.get('plan_code')}")
                lines.append(f"الشبكة: {plan.get('network_name')}")
                lines.append(f"Annual limit: {plan.get('annual_limit')}")
                lines.append(f"Area: {plan.get('area_of_coverage')}")
                lines.append(f"Direct billing: {'Yes' if plan.get('direct_billing') else 'No' if plan.get('direct_billing') is not None else 'Not available'}")
                lines.append(f"Referral required: {'Yes' if plan.get('referral_required') else 'No' if plan.get('referral_required') is not None else 'Not available'}")
                msg = "\n".join(lines)
                resp = {
                    "ok": True,
                    "intent": intent,
                    "plan_name": plan_name,
                    "tool_name": "get_plan_core",
                    "data": plan,
                    "message": msg
                }
                resp["normalized"] = {
                    "status": "ok",
                    "tool": "get_plan_core",
                    "answer": plan,
                    "errors": []
                }
                return resp
            elif intent == "reimbursement_rules":
                data = get_reimbursement_rules(plan_name)
                plan = normalize_plan(data)
                plan = _strip_internal_metadata(plan)
                lines = []
                lines.append(f"Reimbursement allowed: {'Yes' if plan.get('reimbursement_allowed') else 'No' if plan.get('reimbursement_allowed') is not None else 'Not available' }.")
                if plan.get('reimbursement_scope'):
                    lines.append(f"Scope: {plan['reimbursement_scope']}.")
                if plan.get('outside_network_reimbursement'):
                    lines.append(f"Outside network reimbursement: {plan['outside_network_reimbursement']}.")
                if plan.get('outside_uae_reimbursement'):
                    lines.append(f"Outside UAE reimbursement: {plan['outside_uae_reimbursement']}.")
                if plan.get('reimbursement_basis'):
                    lines.append(f"Basis: {plan['reimbursement_basis']}.")
                if plan.get('reimbursement_conditions'):
                    lines.append(f"Conditions: {plan['reimbursement_conditions']}.")
                if plan.get('reimbursement_documents_required'):
                    lines.append(f"Documents required: {plan['reimbursement_documents_required']}.")
                msg = "\n".join(lines)
                resp = {
                    "ok": True,
                    "intent": intent,
                    "plan_name": plan_name,
                    "tool_name": "get_reimbursement_rules",
                    "data": plan,
                    "message": msg
                }
                resp["normalized"] = {
                    "status": "ok",
                    "tool": "get_reimbursement_rules",
                    "answer": plan,
                    "errors": []
                }
                return resp
            elif intent == "plan_summary":
                data = get_plan_summary(plan_name)
                # Do not validate summary output, just return if plan is ready
                data = _strip_internal_metadata(data)
                summary_text = data.get("summary_text")
                if summary_text and isinstance(summary_text, str) and summary_text.strip() and summary_text.strip().lower() not in ["none", "not available", "plan summary returned."]:
                    msg = summary_text.strip()
                else:
                    lines = []
                    lines.append(f"Plan: {data.get('plan_name')}")
                    lines.append(f"Code: {data.get('plan_code')}")
                    msg = "\n".join(lines)
                resp = {
                    "ok": True,
                    "intent": intent,
                    "plan_name": plan_name,
                    "tool_name": "get_plan_summary",
                    "data": data,
                    "message": msg
                }
                resp["normalized"] = {
                    "status": "ok",
                    "tool": "get_plan_summary",
                    "answer": data,
                    "errors": []
                }
                return resp
        except Exception as e:
            msg = f"حدث خطأ: {e}" if is_arabic else f"Error: {e}"
            resp = {
                "ok": False,
                "intent": intent,
                "plan_name": plan_name,
                "tool_name": f"get_{intent}",
                "data": None,
                "message": msg
            }
            resp["normalized"] = {
                "status": "error",
                "tool": f"get_{intent}",
                "answer": None,
                "errors": [msg]
            }
            return resp
