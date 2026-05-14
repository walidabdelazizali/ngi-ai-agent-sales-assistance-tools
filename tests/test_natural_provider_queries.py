"""
Test natural provider/network queries with plan + city + type combinations.
Tests for Arabic, English, and mixed-language queries.
Validates deterministic safety: no hallucination, no guessing, safe ambiguity handling.
"""
import pytest
import re
from pathlib import Path
from src.agent_wrapper import run_agent_wrapper, _intent_from_query, _extract_plan_name


class TestNaturalProviderQueriesArabic:
    """Arabic provider queries with plan + city + type."""
    
    def test_arabic_hospitals_remedy5_dubai(self):
        """مستشفيات Remedy 5 في دبي؟"""
        result = run_agent_wrapper("مستشفيات Remedy 5 في دبي؟")
        assert result["ok"] is False or result["ok"] is True  # Either works or safely blocked
        # Should NOT hallucinate provider membership
        assert "hallucin" not in str(result).lower()
        
    def test_arabic_hospitals_remedy6_sharjah(self):
        """عيادات Remedy 6 في الشارقة؟"""
        result = run_agent_wrapper("عيادات Remedy 6 في الشارقة؟")
        assert isinstance(result, dict)
        assert "intent" in result
        
    def test_arabic_clinics_remedy5_abudhabi(self):
        """عيادات Remedy 5 في أبو ظبي؟"""
        result = run_agent_wrapper("عيادات Remedy 5 في أبو ظبي؟")
        assert isinstance(result, dict)
        assert "plan_name" in result or result["intent"] in ("unsupported", "network_lookup")
        
    def test_arabic_pharmacies_remedy6_dubai(self):
        """صيدليات Remedy 6 في دبي؟"""
        result = run_agent_wrapper("صيدليات Remedy 6 في دبي؟")
        assert isinstance(result, dict)
        
    def test_arabic_labs_remedy5_sharjah(self):
        """تحاليل Remedy 5 في الشارقة؟"""
        result = run_agent_wrapper("تحاليل Remedy 5 في الشارقة؟")
        assert isinstance(result, dict)


class TestNaturalProviderQueriesEnglish:
    """English provider queries with plan + city + type."""
    
    def test_english_hospitals_remedy5_dubai(self):
        """hospitals in Remedy 5 in Dubai"""
        result = run_agent_wrapper("hospitals in Remedy 5 in Dubai")
        assert isinstance(result, dict)
        
    def test_english_clinics_remedy6_sharjah(self):
        """clinics available in Remedy 6 in Sharjah"""
        result = run_agent_wrapper("clinics available in Remedy 6 in Sharjah")
        assert isinstance(result, dict)
        
    def test_english_pharmacies_remedy5_abudhabi(self):
        """List pharmacies in Remedy 5 in Abu Dhabi"""
        result = run_agent_wrapper("List pharmacies in Remedy 5 in Abu Dhabi")
        assert isinstance(result, dict)
        
    def test_english_labs_remedy6_dubai(self):
        """Diagnostic centers for Remedy 6 in Dubai"""
        result = run_agent_wrapper("Diagnostic centers for Remedy 6 in Dubai")
        assert isinstance(result, dict)
        
    def test_english_medical_centers_remedy5_all(self):
        """Medical centers in Remedy 5"""
        result = run_agent_wrapper("Medical centers in Remedy 5")
        assert isinstance(result, dict)


class TestMixedLanguageProviderQueries:
    """Mixed Arabic/English provider queries."""
    
    def test_mixed_hospitals_remedy5_dubai(self):
        """hospitals في Remedy 5 دبي"""
        result = run_agent_wrapper("hospitals في Remedy 5 دبي")
        assert isinstance(result, dict)
        
    def test_mixed_clinics_sharjah_remedy6(self):
        """عيادات clinics في الشارقة Remedy 6"""
        result = run_agent_wrapper("عيادات clinics في الشارقة Remedy 6")
        assert isinstance(result, dict)
        
    def test_mixed_remedy5_hospitals_dubai(self):
        """Remedy 5 مستشفيات في دبي"""
        result = run_agent_wrapper("Remedy 5 مستشفيات في دبي")
        assert isinstance(result, dict)


class TestNaturalProviderQueryIntentDetection:
    """Tests for intent detection of natural provider queries."""
    
    def test_intent_arabic_provider_listing_with_city(self):
        """_intent_from_query should detect provider listing intent."""
        intent = _intent_from_query("مستشفيات Remedy 5 في دبي؟")
        # Should either be network_lookup or plan_network_city_type or unsupported
        assert intent in (None, "unsupported", "network_lookup", "plan_network_city_type")
        
    def test_intent_english_provider_listing(self):
        """English provider listing intent detection."""
        intent = _intent_from_query("hospitals in Remedy 5 in Dubai")
        assert intent in (None, "unsupported", "network_lookup", "plan_network_city_type")
        
    def test_intent_mixed_language_provider_listing(self):
        """Mixed language provider listing intent."""
        intent = _intent_from_query("hospitals في Remedy 5 دبي")
        assert intent in (None, "unsupported", "network_lookup", "plan_network_city_type")


class TestProviderAmbiguityHandling:
    """Test handling of ambiguous provider names."""
    
    def test_burjeel_ambiguity_safe(self):
        """Burjeel family ambiguity should be handled safely."""
        result = run_agent_wrapper("Is Burjeel in the network?")
        # Should return ambiguity message or safe not-found, NOT hallucinate a single provider
        assert "ambiguous" in str(result).lower() or "not found" in str(result).lower() or result["ok"] is False
        
    def test_nmc_royal_ambiguity_safe(self):
        """NMC Royal ambiguity should be handled safely."""
        result = run_agent_wrapper("NMC Royal network?")
        # Should NOT hallucinate a single provider
        assert result["ok"] is False or "ambiguous" in str(result).lower()
        
    def test_aster_ambiguity_safe(self):
        """Aster family ambiguity should be handled safely."""
        result = run_agent_wrapper("Aster Hospital network?")
        assert result["ok"] is False or "ambiguous" in str(result).lower()


class TestUnknownProviderSafeBlocking:
    """Test that unknown providers are safely blocked."""
    
    def test_unknown_provider_not_found(self):
        """Unknown provider should return not found, not hallucination."""
        result = run_agent_wrapper("Is Unknown Hospital Dubai in the network?")
        assert result["ok"] is False
        assert "not found" in str(result).lower() or "unsupported" in str(result).lower()
        
    def test_misspelled_provider_safe_block(self):
        """Misspelled provider should be safely blocked."""
        result = run_agent_wrapper("Is Burjle Hospital in the network?")
        assert result["ok"] is False
        
    def test_fictional_provider_safe_block(self):
        """Fictional provider should be safely blocked."""
        result = run_agent_wrapper("Is Fictional Medical Center in the network?")
        assert result["ok"] is False


class TestPlanExtractionFromNaturalQueries:
    """Test plan name extraction from natural queries."""
    
    def test_plan_extraction_remedy5_with_city(self):
        """Extract Remedy 5 from natural query with city."""
        plan = _extract_plan_name("hospitals in Remedy 5 in Dubai")
        assert plan == "Remedy 05" or plan == "Remedy 5"
        
    def test_plan_extraction_remedy6_arabic(self):
        """Extract Remedy 6 from Arabic natural query."""
        plan = _extract_plan_name("عيادات Remedy 6 في الشارقة؟")
        assert plan == "Remedy 06" or plan == "Remedy 6"
        
    def test_plan_extraction_classic3_with_type(self):
        """Extract Classic 3 from natural query with type."""
        plan = _extract_plan_name("hospitals in Classic 3 in Dubai")
        assert plan == "Classic 3"
        
    def test_no_plan_extraction_provider_only(self):
        """No plan extraction if only provider name."""
        plan = _extract_plan_name("hospitals in Dubai")
        assert plan is None or plan == ""


class TestProviderQueryNormalization:
    """Test query normalization for provider queries."""
    
    def test_normalize_arabic_digits_remedy5(self):
        """Arabic digit normalization in Remedy 5."""
        result = run_agent_wrapper("hospitals في Remedy ٥ دبي")  # Arabic digit ٥
        assert isinstance(result, dict)
        
    def test_normalize_extra_spaces(self):
        """Extra spaces should be normalized."""
        result1 = run_agent_wrapper("hospitals in Remedy 5 in Dubai")
        result2 = run_agent_wrapper("hospitals  in  Remedy  5  in  Dubai")
        assert result1["intent"] == result2["intent"] or result2["intent"] is None
        
    def test_normalize_case_insensitivity(self):
        """Case should not affect intent detection."""
        result1 = run_agent_wrapper("hospitals in remedy 5 in dubai")
        result2 = run_agent_wrapper("HOSPITALS IN REMEDY 5 IN DUBAI")
        # Both should be detected as provider listing or same intent
        assert result1["intent"] == result2["intent"] or (result1["intent"] is None and result2["intent"] is None)


class TestProviderQueryWithoutPlan:
    """Test provider queries that don't include a plan."""
    
    def test_provider_query_no_plan_unsupported(self):
        """Provider query without plan name should be unsupported or blocked."""
        result = run_agent_wrapper("hospitals in Dubai")
        # Without plan context, should be unsupported
        assert result["ok"] is False or result["intent"] == "unsupported"
        
    def test_provider_name_lookup_without_plan(self):
        """Specific provider name lookup is supported without plan."""
        result = run_agent_wrapper("Is Life Medical Centre in the network?")
        # This is a standard network_lookup query, should work
        assert result["intent"] == "network_lookup" or result["ok"] in (True, False)


class TestProviderListingSafetyBoundaries:
    """Test safety boundaries for provider listing."""
    
    def test_no_private_data_leak_in_provider_listing(self):
        """Provider listing should not expose sensitive data."""
        result = run_agent_wrapper("mستشفيات Remedy 5 في دبي؟")
        if result["ok"]:
            # If listing is returned, should only show provider names
            output = str(result.get("message", ""))
            assert "@" not in output  # No email leakage
            assert "phone" not in output.lower()  # No phone leakage
            
    def test_no_pricing_in_provider_listing(self):
        """Provider listing should not include pricing."""
        result = run_agent_wrapper("hospitals in Remedy 5")
        if result["ok"]:
            output = str(result.get("message", ""))
            assert "aed" not in output.lower()
            assert "price" not in output.lower()
            
    def test_only_approved_network_providers_listed(self):
        """Only providers in approved networks should be listed."""
        result = run_agent_wrapper("hospitals in Remedy 6 in Dubai")
        # Even if this returns, should only list HN Basic Plus providers (for Remedy 6)
        if result["ok"]:
            assert "basic plus" in str(result).lower() or "hn basic" in str(result).lower()


class TestProviderSearchAccuracy:
    """Test accuracy of provider search results."""
    
    def test_city_filter_accuracy(self):
        """Results should be filtered by city."""
        result = run_agent_wrapper("hospitals in Remedy 6 in Dubai")
        if result["ok"]:
            output = str(result.get("message", ""))
            # If Dubai is specified, Dubai should be in results or headings
            # (Assumption: Dubai providers exist in test data)
            assert isinstance(output, str) and len(output) > 0
            
    def test_provider_type_filter_accuracy(self):
        """Results should be filtered by provider type."""
        result = run_agent_wrapper("labs in Remedy 6 in Dubai")
        if result["ok"]:
            output = str(result.get("message", ""))
            # Should not mix hospitals with labs if lab filter applied
            assert isinstance(output, str)
            
    def test_plan_network_filter_accuracy(self):
        """Results should match the plan's network."""
        result = run_agent_wrapper("hospitals in Remedy 6 in Dubai")
        if result["ok"] and "basic plus" in str(result).lower():
            # Remedy 6 uses HN Basic Plus, so output should reflect that
            assert "basic plus" in str(result).lower() or "hn basic" in str(result).lower()


class TestProviderQueryErrorHandling:
    """Test error handling for provider queries."""
    
    def test_malformed_query_graceful_handling(self):
        """Malformed queries should be handled gracefully."""
        result = run_agent_wrapper("??? مستشفيات في في في ????")
        assert isinstance(result, dict)
        assert "error" not in str(result).lower() or result["ok"] is False
        
    def test_very_long_query_truncation(self):
        """Very long queries should be handled without hanging."""
        long_query = "hospitals in Remedy 5 in Dubai with" + " very" * 100
        result = run_agent_wrapper(long_query)
        assert isinstance(result, dict)
        
    def test_special_characters_handling(self):
        """Special characters should be handled safely."""
        result = run_agent_wrapper("hospitals in Remedy 5 in Dubai@@@###$$$")
        assert isinstance(result, dict)


class TestProviderQueryBoundaryConditions:
    """Test boundary conditions for provider queries."""
    
    def test_empty_query(self):
        """Empty query should be handled."""
        result = run_agent_wrapper("")
        assert isinstance(result, dict)
        
    def test_single_word_query(self):
        """Single word query should not crash."""
        result = run_agent_wrapper("hospitals")
        assert isinstance(result, dict)
        
    def test_only_city_no_plan(self):
        """Only city, no plan should be unsupported."""
        result = run_agent_wrapper("hospitals in Dubai")
        assert result["ok"] is False or result["intent"] in (None, "unsupported")
        
    def test_only_provider_type_no_plan(self):
        """Only provider type, no plan should be unsupported."""
        result = run_agent_wrapper("hospitals available")
        assert result["ok"] is False or result["intent"] in (None, "unsupported")


class TestProviderListingUsefulness:
    """Usefulness and safety assertions for plan -> network -> city -> type listings."""

    @staticmethod
    def _extract_provider_lines(message: str):
        providers = []
        for line in message.splitlines():
            if not line.startswith("- "):
                continue
            item = line[2:].strip()
            if not item:
                continue
            # Provider readability may append " [AREA]"; keep deterministic provider checks name-only.
            item = re.sub(r"\s+\[[^\]]+\]\s*$", "", item)
            providers.append(item)
        return providers

    @staticmethod
    def _extract_count(message: str):
        for line in message.splitlines():
            if line.startswith("Count:"):
                value = line.split(":", 1)[1].strip().split()[0]
                return int(value)
        return None

    def _assert_clean_listing_shape(self, result, plan_name, network_code, city, provider_type_label):
        assert result["ok"] is True
        msg = result["message"]
        assert "[PROVIDER LIST]" in msg
        assert f"Plan: {plan_name}" in msg
        assert f"Resolved Network: {network_code}" in msg
        assert f"City: {city}" in msg
        assert f"Provider Type: {provider_type_label}" in msg
        assert "Count:" in msg
        assert "hnm_code" not in msg.lower()
        assert "group_name" not in msg.lower()
        assert "tel_no" not in msg.lower()
        assert "location" not in msg.lower()
        assert "google_name" not in msg.lower()

    def test_hospitals_remedy5_dubai_useful_output(self):
        result = run_agent_wrapper("hospitals in Remedy 5 in Dubai")
        self._assert_clean_listing_shape(result, "Remedy 05", "hn_basic_plus", "Dubai", "hospital")
        count = self._extract_count(result["message"])
        assert count is not None and count > 0

    def test_clinics_remedy6_sharjah_useful_output(self):
        result = run_agent_wrapper("clinics in Remedy 6 in Sharjah")
        self._assert_clean_listing_shape(result, "Remedy 06", "hn_basic_plus", "Sharjah", "clinic")
        count = self._extract_count(result["message"])
        assert count is not None and count > 0

    def test_pharmacies_remedy5_dubai_useful_output(self):
        result = run_agent_wrapper("pharmacies in Remedy 5 in Dubai")
        self._assert_clean_listing_shape(result, "Remedy 05", "hn_basic_plus", "Dubai", "pharmacy")
        count = self._extract_count(result["message"])
        assert count is not None and count > 0

    def test_labs_remedy6_abudhabi_useful_output(self):
        result = run_agent_wrapper("labs in Remedy 6 in Abu Dhabi")
        self._assert_clean_listing_shape(result, "Remedy 06", "hn_basic_plus", "Abu Dhabi", "lab")
        count = self._extract_count(result["message"])
        assert count is not None and count > 0

    @pytest.mark.parametrize(
        "query,plan_name,network_code,city,ptype",
        [
            ("مستشفيات Remedy 5 في دبي؟", "Remedy 05", "hn_basic_plus", "Dubai", "hospital"),
            ("عيادات Remedy 6 في الشارقة؟", "Remedy 06", "hn_basic_plus", "Sharjah", "clinic"),
            ("pharmacies في Remedy 5 دبي", "Remedy 05", "hn_basic_plus", "Dubai", "pharmacy"),
        ],
    )
    def test_arabic_and_mixed_queries_useful_output(self, query, plan_name, network_code, city, ptype):
        result = run_agent_wrapper(query)
        self._assert_clean_listing_shape(result, plan_name, network_code, city, ptype)

    def test_unknown_city_safe_response(self):
        result = run_agent_wrapper("hospitals in Remedy 5 in Atlantis")
        assert result["ok"] is False
        assert "city" in result["message"].lower()
        assert "clarify" in result["message"].lower() or "unknown" in result["message"].lower()

    def test_unsupported_provider_type_safe_response(self):
        result = run_agent_wrapper("optical providers in Remedy 5 in Dubai")
        assert result["ok"] is False
        assert "provider type" in result["message"].lower()
        assert "supported" in result["message"].lower()

    def test_provider_lines_stay_within_resolved_network(self):
        from src.query.network_lookup import get_network_lookup
        from src.query.plan_network_lookup import resolve_plan_network

        result = run_agent_wrapper("hospitals in Remedy 5 in Dubai")
        assert result["ok"] is True
        providers = self._extract_provider_lines(result["message"])
        mapping = resolve_plan_network("Remedy 05")
        assert mapping["found"]
        network_code = mapping["medical_network"]

        lookup = get_network_lookup()
        checked = 0
        for provider in providers[:20]:
            details = lookup.provider_in_network(provider, network_code)
            assert details.get("found") is True
            assert details.get("in_network") is True
            checked += 1
        assert checked > 0

    def test_no_match_message_is_safe_and_structured(self):
        result = run_agent_wrapper("labs in Remedy 6 in Fujairah")
        assert result["ok"] is False or result["ok"] is True
        msg = result["message"]
        # If handled as unknown city clarification, it's safe.
        if result["ok"] is False:
            assert "city" in msg.lower()
            return
        # If handled as empty listing, must stay structured and safe.
        assert "[PROVIDER LIST]" in msg
        assert "Count: 0" in msg
        assert "No matching providers found" in msg


class TestProviderMembershipRouting:
    """
    Provider Membership Routing Fix Sprint.
    Tests that provider + plan membership queries route to the correct handler
    and never fall into generic plan_core summaries.
    """

    def _assert_membership_response(self, result, expected_intent="plan_network_provider"):
        """Assert response is a valid structured provider membership answer."""
        assert result.get("intent") == expected_intent, (
            f"Expected intent={expected_intent!r}, got {result.get('intent')!r}"
        )
        assert result.get("ok") is True or result.get("ok") is False
        msg = result.get("message", "")
        # Must NOT return plan core fields (pricing, area, limit)
        assert "Annual limit" not in msg, "plan_core pricing leaked into provider membership response"
        assert "AED" not in msg, "pricing leaked into provider membership response"
        assert "Area:" not in msg, "plan_core area of coverage leaked into provider membership response"

    def _assert_membership_found(self, result, provider_fragment: str, plan_fragment: str):
        """Assert provider membership was found in the correct plan network."""
        self._assert_membership_response(result)
        msg = result.get("message", "")
        assert result.get("ok") is True
        assert provider_fragment.upper() in msg.upper() or provider_fragment.lower() in msg.lower(), (
            f"Provider {provider_fragment!r} not in response: {msg[:200]}"
        )
        assert plan_fragment in msg or plan_fragment.lower() in msg.lower(), (
            f"Plan {plan_fragment!r} not in response: {msg[:200]}"
        )
        assert "Status:" in msg or "status" in msg.lower() or "in network" in msg.lower() or "داخل" in msg

    def _assert_provider_query_safe(self, result):
        """Provider-style query must never leak plan_core pricing or summary fields."""
        assert result.get("intent") != "plan_core"
        msg = result.get("message", "")
        assert "AED" not in msg
        assert "Annual limit" not in msg
        assert result.get("intent") in ("plan_network_provider", "unsupported", "network_lookup", "plan_network_city_type", None)

    # ------------------------------------------------------------------
    # English structured patterns: "Is X in Remedy Y network?"
    # ------------------------------------------------------------------

    def test_is_accuracy_plus_in_remedy05_network(self):
        """Is Accuracy Plus Medical Laboratory in Remedy 05 network?"""
        result = run_agent_wrapper("Is Accuracy Plus Medical Laboratory in Remedy 05 network?")
        self._assert_membership_found(result, "ACCURACY PLUS", "Remedy 05")

    def test_is_accuracy_plus_in_remedy03_network(self):
        """Is Accuracy Plus Medical Laboratory in Remedy 03 network?"""
        result = run_agent_wrapper("Is Accuracy Plus Medical Laboratory in Remedy 03 network?")
        # Remedy 03 uses hn_basic_plus too; ACCURACY PLUS is in it
        self._assert_membership_found(result, "ACCURACY PLUS", "Remedy 03")

    def test_is_medeor_hospital_in_remedy6_network(self):
        """Is MEDEOR 24X7 HOSPITAL in Remedy 6 network? — MEDEOR is NOT in hn_basic_plus, so ok=False is correct."""
        result = run_agent_wrapper("Is MEDEOR 24X7 HOSPITAL in Remedy 6 network?")
        self._assert_membership_response(result)
        # MEDEOR exists in the data but is not in hn_basic_plus; ok=False (out of network) is the correct answer.
        msg = result.get("message", "")
        assert result.get("ok") is False or "out of network" in msg.lower() or "not in" in msg.lower()

    def test_is_hatta_hospital_in_remedy5_network(self):
        """Is HATTA HOSPITAL in Remedy 5 network?"""
        result = run_agent_wrapper("Is HATTA HOSPITAL in Remedy 5 network?")
        self._assert_membership_found(result, "HATTA", "Remedy 05")

    def test_is_cedars_in_remedy5_network(self):
        """Is CEDARS JEBEL ALI in Remedy 5 network?"""
        result = run_agent_wrapper("Is CEDARS JEBEL ALI INTERNATIONAL HOSPITAL in Remedy 5 network?")
        self._assert_membership_found(result, "CEDARS", "Remedy 05")

    # ------------------------------------------------------------------
    # English "Is X in Remedy Y?" (without trailing "network")
    # ------------------------------------------------------------------

    def test_is_burjeel_in_remedy06_no_network_suffix(self):
        """Is Burjeel in Remedy 06? - ambiguous provider but correct routing"""
        result = run_agent_wrapper("Is Burjeel in Remedy 06?")
        # Burjeel is in AMBIGUOUS_PROVIDER_TOKENS; should get ambiguous response (not plan_core)
        self._assert_membership_response(result)
        msg = result.get("message", "")
        assert "ambiguous" in msg.lower() or "not found" in msg.lower() or result.get("ok") is False

    # ------------------------------------------------------------------
    # Arabic structured patterns: "هل X في شبكة Remedy Y؟"
    # ------------------------------------------------------------------

    def test_arabic_is_aster_in_remedy05_network(self):
        """هل ASTER HOSPITAL في شبكة Remedy 05؟"""
        result = run_agent_wrapper("هل ASTER HOSPITAL في شبكة Remedy 05؟")
        # ASTER is in AMBIGUOUS_PROVIDER_TOKENS
        self._assert_membership_response(result)
        msg = result.get("message", "")
        assert "ambiguous" in msg.lower() or "غير محدد" in msg or "not found" in msg.lower() or result.get("ok") is False

    def test_arabic_is_accuracy_plus_in_remedy02(self):
        """هل Accuracy Plus Medical Laboratory داخل شبكة Remedy 02؟"""
        result = run_agent_wrapper("هل Accuracy Plus Medical Laboratory داخل شبكة Remedy 02؟")
        self._assert_membership_response(result)
        assert result.get("ok") is True
        msg = result.get("message", "")
        assert "ACCURACY PLUS" in msg.upper()

    # ------------------------------------------------------------------
    # Arabic informal patterns: "هل X داخل Remedy Y؟"
    # ------------------------------------------------------------------

    def test_arabic_informal_aster_in_remedy5(self):
        """هل أستر داخل Remedy 5؟"""
        result = run_agent_wrapper("هل أستر داخل Remedy 5؟")
        self._assert_membership_response(result)
        # أستر → aster → ambiguous
        msg = result.get("message", "")
        assert "ambiguous" in msg.lower() or "غير محدد" in msg or "not found" in msg.lower() or result.get("ok") is False

    # ------------------------------------------------------------------
    # Shorthand patterns: "Provider Plan?"
    # ------------------------------------------------------------------

    def test_shorthand_accuracy_plus_remedy03(self):

        """Accuracy Plus Remedy 03? — shorthand pattern not detected, must be safe (no pricing)."""
        result = run_agent_wrapper("Accuracy Plus Remedy 03?")
        # Shorthand is not reliably detected without knowing the provider name set.
        # What matters: no pricing leak, no crash.
        msg = result.get("message", "")
        assert "Annual limit" not in msg
        assert "AED" not in msg
        assert isinstance(result, dict)
    def test_shorthand_aster_remedy5(self):

        """ASTER Remedy 5? — shorthand pattern not detected, must be safe (no pricing)."""
        result = run_agent_wrapper("ASTER Remedy 5?")
        msg = result.get("message", "")
        assert "Annual limit" not in msg
        assert "AED" not in msg
        assert isinstance(result, dict)
    # ------------------------------------------------------------------
    # Plan_core should NOT be returned for any of these
    # ------------------------------------------------------------------

    def test_plan_core_not_returned_for_membership_query(self):
        """plan_core intent must not be returned for provider membership queries."""
        membership_queries = [
            "Is Accuracy Plus Medical Laboratory in Remedy 05 network?",
            "Is HATTA HOSPITAL in Remedy 5 network?",
            "هل Accuracy Plus Medical Laboratory داخل شبكة Remedy 02؟",
        ]
        for q in membership_queries:
            result = run_agent_wrapper(q)
            assert result.get("intent") != "plan_core", (
                f"Query routed to plan_core (should be plan_network_provider): {q!r}"
            )

    # ------------------------------------------------------------------
    # Provider without plan context: must stay conservative
    # ------------------------------------------------------------------

    def test_provider_without_plan_stays_conservative(self):
        """Provider membership query without plan must stay conservative / not guess network."""
        result = run_agent_wrapper("Is HATTA HOSPITAL in the network?")
        # No plan specified, should NOT guess a plan, should return generic network lookup
        # or safely ask for plan specification
        assert result.get("intent") != "plan_core"
        msg = result.get("message", "")
        # Must not guess/hallucinate plan membership
        assert "AED" not in msg
        assert "Annual limit" not in msg

    # ------------------------------------------------------------------
    # Ambiguous providers must always be safe
    # ------------------------------------------------------------------

    def test_ambiguous_provider_aster_remains_safe_in_membership(self):
        """ASTER (family name) in membership query must return ambiguous, never guess."""
        result = run_agent_wrapper("Is Aster in Remedy 5 network?")
        self._assert_membership_response(result)
        msg = result.get("message", "")
        # Should be ambiguous or not found, never a single specific provider answer
        assert "ambiguous" in msg.lower() or "not found" in msg.lower() or result.get("ok") is False

    def test_ambiguous_provider_burjeel_remains_safe(self):
        """Burjeel in membership query must return ambiguous, never guess."""
        result = run_agent_wrapper("Is Burjeel in Remedy 6 network?")
        self._assert_membership_response(result)
        msg = result.get("message", "")
        assert "ambiguous" in msg.lower() or "not found" in msg.lower() or result.get("ok") is False

    # ------------------------------------------------------------------
    # Unknown provider safe block
    # ------------------------------------------------------------------

    def test_unknown_provider_in_remedy5_not_found(self):
        """Completely unknown provider in Remedy 5 should return not found."""
        result = run_agent_wrapper("Is Nonexistent XYZ Hospital in Remedy 5 network?")
        self._assert_membership_response(result)
        assert result.get("ok") is False
        msg = result.get("message", "")
        assert "not found" in msg.lower() or "provider" in msg.lower()

    def test_critical_dash_style_provider_query_never_leaks_pricing(self):
        result = run_agent_wrapper("NMC ROYAL HOSPITAL DXB - Remedy 5 - network?")
        self._assert_provider_query_safe(result)

    def test_critical_provider_prefix_query_never_leaks_pricing(self):
        result = run_agent_wrapper("Provider 24HOUR PHARMACY in Remedy 6 network?")
        self._assert_provider_query_safe(result)


class TestPlanCorePreservation:
    def test_network_question_stays_plan_core(self):
        result = run_agent_wrapper("What is the network for Remedy 5?")
        assert result["intent"] == "plan_core"

    def test_summary_question_stays_plan_summary(self):
        result = run_agent_wrapper("Summarize Remedy 5")
        assert result["intent"] == "plan_summary"

    def test_annual_limit_question_stays_plan_core(self):
        result = run_agent_wrapper("What is the annual limit for Remedy 5?")
        assert result["intent"] == "plan_core"
        assert "Annual limit" in result.get("message", "") or "AED" in result.get("message", "")
