#!/usr/bin/env python
"""
Controlled Operator Usage Pack: Run 50+ realistic queries and categorize results.
Purpose: Measure operational usability without feature expansion.
"""
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.agent_wrapper import run_agent_wrapper

# Query pack: diverse realistic scenarios
QUERY_PACK = [
    # === PROVIDER LISTING QUERIES (10) ===
    ("hospitals in Remedy 5 in Dubai", "provider_listing"),
    ("clinics in Remedy 6 in Sharjah", "provider_listing"),
    ("pharmacies in Remedy 5 in Dubai", "provider_listing"),
    ("labs in Remedy 6 in Abu Dhabi", "provider_listing"),
    ("hospitals in Remedy 3 in Ajman", "provider_listing"),
    ("diagnostic centers in Remedy 2 in Dubai", "provider_listing"),
    ("medical centers in Remedy 4 in Sharjah", "provider_listing"),
    ("What hospitals are in Remedy 05?", "provider_listing"),
    ("Show me pharmacies in Dubai for Remedy 6", "provider_listing"),
    ("Is ASTER HOSPITAL in Remedy 5 network?", "provider_lookup"),
    
    # === PROVIDER LOOKUP QUERIES (10) ===
    ("Is Accuracy Plus Medical Laboratory in Remedy 05 network?", "provider_lookup"),
    ("provider MEDEOR 24X7 HOSPITAL in Remedy 6", "provider_lookup"),
    ("NMC ROYAL HOSPITAL DXB - Remedy 5 - network?", "provider_lookup"),
    ("Is DUBAI MEDICAL UNIVERSITY HOSPITAL covered?", "provider_lookup"),
    ("AL BORG diagnostic in Remedy 3?", "provider_lookup"),
    ("Covered in Remedy 06: QUALITY DIAGNOSTIC LABORATORY", "provider_lookup"),
    ("Is HATTA HOSPITAL in plan?", "provider_lookup"),
    ("CEDARS JEBEL ALI in Remedy 5?", "provider_lookup"),
    ("Provider 24HOUR PHARMACY in Remedy 6 network?", "provider_lookup"),
    ("MEDSTAR HEALTHCARE - covered Remedy 05?", "provider_lookup"),
    
    # === ARABIC QUERIES (10) ===
    ("مستشفيات Remedy 5 في دبي؟", "arabic_provider_listing"),
    ("عيادات Remedy 6 في الشارقة؟", "arabic_provider_listing"),
    ("صيدليات في دبي Remedy 5", "arabic_provider_listing"),
    ("هل ASTER HOSPITAL في شبكة Remedy 05؟", "arabic_provider_lookup"),
    ("AL BORG في Remedy 6؟", "arabic_provider_lookup"),
    ("تحاليل في ابو ظبي Remedy 6", "arabic_provider_listing"),
    ("مختبرات طبية Remedy 5 في دبي", "arabic_provider_listing"),
    ("هل مستشفى CEDARS في Remedy 5؟", "arabic_provider_lookup"),
    ("عيادات طبية في الشارقة Remedy 6", "arabic_provider_listing"),
    ("صيدليات في الشارقة Remedy 05؟", "arabic_provider_listing"),
    
    # === MIXED-LANGUAGE QUERIES (5) ===
    ("hospitals في Dubai Remedy 5", "mixed_language"),
    ("pharmacies في الشارقة Remedy 6", "mixed_language"),
    ("تحاليل diagnostic في Abu Dhabi Remedy 6", "mixed_language"),
    ("عيادات clinics في Dubai Remedy 5", "mixed_language"),
    ("ACCURACY PLUS في شبكة Remedy 05؟", "mixed_language"),
    
    # === SHORTHAND / INFORMAL PHRASING (5) ===
    ("R5 hospitals Dubai", "shorthand"),
    ("Remedy 06 pharmacies Sharjah", "shorthand"),
    ("Remedy 5 - any hospitals in Dubai?", "shorthand"),
    ("Show clinics - Remedy 6 - Sharjah", "shorthand"),
    ("Labs Remedy 6 Abu Dhabi?", "shorthand"),
    
    # === AMBIGUOUS / CHALLENGING (5) ===
    ("hospitals in Remedy", "ambiguous"),
    ("providers in Dubai", "ambiguous"),
    ("Are there hospitals?", "ambiguous"),
    ("What's the network?", "ambiguous"),
    ("Pharmacies available?", "ambiguous"),
    
    # === UNSUPPORTED REQUESTS (5) ===
    ("optical stores in Remedy 5 Dubai", "unsupported"),
    ("dental clinics Remedy 6 Sharjah", "unsupported"),
    ("mental health clinics Remedy 5", "unsupported"),
    ("Compare Remedy 5 and Remedy 6 hospitals", "unsupported"),
    ("Cheapest pharmacy Remedy 5", "unsupported"),
    
    # === EDGE CASES / UNKNOWN CITIES (5) ===
    ("hospitals in Remedy 5 in Atlantis", "unknown_city"),
    ("pharmacies in Remedy 6 in Fujairah", "unknown_city"),
    ("clinics in Remedy 5 in Ras Al Khaimah", "unknown_city"),
    ("labs in Remedy 6 in Umm Al Quwain", "unknown_city"),
    ("hospitals in Remedy 5 in Unknown City", "unknown_city"),
]

def categorize_result(query: str, result: dict, query_type: str) -> dict:
    """Categorize a result as GOOD, REVIEW, BLOCKED_OK, GAP, or CRITICAL."""
    ok = result.get("ok", False)
    message = result.get("message", "")
    intent = result.get("intent", "")
    
    # === CRITICAL (hallucination, wrong data, pricing, unsafe) ===
    if "hallucin" in message.lower() or "recommend" in message.lower():
        if query_type not in ["unsupported"]:
            return {"category": "CRITICAL", "reason": "Hallucination or improper recommendation"}
    
    if "AED" in message and query_type in ["provider_listing", "provider_lookup"]:
        if "price" not in query.lower():
            return {"category": "CRITICAL", "reason": "Unexpected pricing information leaked"}
    
    # === BLOCKED_OK (correctly rejected unsupported/ambiguous) ===
    if not ok and query_type in ["unsupported", "ambiguous", "unknown_city"]:
        if "not supported" in message.lower() or "unclear" in message.lower() or "ambiguous" in message.lower():
            return {"category": "BLOCKED_OK", "reason": f"Safe block: {message[:80]}"}
    
    # === GOOD (correct, operationally usable) ===
    if ok and intent == "plan_network_city_type":
        if "[PROVIDER LIST]" in message:
            if "Plan:" in message and "Count:" in message:
                return {"category": "GOOD", "reason": "Structured provider listing"}
    
    if ok and intent == "plan_network_provider":
        if "[NETWORK]" in message or "Status:" in message:
            return {"category": "GOOD", "reason": "Structured provider lookup"}
    
    if ok and intent == "plan_core":
        if "Plan:" in message or "Network:" in message:
            return {"category": "GOOD", "reason": "Structured plan core response"}
    
    # === REVIEW (safe but awkward, incomplete, confusing) ===
    if ok and query_type in ["shorthand", "mixed_language"]:
        if intent == "plan_network_city_type" and "[PROVIDER LIST]" in message:
            return {"category": "REVIEW", "reason": "Phrasing friction: informal/mixed-language OK but sluggish extraction"}
    
    if ok and message and len(message) > 500 and "Providers:" in message:
        if "Showing first" not in message:
            return {"category": "REVIEW", "reason": "Large provider list without truncation notice"}
    
    if ok and intent == "unsupported":
        return {"category": "REVIEW", "reason": "Safe but could be clearer intent"}
    
    # === GAP (should work but failed) ===
    if not ok and query_type in ["provider_listing", "provider_lookup", "arabic_provider_listing"]:
        if intent == "plan_network_city_type" or intent == "plan_network_provider":
            return {"category": "GAP", "reason": f"Failed lookup: {message[:80]}"}
    
    if not ok and query_type == "provider_listing":
        return {"category": "GAP", "reason": f"Provider listing failed: {message[:80]}"}
    
    # Default fallback
    if ok:
        return {"category": "REVIEW", "reason": "Unexpected result shape; check message"}
    else:
        return {"category": "GAP", "reason": f"Unexpected failure: {message[:80]}"}

def run_pack():
    """Execute the query pack and produce categorized results."""
    results = []
    
    for i, (query, query_type) in enumerate(QUERY_PACK, 1):
        query_preview = query[:60] if len(query) <= 60 else query[:57] + "..."
        print(f"[{i:2d}/{len(QUERY_PACK)}] {query_type:20s} | {query_preview:<60s}", end="", flush=True)
        try:
            result = run_agent_wrapper(query)
            categorized = categorize_result(query, result, query_type)
            category = categorized["category"]
            reason = categorized["reason"]
            
            results.append({
                "seq": i,
                "query": query,
                "query_type": query_type,
                "ok": result.get("ok"),
                "intent": result.get("intent"),
                "category": category,
                "reason": reason,
                "message_preview": (result.get("message", "") or "")[:100].replace("\n", " | "),
            })
            
            print(f" -> {category}")
        except Exception as e:
            print(f" -> ERROR: {str(e)[:50]}")
            results.append({
                "seq": i,
                "query": query,
                "query_type": query_type,
                "ok": False,
                "intent": "ERROR",
                "category": "CRITICAL",
                "reason": f"Exception: {str(e)[:80]}",
                "message_preview": str(e)[:100],
            })
    
    return results

def summarize_results(results: list) -> dict:
    """Produce summary statistics."""
    categories = {}
    for r in results:
        cat = r["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    total = len(results)
    return {
        "total_queries": total,
        "counts": categories,
        "percentages": {k: round(100 * v / total, 1) for k, v in categories.items()},
        "criticals": [r for r in results if r["category"] == "CRITICAL"],
        "gaps": [r for r in results if r["category"] == "GAP"],
        "reviews": [r for r in results if r["category"] == "REVIEW"],
    }

def main():
    print(f"\n{'='*80}")
    print(f"OPERATOR USAGE PACK: {len(QUERY_PACK)} queries")
    print(f"{'='*80}\n")
    
    results = run_pack()
    summary = summarize_results(results)
    
    # Write detailed results
    output_path = Path("docs/operational_usage/operator_usage_pack_50_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Total queries: {summary['total_queries']}")
    print(f"GOOD:        {summary['counts'].get('GOOD', 0):3d} ({summary['percentages'].get('GOOD', 0):5.1f}%)")
    print(f"REVIEW:      {summary['counts'].get('REVIEW', 0):3d} ({summary['percentages'].get('REVIEW', 0):5.1f}%)")
    print(f"BLOCKED_OK:  {summary['counts'].get('BLOCKED_OK', 0):3d} ({summary['percentages'].get('BLOCKED_OK', 0):5.1f}%)")
    print(f"GAP:         {summary['counts'].get('GAP', 0):3d} ({summary['percentages'].get('GAP', 0):5.1f}%)")
    print(f"CRITICAL:    {summary['counts'].get('CRITICAL', 0):3d} ({summary['percentages'].get('CRITICAL', 0):5.1f}%)")
    
    if summary["criticals"]:
        print(f"\n{'CRITICAL ISSUES FOUND'}")
        print(f"{'-'*80}")
        for r in summary["criticals"]:
            print(f"Query: {r['query']}")
            print(f"Reason: {r['reason']}")
            print(f"Preview: {r['message_preview']}\n")
    
    if summary["gaps"]:
        print(f"\nGAP ANALYSIS (Top 5)")
        print(f"{'-'*80}")
        for r in summary["gaps"][:5]:
            print(f"Query: {r['query']}")
            print(f"Intent: {r['intent']}")
            print(f"Reason: {r['reason']}\n")
    
    print(f"\nDetailed results: {output_path}")
    
    return 0 if not summary["criticals"] else 1

if __name__ == "__main__":
    sys.exit(main())
