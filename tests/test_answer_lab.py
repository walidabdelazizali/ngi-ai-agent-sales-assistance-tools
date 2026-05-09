from scripts.run_answer_lab import QUERIES


def test_answer_lab_includes_classic2r_queries():
    assert "Summarize Classic 2R" in QUERIES
    assert "classic2r limit" in QUERIES
    assert "شبكة كلاسيك 2R" in QUERIES
