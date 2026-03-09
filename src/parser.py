"""
parser.py
---------
Takes raw paper data fetched from PubMed and extracts
only the metadata fields relevant to genome assemblies.
"""

from typing import Optional

GENOME_KEYWORDS = [
    "genome", "assembly", "polyploid", "diploid", "ploidy",
    "chromosome", "annotation", "sequencing", "scaffold",
    "contig", "transcriptome", "metagenome"
]

def extract_authors(raw_authors: list[dict]) -> list[str]:
    authors = []
    for author in raw_authors:
        name = author.get("name", "").strip()
        if name:
            authors.append(name)
    return authors

def extract_keywords_found(text: str) -> list[str]:
    text_lower = text.lower()
    found = []
    for keyword in GENOME_KEYWORDS:
        if keyword in text_lower:
            found.append(keyword)
    return found

def parse_paper(raw_paper: dict) -> Optional[dict]:
    if not raw_paper:
        return None
    title = raw_paper.get("title", "No title available").strip()
    pub_date = raw_paper.get("pubdate", "Unknown date").strip()
    journal = raw_paper.get("fulljournalname", "Unknown journal").strip()
    raw_authors = raw_paper.get("authors", [])
    authors = extract_authors(raw_authors)
    pubmed_id = raw_paper.get("uid", "Unknown ID").strip()
    keywords_found = extract_keywords_found(title)
    parsed = {
        "pubmed_id":      pubmed_id,
        "title":          title,
        "authors":        authors,
        "journal":        journal,
        "pub_date":       pub_date,
        "keywords_found": keywords_found,
    }
    return parsed

def parse_multiple_papers(raw_papers: list[dict]) -> list[dict]:
    parsed_papers = []
    for raw in raw_papers:
        parsed = parse_paper(raw)
        if parsed:
            parsed_papers.append(parsed)
    print(f"[parser] Successfully parsed {len(parsed_papers)} papers")
    return parsed_papers