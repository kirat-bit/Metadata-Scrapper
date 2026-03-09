"""
exporter.py
-----------
Saves parsed paper metadata to CSV and JSON formats.
"""

import json
import csv
from pathlib import Path


def export_to_json(papers: list[dict], output_path: str = "output.json") -> None:
    """
    Save parsed papers to a JSON file.

    Args:
        papers:      List of parsed paper dictionaries
        output_path: Where to save the file (default: output.json)
    """

    path = Path(output_path)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=4, ensure_ascii=False)

    print(f"[exporter] Saved {len(papers)} papers to {path}")


def export_to_csv(papers: list[dict], output_path: str = "output.csv") -> None:
    """
    Save parsed papers to a CSV file.

    Args:
        papers:      List of parsed paper dictionaries
        output_path: Where to save the file (default: output.csv)
    """

    if not papers:
        print("[exporter] No papers to export.")
        return

    path = Path(output_path)

    # Flatten authors and keywords to strings for CSV
    rows = []
    for p in papers:
        rows.append({
            "pubmed_id":      p["pubmed_id"],
            "title":          p["title"],
            "authors":        ", ".join(p["authors"]),
            "journal":        p["journal"],
            "pub_date":       p["pub_date"],
            "keywords_found": ", ".join(p["keywords_found"]),
        })

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"[exporter] Saved {len(papers)} papers to {path}")