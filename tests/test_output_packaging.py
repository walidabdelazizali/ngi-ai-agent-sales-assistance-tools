import pytest
from src.query import output_packaging

def test_format_plan_output_whatsapp_short_en():
    out = output_packaging.format_plan_output("Remedy 03", "whatsapp_short", language="en")
    assert "WhatsApp" in out and "Remedy 03" in out

def test_format_plan_output_whatsapp_short_ar():
    out = output_packaging.format_plan_output("Remedy 03", "whatsapp_short", language="ar")
    assert "ملخص واتساب" in out and ("Remedy 03" in out or "HN-REMEDY-3" in out)

def test_format_plan_output_client_summary_en():
    out = output_packaging.format_plan_output("Remedy 02", "client_summary", language="en")
    assert "Client summary" in out and "Remedy 02" in out

def test_format_plan_output_client_summary_ar():
    out = output_packaging.format_plan_output("Remedy 02", "client_summary", language="ar")
    assert "ملخص للعميل" in out and "Remedy 02" in out

def test_format_plan_output_executive_note_en():
    out = output_packaging.format_plan_output("Remedy 03", "executive_note", language="en")
    assert "Executive note" in out and "Remedy 03" in out

def test_format_plan_output_executive_note_ar():
    out = output_packaging.format_plan_output("Remedy 03", "executive_note", language="ar")
    assert "ملاحظة تنفيذية" in out and "Remedy 03" in out

def test_format_plan_output_bullet_summary_en():
    out = output_packaging.format_plan_output("Remedy 03", "bullet_summary", language="en")
    assert "- Plan Name:" in out and "- Plan Code:" in out

def test_format_plan_output_bullet_summary_ar():
    out = output_packaging.format_plan_output("Remedy 03", "bullet_summary", language="ar")
    assert "• اسم الخطة:" in out and "• رمز الخطة:" in out

def test_format_comparison_output_whatsapp_short_en():
    out = output_packaging.format_comparison_output("Remedy 02", "Remedy 03", "whatsapp_short", language="en")
    assert "WhatsApp comparison" in out

def test_format_comparison_output_whatsapp_short_ar():
    out = output_packaging.format_comparison_output("Remedy 02", "Remedy 03", "whatsapp_short", language="ar")
    assert "مقارنة واتساب" in out

def test_format_comparison_output_client_summary_en():
    out = output_packaging.format_comparison_output("Remedy 02", "Remedy 03", "client_summary", language="en")
    assert "Client comparison summary" in out

def test_format_comparison_output_client_summary_ar():
    out = output_packaging.format_comparison_output("Remedy 02", "Remedy 03", "client_summary", language="ar")
    assert "ملخص مقارنة للعميل" in out

def test_format_comparison_output_executive_note_en():
    out = output_packaging.format_comparison_output("Remedy 02", "Remedy 03", "executive_note", language="en")
    assert "Executive comparison note" in out

def test_format_comparison_output_executive_note_ar():
    out = output_packaging.format_comparison_output("Remedy 02", "Remedy 03", "executive_note", language="ar")
    assert "ملاحظة تنفيذية مقارنة" in out

def test_format_comparison_output_comparison_brief_en():
    out = output_packaging.format_comparison_output("Remedy 02", "Remedy 03", "comparison_brief", language="en")
    assert "Comparison brief" in out

def test_format_comparison_output_comparison_brief_ar():
    out = output_packaging.format_comparison_output("Remedy 02", "Remedy 03", "comparison_brief", language="ar")
    assert "مقارنة مختصرة" in out

def test_format_comparison_output_bullet_summary_en():
    out = output_packaging.format_comparison_output("Remedy 02", "Remedy 03", "bullet_summary", language="en")
    assert "-" in out

def test_format_comparison_output_bullet_summary_ar():
    out = output_packaging.format_comparison_output("Remedy 02", "Remedy 03", "bullet_summary", language="ar")
    assert "•" in out

def test_answer_packaged_query_english():
    out = output_packaging.answer_packaged_query("Give me a WhatsApp-ready summary for Remedy 03")
    assert "WhatsApp" in out
    out2 = output_packaging.answer_packaged_query("Create a short client-facing explanation for Remedy 02")
    assert "Client summary" in out2
    out3 = output_packaging.answer_packaged_query("Write an executive internal note comparing Remedy 02 vs Remedy 03")
    assert "Executive comparison note" in out3 or "No deterministic" in out3
    out4 = output_packaging.answer_packaged_query("Give me a comparison brief for Remedy 02 and Remedy 03")
    assert "Comparison brief" in out4 or "No deterministic" in out4

def test_answer_packaged_query_arabic():
    out = output_packaging.answer_packaged_query("اعطني ملخص واتساب لخطة Remedy 03")
    assert "ملخص واتساب" in out
    out2 = output_packaging.answer_packaged_query("اعطني شرح قصير للعميل عن Remedy 02")
    assert "ملخص للعميل" in out2
    out3 = output_packaging.answer_packaged_query("اكتب ملاحظة تنفيذية داخلية تقارن Remedy 02 و Remedy 03")
    assert "ملاحظة تنفيذية" in out3 or "عذراً" in out3
    out4 = output_packaging.answer_packaged_query("اعطني مقارنة مختصرة بين Remedy 02 و Remedy 03")
    assert "مقارنة مختصرة" in out4 or "عذراً" in out4

def test_packaging_fallback():
    out = output_packaging.format_plan_output("Remedy 03", "unsupported_format", language="en")
    assert "No deterministic" in out
    out2 = output_packaging.format_comparison_output("Remedy 02", "Remedy 03", "unsupported_format", language="ar")
    assert "عذراً" in out2
    out3 = output_packaging.answer_packaged_query("unsupported query")
    assert "No deterministic" in out3 or "عذراً" in out3

def test_no_replacement_char_in_outputs():
    out_en = output_packaging.format_plan_output("Remedy 03", "bullet_summary", language="en")
    out_ar = output_packaging.format_plan_output("Remedy 03", "bullet_summary", language="ar")
    assert "\uFFFD" not in out_en
    assert "\uFFFD" not in out_ar

def test_arabic_bullet_summary_labels():
    out_ar = output_packaging.format_plan_output("Remedy 03", "bullet_summary", language="ar")
    assert "اسم الخطة" in out_ar
    assert "رمز الخطة" in out_ar
    assert "الشبكة" in out_ar
    assert "الحد السنوي" in out_ar

def test_english_plan_name_no_mojibake():
    out_en = output_packaging.format_plan_output("Remedy 03", "bullet_summary", language="en")
    # Should not contain mojibake or replacement char
    assert "\uFFFD" not in out_en
    assert "Plan Name:" in out_en
