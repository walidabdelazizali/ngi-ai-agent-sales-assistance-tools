from src.telegram_transport import handle_telegram_message

def test_plan_core():
    out = handle_telegram_message("What is the annual limit for Remedy 04?")
    assert "not available" in out.lower() or "غير متاحة" in out

def test_reimbursement_rules():
    out = handle_telegram_message("What are the reimbursement rules for Remedy 05?")

def test_plan_summary():
    out = handle_telegram_message("Give me a summary of Remedy 04")

def test_unsupported_plan():
    out = handle_telegram_message("Tell me about Remedy 99")
    assert "Intent: unsupported" in out
    assert "supported plan" in out.lower()

def test_empty_input():
    out = handle_telegram_message("")
    assert "didn't receive a valid question" in out.lower()

def test_regression_safe():
    queries = [
        "What is the annual limit for Remedy 04?",
        "What are the reimbursement rules for Remedy 05?",
        "Give me a summary of Remedy 04",
        "Tell me about Remedy 99",
        ""
    ]
    for q in queries:
        out = handle_telegram_message(q)
        assert isinstance(out, str)
        assert out
