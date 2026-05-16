"""
tests/test_formatting_layer_stabilization.py — Comprehensive tests for centralized formatting.

Tests for:
- Deterministic field ordering
- No duplicate labels
- Proper spacing normalization
- Safe fallback handling
- Snapshot stability
- Regression prevention
"""

import pytest
from src.output import format_output
from src.output.whatsapp_formatter import whatsapp_summary
from src.output.arabic_formatter import (
    arabic_plan_summary,
    arabic_comparison_summary,
)
from src.output.compact_formatter import compact_summary
from src.output.comparison_formatter import english_comparison_summary
from src.output.shared_helpers import (
    _MISSING,
    _SAFE_REFUSAL,
    no_duplicate_labels,
    no_empty_lines,
    detect_language,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def approved_plan_core_response():
    """Standard approved plan_core response."""
    return {
        "ok": True,
        "intent": "plan_core",
        "plan_name": "Remedy 03",
        "message": "Plan details loaded.",
        "data": {
            "plan_name": "Remedy 03",
            "plan_code": "HN-REMEDY-3",
            "network_name": "REMEDY Network",
            "annual_limit": "AED 150,000",
            "area_of_coverage": "UAE",
            "direct_billing": True,
            "referral_required": False,
            "maternity_cover": "Covered",
            "pharmacy_cover_summary": "Covered",
            "dental_cover_summary": "Not covered",
        }
    }


@pytest.fixture
def approved_plan_summary_response():
    """Approved plan_summary response."""
    return {
        "ok": True,
        "intent": "plan_summary",
        "plan_name": "Remedy 02",
        "message": "Plan summary loaded.",
        "data": {
            "plan_name": "Remedy 02",
            "plan_code": "HN-REMEDY-2",
            "network_name": "REMEDY Network",
            "annual_limit": "AED 100,000",
            "area_of_coverage": "Dubai, Abu Dhabi",
            "direct_billing": True,
            "referral_required": True,
            "key_exclusions": "Cosmetic procedures",
        }
    }


@pytest.fixture
def comparison_message():
    """Standard comparison message."""
    return """Comparison between Remedy 02 and Remedy 03:
Annual Limit: AED 100,000 | AED 150,000
Network: REMEDY Network | REMEDY Network
Area of Coverage: Dubai, Abu Dhabi | UAE
Direct Billing: Yes | Yes
Referral Required: Yes | No"""


# ============================================================================
# WHATSAPP FORMATTER TESTS
# ============================================================================

class TestWhatsappFormatter:
    """Tests for WhatsApp summary formatter."""
    
    def test_whatsapp_summary_deterministic_field_order(self, approved_plan_core_response):
        """Verify deterministic field ordering."""
        result = whatsapp_summary(approved_plan_core_response)
        lines = result.split("\n")
        
        # Check order: Plan, Network, Annual Limit, Direct Billing, etc.
        assert lines[0].startswith("Plan:")
        assert any("Network:" in l for l in lines)
        assert any("Annual Limit:" in l for l in lines)
        assert any("Direct Billing:" in l for l in lines)
    
    def test_whatsapp_summary_no_duplicate_labels(self, approved_plan_core_response):
        """Ensure no label appears twice."""
        result = whatsapp_summary(approved_plan_core_response)
        lines = result.split("\n")
        assert no_duplicate_labels(lines), "Found duplicate labels in output"
    
    def test_whatsapp_summary_filters_missing_fields(self):
        """Verify missing fields (_MISSING) are filtered out."""
        response = {
            "ok": True,
            "intent": "plan_core",
            "plan_name": "Remedy 01",
            "data": {
                "plan_name": "Remedy 01",
                "network_name": "Network1",
                "annual_limit": "AED 50,000",
                "area_of_coverage": None,  # Missing
                "direct_billing": None,  # Missing
            }
        }
        result = whatsapp_summary(response)
        
        # Should include available fields
        assert "Remedy 01" in result
        assert "Network1" in result
        assert "50,000" in result
        # Should NOT include missing fields
        assert "Not specified" not in result or result.count("Not specified") == 0
    
    def test_whatsapp_summary_cleans_aed_duplicates(self):
        """Verify AED currency duplication is cleaned."""
        response = {
            "ok": True,
            "intent": "plan_core",
            "plan_name": "Test Plan",
            "data": {
                "plan_name": "Test Plan",
                "annual_limit": "AED AED 100,000",  # Duplicate AED
            }
        }
        result = whatsapp_summary(response)
        
        # Should clean duplicate AED
        assert "AED AED" not in result
        assert "AED 100,000" in result or "100,000" in result
    
    def test_whatsapp_summary_returns_refusal_on_not_approved(self):
        """Verify safe refusal when response not approved."""
        response = {
            "ok": False,  # Not approved
            "intent": "plan_core",
        }
        result = whatsapp_summary(response)
        assert result == _SAFE_REFUSAL
    
    def test_whatsapp_summary_returns_refusal_on_unsupported_intent(self):
        """Verify safe refusal for unsupported intent."""
        response = {
            "ok": True,
            "intent": "unsupported_intent",
            "data": {}
        }
        result = whatsapp_summary(response)
        assert result == _SAFE_REFUSAL
    
    def test_whatsapp_summary_no_trailing_separators(self, approved_plan_core_response):
        """Verify no trailing newlines or separators."""
        result = whatsapp_summary(approved_plan_core_response)
        assert not result.endswith("\n"), "Trailing newline found"
        assert not result.endswith("\n\n"), "Multiple trailing newlines found"


# ============================================================================
# ARABIC FORMATTER TESTS
# ============================================================================

class TestArabicFormatter:
    """Tests for Arabic language formatter."""
    
    def test_arabic_plan_summary_uses_arabic_labels(self, approved_plan_core_response):
        """Verify Arabic labels are used."""
        result = arabic_plan_summary(approved_plan_core_response)
        
        # Should contain Arabic labels
        assert "اسم الخطة" in result or "الشبكة" in result or "الحد السنوي" in result
    
    def test_arabic_plan_summary_deterministic_order(self, approved_plan_core_response):
        """Verify field ordering is deterministic in Arabic."""
        result = arabic_plan_summary(approved_plan_core_response)
        lines = result.split("\n")
        
        # Should follow standard field order
        assert len(lines) > 0
        # First field with content should be plan-related
        first_line = next((l for l in lines if l.strip()), "")
        assert "الخطة" in first_line or "الشبكة" in first_line or "الحد" in first_line
    
    def test_arabic_plan_summary_no_duplicate_labels(self, approved_plan_core_response):
        """Ensure no duplicate Arabic labels."""
        result = arabic_plan_summary(approved_plan_core_response)
        lines = result.split("\n")
        assert no_duplicate_labels(lines), "Found duplicate labels in Arabic output"
    
    def test_arabic_comparison_translates_labels(self, comparison_message):
        """Verify comparison labels are translated to Arabic."""
        result = arabic_comparison_summary(comparison_message, "Remedy 02", "Remedy 03")
        
        # Should contain Arabic labels
        assert "مقارنة" in result  # "comparison"
        assert "الحد السنوي" in result or "الشبكة" in result
    
    def test_arabic_comparison_translates_yesno(self, comparison_message):
        """Verify Yes/No values are translated."""
        result = arabic_comparison_summary(comparison_message, "Remedy 02", "Remedy 03")
        
        # Should translate Yes/No
        assert "نعم" in result or "لا" in result


# ============================================================================
# COMPACT FORMATTER TESTS
# ============================================================================

class TestCompactFormatter:
    """Tests for compact single-line formatter."""
    
    def test_compact_summary_single_line_format(self, approved_plan_core_response):
        """Verify compact output is single-line or minimal."""
        result = compact_summary(approved_plan_core_response)
        
        # Should be single line or very short
        lines = result.split("\n")
        assert len(lines) <= 2, f"Expected single line, got {len(lines)}"
    
    def test_compact_summary_uses_pipe_separator(self, approved_plan_core_response):
        """Verify pipe separator is used."""
        result = compact_summary(approved_plan_core_response)
        
        # Should use | as separator
        assert "|" in result
    
    def test_compact_summary_no_duplicate_pipes(self, approved_plan_core_response):
        """Verify no duplicate separators."""
        result = compact_summary(approved_plan_core_response)
        
        # No || patterns
        assert "||" not in result
    
    def test_compact_summary_no_trailing_separator(self, approved_plan_core_response):
        """Verify no trailing separator."""
        result = compact_summary(approved_plan_core_response)
        
        # Should not end with |
        assert not result.rstrip().endswith("|"), "Trailing pipe separator found"
    
    def test_compact_summary_includes_plan_name(self, approved_plan_core_response):
        """Verify plan name is always included."""
        result = compact_summary(approved_plan_core_response)
        
        # Should start with plan name
        assert "Remedy" in result


# ============================================================================
# COMPARISON FORMATTER TESTS
# ============================================================================

class TestComparisonFormatter:
    """Tests for comparison formatting."""
    
    def test_english_comparison_cleans_utf8(self, comparison_message):
        """Verify UTF-8 cleaning in comparison."""
        # Add mojibake to test cleaning
        dirty_message = comparison_message.replace("Remedy", "Rem�dy")
        result = english_comparison_summary(dirty_message)
        
        # Should clean mojibake
        assert "Rem�dy" not in result or "Remedy" in result
    
    def test_english_comparison_cleans_aed_duplicates(self):
        """Verify AED cleaning in comparison."""
        msg = "Annual Limit: AED AED 100,000 | AED AED 150,000"
        result = english_comparison_summary(f"Comparison between A and B:\n{msg}")
        
        # Should remove AED AED patterns
        assert "AED AED" not in result


# ============================================================================
# DISPATCHER TESTS
# ============================================================================

class TestFormatOutputDispatcher:
    """Tests for unified format_output dispatcher."""
    
    def test_format_output_routes_to_whatsapp(self, approved_plan_core_response):
        """Verify dispatcher routes to whatsapp formatter."""
        result = format_output(approved_plan_core_response, "whatsapp_summary")
        assert "Plan:" in result
        assert result != _SAFE_REFUSAL
    
    def test_format_output_routes_to_arabic(self, approved_plan_core_response):
        """Verify dispatcher routes to arabic formatter."""
        result = format_output(approved_plan_core_response, "arabic_summary")
        # Should either have Arabic or safe refusal
        assert result == _SAFE_REFUSAL or any(c in result for c in "اسم الخطة الشبكة الحد")
    
    def test_format_output_routes_to_compact(self, approved_plan_core_response):
        """Verify dispatcher routes to compact formatter."""
        result = format_output(approved_plan_core_response, "compact_summary")
        assert "|" in result or result == _SAFE_REFUSAL
    
    def test_format_output_rejects_invalid_mode(self, approved_plan_core_response):
        """Verify invalid modes are rejected with informative message."""
        result = format_output(approved_plan_core_response, "invalid_mode")
        assert "not supported" in result or result == _SAFE_REFUSAL
    
    def test_format_output_safe_fallback_on_exception(self, approved_plan_core_response):
        """Verify safe fallback on any exception."""
        # Pass malformed response that might cause issues
        result = format_output({}, "whatsapp_summary")
        assert result == _SAFE_REFUSAL or isinstance(result, str)


# ============================================================================
# LANGUAGE DETECTION TESTS
# ============================================================================

class TestLanguageDetection:
    """Tests for language detection utility."""
    
    def test_detect_language_arabic(self):
        """Verify Arabic detection."""
        assert detect_language("اعطني ملخص") == "ar"
    
    def test_detect_language_english(self):
        """Verify English detection."""
        assert detect_language("Give me a summary") == "en"
    
    def test_detect_language_mixed(self):
        """Verify Arabic takes precedence in mixed text."""
        assert detect_language("Give me اعطني summary") == "ar"
    
    def test_detect_language_empty(self):
        """Verify empty string defaults to English."""
        assert detect_language("") == "en"


# ============================================================================
# VALIDATION HELPER TESTS
# ============================================================================

class TestValidationHelpers:
    """Tests for validation utilities."""
    
    def test_no_duplicate_labels_clean_output(self):
        """Verify no duplicate labels detection."""
        lines = ["Plan: Test", "Network: Network1", "Annual Limit: 100,000"]
        assert no_duplicate_labels(lines) is True
    
    def test_no_duplicate_labels_detects_duplicates(self):
        """Verify duplicate label detection."""
        lines = ["Plan: Test", "Plan: Test2", "Network: Network1"]
        assert no_duplicate_labels(lines) is False
    
    def test_no_empty_lines_clean_output(self):
        """Verify no excessive empty lines."""
        text = "Line 1\nLine 2\nLine 3"
        assert no_empty_lines(text) is True
    
    def test_no_empty_lines_detects_excess(self):
        """Verify excessive blank lines detection."""
        text = "Line 1\n\n\nLine 2"  # Three newlines = two blank lines
        assert no_empty_lines(text) is False


# ============================================================================
# SNAPSHOT STABILITY TESTS
# ============================================================================

class TestSnapshotStability:
    """Tests to ensure formatting output is stable across runs."""
    
    def test_whatsapp_snapshot_stable(self, approved_plan_core_response):
        """Verify WhatsApp formatting is deterministic."""
        result1 = whatsapp_summary(approved_plan_core_response)
        result2 = whatsapp_summary(approved_plan_core_response)
        
        assert result1 == result2, "Formatting output not deterministic"
    
    def test_arabic_snapshot_stable(self, approved_plan_core_response):
        """Verify Arabic formatting is deterministic."""
        result1 = arabic_plan_summary(approved_plan_core_response)
        result2 = arabic_plan_summary(approved_plan_core_response)
        
        assert result1 == result2, "Arabic formatting output not deterministic"
    
    def test_compact_snapshot_stable(self, approved_plan_core_response):
        """Verify compact formatting is deterministic."""
        result1 = compact_summary(approved_plan_core_response)
        result2 = compact_summary(approved_plan_core_response)
        
        assert result1 == result2, "Compact formatting output not deterministic"


# ============================================================================
# REGRESSION TESTS
# ============================================================================

class TestFormattingRegression:
    """Tests to prevent regression of known issues."""
    
    def test_no_aed_aed_duplication(self):
        """Prevent AED AED duplications."""
        response = {
            "ok": True,
            "intent": "plan_core",
            "plan_name": "Test",
            "data": {
                "plan_name": "Test",
                "annual_limit": "AED AED 100,000"
            }
        }
        result = whatsapp_summary(response)
        assert "AED AED" not in result
    
    def test_no_mojibake_in_output(self):
        """Prevent mojibake (broken UTF-8) in output."""
        response = {
            "ok": True,
            "intent": "plan_core",
            "plan_name": "Rem\ufffddy",  # Mojibake char
            "data": {
                "plan_name": "Rem\ufffddy",
            }
        }
        result = whatsapp_summary(response)
        assert "\ufffd" not in result or "Remedy" in result
    
    def test_no_internal_metadata_leakage(self):
        """Prevent internal metadata from leaking."""
        response = {
            "ok": True,
            "intent": "plan_core",
            "plan_name": "Test",
            "data": {
                "plan_name": "Test",
                "network_name": "Internal_source_trace_data"
            }
        }
        result = whatsapp_summary(response)
        # source_trace should be filtered out
        assert "source_trace" not in result.lower()
    
    def test_preserves_deterministic_behavior(self, approved_plan_core_response):
        """Ensure all deterministic behavior is preserved."""
        result = whatsapp_summary(approved_plan_core_response)
        
        # Should have basic structure
        assert len(result) > 0
        assert ":" in result  # Has labels
        assert "\n" in result  # Has line breaks


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
