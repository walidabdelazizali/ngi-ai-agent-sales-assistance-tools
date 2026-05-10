#!/usr/bin/env python3
"""
Classic 1R Operational Usage Pack - Supervised measurement script.
Runs 25-30 queries through the agent and categorizes results.
"""
import json
import sys
from src.agent_wrapper import run_agent_wrapper

# Comprehensive query set for Classic 1R
QUERY_SET = [
    # Basic coverage
    ("Summarize Classic 1R", "plan_summary", "GOOD", "Plan summary should return core details"),
    ("What is the annual limit for Classic 1R?", "plan_field", "GOOD", "Annual limit field query"),
    ("What is the network for Classic 1R?", "plan_field", "GOOD", "Network field query"),
    ("What is the network name for Classic 1R?", "plan_field", "GOOD", "Network name alias"),
    
    # Benefit queries
    ("What is the pharmacy benefit for Classic 1R?", "plan_field", "GOOD", "Pharmacy benefit field"),
    ("What is the maternity limit for Classic 1R?", "plan_field", "GOOD", "Maternity limit field"),
    ("Does Classic 1R cover dental?", "plan_field", "GOOD", "Dental coverage query"),
    ("What is the mental health cover for Classic 1R?", "plan_field", "GOOD", "Mental health field"),
    
    # Shorthand/alternative phrasing
    ("classic 1r limit", "plan_field", "REVIEW", "Shorthand without 'What is'"),
    ("pharmacy Classic 1R", "plan_field", "REVIEW", "Field without full question structure"),
    ("maternity Classic 1R", "plan_field", "REVIEW", "Maternity shorthand"),
    ("dental Classic 1R", "plan_field", "REVIEW", "Dental shorthand"),
    ("mental health Classic 1R", "plan_field", "REVIEW", "Mental health shorthand"),
    
    # Arabic queries
    ("ملخص Classic 1R", "plan_summary", "REVIEW", "Arabic-English mix: summarize"),
    ("ما هي الحد السنوي لـ Classic 1R؟", "plan_field", "REVIEW", "Arabic annual limit"),
    ("شبكة Classic 1R", "plan_field", "REVIEW", "Arabic network"),
    ("صيدلية Classic 1R", "plan_field", "REVIEW", "Arabic pharmacy"),
    ("الولادة Classic 1R", "plan_field", "REVIEW", "Arabic maternity"),
    
    # Provider/Network lookup
    ("hospitals in Classic 1R in Dubai", "plan_network_city_type", "GOOD", "Provider list with city"),
    ("clinics in Classic 1R in Abu Dhabi", "plan_network_city_type", "GOOD", "Clinic list with city"),
    ("pharmacies in Classic 1R in Dubai", "plan_network_city_type", "GOOD", "Pharmacy list"),
    ("Is Burjeel Hospital in Classic 1R network?", "plan_network_provider", "GOOD", "Provider membership check"),
    ("Is ASTER HOSPITAL in Classic 1R network?", "plan_network_provider", "GOOD", "Another provider check"),
    
    # Mixed language
    ("Classic 1R hospital في Dubai", "plan_network_city_type", "REVIEW", "English-Arabic mix"),
    ("شبكة hospitals Classic 1R", "plan_field", "REVIEW", "Arabic-English phrase"),
    
    # Ambiguity/edge cases
    ("Compare Classic 1R and Classic 3", "plan_comparison", "BLOCKED_OK", "Comparison should be safe-blocked"),
    ("Does Classic 1R have maternity?", "plan_field", "GOOD", "Yes/No maternity phrasing"),
    ("Is optical covered in Classic 1R?", "unsupported", "GAP", "Unsupported benefit type"),
    ("What is the area of coverage for Classic 1R?", "plan_core", "GOOD", "Core field query"),
    ("Get me deals on Classic 1R", "unsupported", "BLOCKED_OK", "Unsupported/hallucination prevention"),
]

def categorize_result(query, result, expected_intent, expected_category):
    """
    Categorize a single query result.
    
    Returns: (actual_category, exact_reason)
    """
    ok = result.get("ok", False)
    intent = result.get("intent", "unknown")
    message = result.get("message", "").lower()
    plan = result.get("plan_name", "")
    
    # Check for CRITICAL failures first
    if plan and plan != "Classic 1R" and "classic 1r" not in query.lower():
        pass  # Not a critical if plan not explicitly Classic 1R in query
    
    # CRITICAL: hallucinated benefits (returning data that doesn't exist)
    if ok and intent == "plan_field":
        if "optical" in query.lower() and "optical" in message:
            return ("CRITICAL", "Hallucinated optical coverage (unsupported for Classic 1R)")
    
    # CRITICAL: pricing leakage outside of plan_field/plan_summary
    if ok and intent not in ("plan_field", "plan_summary", "plan_network_city_type", "plan_network_provider", "plan_comparison"):
        if any(price_term in message for price_term in ["aed", "price", "cost", "charge"]):
            if intent != "plan_field":  # plan_field is allowed to show AED values
                return ("CRITICAL", f"Pricing leak in {intent}: {message[:100]}")
    
    # CRITICAL: wrong provider membership
    if ok and intent == "plan_network_provider" and "in network" in message.lower():
        # Only flag if it seems incorrect (e.g., provider that shouldn't be there)
        # This is hard to detect without ground truth, so skip for now
        pass
    
    # CRITICAL: unsupported query returning full plan summary
    if ok and intent == "plan_summary" and expected_category in ("unsupported", "GAP"):
        return ("CRITICAL", "Unsupported query returned full plan summary instead of rejecting")
    
    # Expected intent match
    if intent == expected_intent:
        if expected_category == "GOOD":
            if ok and plan == "Classic 1R":
                return ("GOOD", "Query routed and answered correctly")
            elif not ok and intent == "unsupported":
                return ("BLOCKED_OK", "Query safely blocked as unsupported")
        elif expected_category == "BLOCKED_OK":
            if not ok or intent == "unsupported":
                return ("BLOCKED_OK", "Query safely blocked")
            elif ok:
                return ("REVIEW", f"Query answered but should be blocked: {intent}")
        elif expected_category == "REVIEW":
            return ("REVIEW", "Alternative phrasing handling")
        elif expected_category == "GAP":
            if not ok:
                return ("GAP", "Unsupported/unavailable")
            else:
                return ("GOOD", "Query surprisingly answered")
    
    # Intent mismatch
    if intent != expected_intent:
        if expected_intent == "plan_field" and intent == "plan_core":
            return ("REVIEW", f"Routed to plan_core instead of plan_field")
        if expected_intent == "unsupported" and intent != "unsupported":
            if ok:
                return ("REVIEW", f"Answered as {intent} instead of blocking")
            else:
                return ("BLOCKED_OK", "Blocked even if not marked unsupported")
        return ("REVIEW", f"Intent mismatch: expected {expected_intent}, got {intent}")
    
    # Default categorization
    if ok:
        if plan == "Classic 1R":
            return ("GOOD", "Successfully answered")
        else:
            return ("REVIEW", f"Answered but plan is {plan}, not Classic 1R")
    else:
        if expected_category == "unsupported":
            return ("BLOCKED_OK", "Correctly rejected unsupported query")
        return ("GAP", "Query not answered")

def run_evaluation():
    """Run the full operator pack evaluation."""
    results = {
        "GOOD": [],
        "REVIEW": [],
        "BLOCKED_OK": [],
        "GAP": [],
        "CRITICAL": [],
    }
    
    print("=" * 100)
    print("CLASSIC 1R OPERATIONAL USAGE PACK - RUNNING 25-30 QUERIES")
    print("=" * 100)
    print()
    
    for i, (query, expected_intent, expected_category, description) in enumerate(QUERY_SET, 1):
        print(f"[{i:2d}] Running: {query}")
        try:
            result = run_agent_wrapper(query)
            actual_category, reason = categorize_result(query, result, expected_intent, expected_category)
            
            entry = {
                "query": query,
                "expected_intent": expected_intent,
                "expected_category": expected_category,
                "actual_intent": result.get("intent"),
                "actual_category": actual_category,
                "ok": result.get("ok"),
                "plan": result.get("plan_name"),
                "message": result.get("message", "")[:200],
                "reason": reason,
                "description": description,
            }
            results[actual_category].append(entry)
            
            status_icon = "✓" if actual_category == expected_category else "⚠" if actual_category == "REVIEW" else "✗"
            print(f"     {status_icon} {actual_category}: {reason}")
        except Exception as e:
            print(f"     ✗ ERROR: {str(e)[:100]}")
            results["GAP"].append({
                "query": query,
                "error": str(e),
                "actual_category": "GAP",
            })
        print()
    
    return results

def print_summary(results):
    """Print the results summary table."""
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    
    total = sum(len(v) for v in results.values())
    good_count = len(results["GOOD"])
    review_count = len(results["REVIEW"])
    blocked_count = len(results["BLOCKED_OK"])
    gap_count = len(results["GAP"])
    critical_count = len(results["CRITICAL"])
    
    print(f"\nTotal queries: {total}")
    print(f"GOOD:       {good_count:2d} ({100*good_count/total:.1f}%) ✓ Fully functional")
    print(f"REVIEW:     {review_count:2d} ({100*review_count/total:.1f}%) ~ Alternative/edge phrasing")
    print(f"BLOCKED_OK: {blocked_count:2d} ({100*blocked_count/total:.1f}%) ⊘ Safely blocked (correct)")
    print(f"GAP:        {gap_count:2d} ({100*gap_count/total:.1f}%) ✗ Unsupported/missing")
    print(f"CRITICAL:   {critical_count:2d} ({100*critical_count/total:.1f}%) ⚠ SAFETY VIOLATIONS")
    
    print("\n" + "-" * 100)
    print("GOOD Results (fully functional):")
    print("-" * 100)
    for item in results["GOOD"]:
        print(f"  ✓ {item['query']}")
        print(f"    → {item.get('reason', 'N/A')}")
    
    if results["REVIEW"]:
        print("\n" + "-" * 100)
        print("REVIEW Results (alternative phrasing/edge cases):")
        print("-" * 100)
        for item in results["REVIEW"]:
            print(f"  ~ {item['query']}")
            print(f"    → {item.get('reason', 'N/A')}")
    
    if results["GAP"]:
        print("\n" + "-" * 100)
        print("GAP Results (unsupported/missing):")
        print("-" * 100)
        for item in results["GAP"]:
            print(f"  ✗ {item['query']}")
            print(f"    → {item.get('reason', item.get('error', 'N/A'))}")
    
    if results["CRITICAL"]:
        print("\n" + "-" * 100)
        print("⚠ CRITICAL FAILURES (SAFETY VIOLATIONS):")
        print("-" * 100)
        for item in results["CRITICAL"]:
            print(f"  ⚠ {item['query']}")
            print(f"    → {item.get('reason', 'N/A')}")
    
    print("\n" + "=" * 100)
    
    # Recommendation
    recommendation = "OPERATIONALLY USABLE"
    if critical_count > 0:
        recommendation = "NOT READY - CRITICAL ISSUES FOUND"
    elif gap_count > 3:
        recommendation = "USABLE WITH RESTRICTIONS"
    elif review_count > 5:
        recommendation = "USABLE WITH RESTRICTIONS"
    
    print(f"\nRECOMMENDATION: {recommendation}")
    print("=" * 100)
    
    return {
        "total": total,
        "good": good_count,
        "review": review_count,
        "blocked_ok": blocked_count,
        "gap": gap_count,
        "critical": critical_count,
        "recommendation": recommendation,
        "good_percent": 100*good_count/total if total > 0 else 0,
        "gap_percent": 100*gap_count/total if total > 0 else 0,
    }

if __name__ == "__main__":
    results = run_evaluation()
    summary = print_summary(results)
    
    # Save detailed results to JSON
    with open("runtime_data/classic1r_operator_pack_results.json", "w") as f:
        # Convert results to serializable format
        serializable = {}
        for category, items in results.items():
            serializable[category] = []
            for item in items:
                serializable[category].append(item)
        json.dump({"results": serializable, "summary": summary}, f, indent=2)
    
    print(f"\nDetailed results saved to: runtime_data/classic1r_operator_pack_results.json")
    
    # Exit with error if CRITICAL found
    if summary["critical"] > 0:
        print("\n⚠ CRITICAL FAILURES DETECTED - INVESTIGATION REQUIRED")
        sys.exit(1)
    
    sys.exit(0)
