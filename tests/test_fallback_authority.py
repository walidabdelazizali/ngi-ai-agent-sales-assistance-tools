import pytest

from src.agent_adapter import handle_user_query
from src.query.business_answer import answer_business_query


def test_business_answer_returns_structured_fallback_signal_english():
    out = answer_business_query("How do I get a discount?")

    assert isinstance(out, str)
    assert getattr(out, "is_fallback", False) is True
    assert "No deterministic answer" in str(out)


def test_business_answer_returns_structured_fallback_signal_arabic():
    out = answer_business_query("كيف أحصل على خصم؟")

    assert isinstance(out, str)
    assert getattr(out, "is_fallback", False) is True
    assert "عذراً" in str(out)


@pytest.mark.parametrize("output_mode", ["dict", "text"])
def test_adapter_uses_structured_fallback_signal_without_string_inspection(monkeypatch, output_mode):
    import src.agent_adapter as adapter
    import src.agent_wrapper as agent_wrapper_module
    import src.query.business_answer as business_answer_module

    fallback_result = {
        "ok": False,
        "intent": "unsupported",
        "plan_name": None,
        "tool_name": None,
        "data": None,
        "message": "Canonical fallback message",
        "normalized": {"status": "not_found", "tool": None, "answer": None, "errors": ["Canonical fallback message"]},
    }

    def _explode_lower(self):
        raise AssertionError("adapter should not inspect fallback text")

    monkeypatch.setattr(business_answer_module.StructuredFallbackAnswer, "lower", _explode_lower, raising=False)
    monkeypatch.setattr(agent_wrapper_module, "run_agent_wrapper", lambda _query: fallback_result)

    out = handle_user_query("How do I get a discount?", output_mode)

    if output_mode == "dict":
        assert out == fallback_result
    else:
        assert out == "Canonical fallback message"
