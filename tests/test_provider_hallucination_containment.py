from src.agent_wrapper import run_agent_wrapper
from src.query.network_lookup import NetworkLookup


def test_critical_provider_hallucination_queries_are_blocked_or_ambiguous():
    queries = [
        "Is Burjeel Hospital in the network?",
        "هل Burjeel Hospital داخل الشبكة؟",
        "Is Royal Hospital in the network?",
        "هل Royal Hospital داخل الشبكة؟",
        "في أي شبكة Imaginary Clinic",
        "Royal Hospital في أي شبكة",
        "NoSuch Hospital in which network?",
        "Unknown Future Hospital في أي شبكة",
        "Imaginary Clinic في أي شبكة",
        "Provider xyzq in which network?",
    ]
    for q in queries:
        out = run_agent_wrapper(q)
        assert out["intent"] == "network_lookup"
        assert out["tool_name"] == "network_lookup"
        assert out["ok"] is False
        msg = str(out["message"])
        assert (
            "Ambiguous provider match" in msg
            or "مزود غير محدد" in msg
            or "Provider not found." in msg
            or "المزود غير موجود" in msg
        ), msg


def test_arabic_family_tokens_escalate_to_ambiguity():
    lookup = NetworkLookup()
    for q in [
        "هل برجيل داخل الشبكة؟",
        "هل رويال داخل الشبكة؟",
        "هل استر داخل الشبكة؟",
        "هل ان ام سي داخل الشبكة؟",
    ]:
        msg = str(lookup.answer_query(q))
        assert "Ambiguous provider match" in msg or "مزود غير محدد" in msg, msg


def test_unknown_provider_not_found_hard_block():
    lookup = NetworkLookup()
    for q in [
        "Imaginary Clinic in which network?",
        "NoSuch Hospital in which network?",
        "Provider xyzq in which network?",
    ]:
        msg = str(lookup.answer_query(q))
        assert msg == "Provider not found.", msg


def test_malformed_provider_names_do_not_guess_membership():
    lookup = NetworkLookup()
    for q in [
        "burj dh? network",
        "Royal Hospital ??? network",
        "provider xyz ??? network ???",
    ]:
        msg = str(lookup.answer_query(q))
        assert (
            msg == "Provider not found."
            or "Ambiguous provider match" in msg
            or "مزود غير محدد" in msg
        ), msg
