from src.agent_wrapper import _extract_plan_name, run_agent_wrapper


def test_arabic_shorthand_plan_aliases_are_explicitly_normalized():
    assert _extract_plan_name("ريمدي5") == "Remedy 05"
    assert _extract_plan_name("رمدي 5") == "Remedy 05"
    assert _extract_plan_name("كلاسك 1") == "Classic 1"
    assert _extract_plan_name("برايم2") == "Prime 2"


def test_arabic_shorthand_routes_without_broad_inference():
    out = run_agent_wrapper("ليمت رمدي 5")
    assert out["ok"] is True
    assert out["intent"] == "plan_core"
    assert out["plan_name"] == "Remedy 05"


def test_provider_abbreviation_sgh_membership_query_routes_deterministically():
    out = run_agent_wrapper("Is SGH in Remedy 5 network?")
    assert out["intent"] == "plan_network_provider"
    assert "Could not determine provider name" not in out["message"]


def test_provider_abbreviation_nmc_dxb_membership_query_routes_deterministically():
    out = run_agent_wrapper("Provider NMC DXB in Remedy 5 network?")
    assert out["intent"] == "plan_network_provider"
    assert "Could not determine provider name" not in out["message"]


def test_provider_abbreviation_aster_qusais_membership_query_routes_deterministically():
    out = run_agent_wrapper("Is Aster Qusais in Remedy 5 network?")
    assert out["intent"] == "plan_network_provider"
    assert "Could not determine provider name" not in out["message"]


def test_broker_phrasing_available_under_routes_to_existing_membership_intent():
    out = run_agent_wrapper("Is SGH available under Remedy 5?")
    assert out["intent"] == "plan_network_provider"


def test_broker_phrasing_covered_routes_to_existing_membership_intent():
    out = run_agent_wrapper("Is SGH covered in Remedy 5?")
    assert out["intent"] == "plan_network_provider"


def test_broker_phrasing_arabic_network_variants_route_to_existing_membership_intent():
    for q in [
        "هل SGH ضمن الشبكة Remedy 5؟",
        "هل SGH موجود بالشبكة Remedy 5؟",
        "هل SGH يشمله Remedy 5؟",
    ]:
        out = run_agent_wrapper(q)
        assert out["intent"] == "plan_network_provider"


def test_planless_broker_phrasing_remains_unsupported():
    for q in ["في الشبكة؟", "يشمله؟", "covered?", "direct billing?"]:
        out = run_agent_wrapper(q)
        assert out["ok"] is False
        assert out["intent"] == "unsupported"


def test_safety_boundary_recommendation_style_still_blocked():
    out = run_agent_wrapper("Which is better SGH under Remedy 5 or Remedy 6?")
    assert out["ok"] is False
    assert out["intent"] == "unsupported"
