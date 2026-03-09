"""
fetcher.py
----------
Fetches paper metadata from the PubMed API using a search term.
PubMed is a free public database of biology/biomedical research papers.
No API key required.
"""

import requests
from typing import Optional


# Base URLs for the PubMed API (completely free, no key needed)
PUBMED_SEARCH_URL  = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


def search_pubmed(query: str, max_results: int = 5) -> list[str]:
    """
    Search PubMed for papers matching a query string.

    Args:
        query:       The search term e.g. 'Arabidopsis genome assembly'
        max_results: How many paper IDs to return (default 5)

    Returns:
        A list of PubMed IDs (strings) matching the query
    """

    params = {
        "db":      "pubmed",    # which database to search
        "term":    query,       # our search term
        "retmax":  max_results, # max number of results
        "retmode": "json",      # we want the response in JSON format
    }

    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()  # raises an error if request failed

    data = response.json()
    ids  = data["esearchresult"]["idlist"]

    print(f"[fetcher] Found {len(ids)} papers for query: '{query}'")
    return ids


def fetch_paper_details(pubmed_id: str) -> Optional[dict]:
    """
    Fetch the full details of a single paper using its PubMed ID.

    Args:
        pubmed_id: A PubMed ID string e.g. '39771483'

    Returns:
        A dictionary containing the paper's metadata, or None if not found
    """

    params = {
        "db":      "pubmed",
        "id":      pubmed_id,
        "retmode": "json",
    }

    response = requests.get(PUBMED_SUMMARY_URL, params=params)
    response.raise_for_status()

    data   = response.json()
    result = data.get("result", {})
    paper  = result.get(pubmed_id)

    if not paper:
        print(f"[fetcher] No data found for PubMed ID: {pubmed_id}")
        return None

    return paper


def fetch_multiple_papers(pubmed_ids: list[str]) -> list[dict]:
    """
    Fetch details for a list of PubMed IDs.

    Args:
        pubmed_ids: List of PubMed ID strings

    Returns:
        List of paper metadata dictionaries
    """

    papers = []

    for pid in pubmed_ids:
        paper = fetch_paper_details(pid)
        if paper:
            papers.append(paper)

    print(f"[fetcher] Successfully fetched {len(papers)} papers")
    return papers