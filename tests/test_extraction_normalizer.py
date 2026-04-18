"""Tests for src.normalizers.extraction_normalizer."""

from src.normalizers.extraction_normalizer import normalize_extraction


def _base_payload(**overrides) -> dict:
    """Minimal valid payload with optional overrides."""
    data = {
        "schema_version": "1.0",
        "source_filename": "test.docx",
        "source_path": "/tmp/test.docx",
        "paragraph_count": 0,
        "table_count": 0,
        "paragraphs": [],
        "tables": [],
    }
    data.update(overrides)
    return data


# --- paragraph normalization ---


def test_strips_paragraph_whitespace():
    data = _base_payload(paragraphs=["  hello  ", "\tworld\t"], paragraph_count=2)
    result = normalize_extraction(data)
    assert result["paragraphs"] == ["hello", "world"]


def test_collapses_internal_spaces():
    data = _base_payload(paragraphs=["too   many   spaces"], paragraph_count=1)
    result = normalize_extraction(data)
    assert result["paragraphs"] == ["too many spaces"]


def test_collapses_internal_tabs():
    data = _base_payload(paragraphs=["tab\t\there"], paragraph_count=1)
    result = normalize_extraction(data)
    assert result["paragraphs"] == ["tab here"]


def test_drops_empty_paragraphs():
    data = _base_payload(paragraphs=["keep", "  ", "", "also keep"], paragraph_count=4)
    result = normalize_extraction(data)
    assert result["paragraphs"] == ["keep", "also keep"]
    assert result["paragraph_count"] == 2


def test_drops_whitespace_only_paragraphs():
    data = _base_payload(paragraphs=["\t  \t"], paragraph_count=1)
    result = normalize_extraction(data)
    assert result["paragraphs"] == []
    assert result["paragraph_count"] == 0


# --- table normalization ---


def test_strips_cell_whitespace():
    data = _base_payload(
        tables=[[[" A1 ", "B1\t"], ["\tA2", " B2 "]]],
        table_count=1,
    )
    result = normalize_extraction(data)
    assert result["tables"] == [
        [["A1", "B1"], ["A2", "B2"]],
    ]


def test_collapses_cell_internal_spaces():
    data = _base_payload(
        tables=[[["lots   of   space"]]],
        table_count=1,
    )
    result = normalize_extraction(data)
    assert result["tables"][0][0][0] == "lots of space"


def test_drops_empty_table_rows():
    data = _base_payload(
        tables=[[["A1", "B1"], ["", ""], ["A3", "B3"]]],
        table_count=1,
    )
    result = normalize_extraction(data)
    assert result["tables"] == [[["A1", "B1"], ["A3", "B3"]]]


def test_drops_whitespace_only_rows():
    data = _base_payload(
        tables=[[["  ", "\t"]]],
        table_count=1,
    )
    result = normalize_extraction(data)
    assert result["tables"] == []
    assert result["table_count"] == 0


def test_drops_table_that_becomes_empty():
    data = _base_payload(
        tables=[[["", ""]], [["valid"]]],
        table_count=2,
    )
    result = normalize_extraction(data)
    assert result["tables"] == [[["valid"]]]
    assert result["table_count"] == 1


# --- count recomputation ---


def test_counts_recomputed_after_normalization():
    data = _base_payload(
        paragraphs=["keep", "  ", "also"],
        tables=[[["", ""]], [["ok"]]],
        paragraph_count=3,
        table_count=2,
    )
    result = normalize_extraction(data)
    assert result["paragraph_count"] == 2
    assert result["table_count"] == 1


# --- passthrough of non-content fields ---


def test_non_content_fields_unchanged():
    data = _base_payload(paragraphs=["hello"], paragraph_count=1)
    result = normalize_extraction(data)
    assert result["schema_version"] == "1.0"
    assert result["source_filename"] == "test.docx"
    assert result["source_path"] == "/tmp/test.docx"


# --- already-clean data ---


def test_clean_data_passes_through():
    data = _base_payload(
        paragraphs=["First paragraph.", "Second paragraph."],
        tables=[[["A1", "B1"], ["A2", "B2"]]],
        paragraph_count=2,
        table_count=1,
    )
    result = normalize_extraction(data)
    assert result["paragraphs"] == ["First paragraph.", "Second paragraph."]
    assert result["tables"] == [[["A1", "B1"], ["A2", "B2"]]]
    assert result["paragraph_count"] == 2
    assert result["table_count"] == 1
