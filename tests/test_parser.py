"""
test_parser.py
--------------
Unit tests for parser.py functions.
Run with: pytest
"""

import pytest
from src.parser import extract_authors, extract_keywords_found, parse_paper


# ── extract_authors ───────────────────────────────────────────────

def test_extract_authors_normal():
    """Should return a clean list of author names."""
    raw = [{"name": "Smith J"}, {"name": "Jones A"}]
    result = extract_authors(raw)
    assert result == ["Smith J", "Jones A"]


def test_extract_authors_empty():
    """Should return empty list if no authors provided."""
    result = extract_authors([])
    assert result == []


def test_extract_authors_missing_name():
    """Should skip authors with no name field."""
    raw = [{"name": ""}, {"name": "Jones A"}]
    result = extract_authors(raw)
    assert result == ["Jones A"]


# ── extract_keywords_found ────────────────────────────────────────

def test_keywords_found_in_title():
    """Should detect genome keywords in a title."""
    title = "Chromosome-level genome assembly of a diploid plant"
    result = extract_keywords_found(title)
    assert "genome" in result
    assert "assembly" in result
    assert "chromosome" in result
    assert "diploid" in result


def test_keywords_not_found():
    """Should return empty list if no keywords match."""
    title = "A study of weather patterns in North America"
    result = extract_keywords_found(title)
    assert result == []


def test_keywords_case_insensitive():
    """Should detect keywords regardless of capitalisation."""
    title = "GENOME ASSEMBLY OF A NEW SPECIES"
    result = extract_keywords_found(title)
    assert "genome" in result
    assert "assembly" in result


# ── parse_paper ───────────────────────────────────────────────────

def test_parse_paper_normal():
    """Should return a clean dict with all expected fields."""
    raw = {
        "uid":              "12345",
        "title":            "Chromosome-level genome assembly of a plant",
        "pubdate":          "2026 Mar 1",
        "fulljournalname":  "Scientific Data",
        "authors":          [{"name": "Smith J"}, {"name": "Jones A"}],
    }
    result = parse_paper(raw)
    assert result is not None
    assert result["pubmed_id"] == "12345"
    assert result["title"] == "Chromosome-level genome assembly of a plant"
    assert result["journal"] == "Scientific Data"
    assert result["pub_date"] == "2026 Mar 1"
    assert "Smith J" in result["authors"]
    assert "genome" in result["keywords_found"]


def test_parse_paper_empty():
    """Should return None for empty input."""
    result = parse_paper({})
    assert result is None


def test_parse_paper_missing_fields():
    """Should handle missing fields gracefully with defaults."""
    raw = {"uid": "99999"}
    result = parse_paper(raw)
    assert result is not None
    assert result["title"] == "No title available"
    assert result["journal"] == "Unknown journal"
    assert result["pub_date"] == "Unknown date"
    assert result["authors"] == []