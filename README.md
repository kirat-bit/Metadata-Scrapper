# paper-metadata-scraper

A Python tool that searches PubMed's free API for biology research papers
and extracts structured genome-related metadata saving results to JSON and CSV.

Built as a demonstration of AI-assisted metadata extraction concepts,
relevant to EMBL-EBI's Ensembl genome loading pipeline work.

---

## What it does

- Searches PubMed for papers matching any query 
- Fetches full metadata for each paper 
- Scans titles for genome-related keywords 
- Exports clean structured results to JSON and CSV

---

## Project structure
```
paper-metadata-scraper/
├── src/
│   ├── fetcher.py     # Talks to the PubMed API and retrieves papers
│   ├── parser.py      # Extracts and structures relevant metadata fields
│   └── exporter.py    # Saves results to JSON and CSV
├── tests/
│   └── test_parser.py # Unit tests for parser functions
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.10+
---

## Setup
```bash

mkdir paper-metadata-scraper
 
cd paper-metadata-scraper

python -m venv venv

.\venv\Scripts\activate

source venv/bin/activate

pip install -r requirements.txt
```

---

## Usage

Run the full pipeline from the terminal:
```bash
python -c "
from src.fetcher import search_pubmed, fetch_multiple_papers
from src.parser import parse_multiple_papers
from src.exporter import export_to_json, export_to_csv

ids    = search_pubmed('plant genome assembly', 5)
raw    = fetch_multiple_papers(ids)
parsed = parse_multiple_papers(raw)

export_to_json(parsed)
export_to_csv(parsed)
"
```

This will create two output files in the project folder:
- `output.json` — structured metadata in JSON format
- `output.csv` — same data in spreadsheet-friendly CSV format

---

## Running tests

pytest tests/ -v
```

Expected output:
```
9 passed in 0.07s
```

---

## Example output
```json
[
    {
        "pubmed_id": "41792214",
        "title": "High quality chromosome-level genome assembly of Psammosilene tunicoides",
        "authors": ["Zhang Y", "Li H"],
        "journal": "Scientific data",
        "pub_date": "2026 Mar 6",
        "keywords_found": ["genome", "assembly", "chromosome"]
    }
]
```

---

## Relevance to bioinformatics

This project demonstrates core concepts behind metadata extraction from
biological literature — the same challenge addressed in genome loading
pipelines where assembly submissions are often missing key metadata fields
such as ploidy level that can only be found in the corresponding publication.

---

## Author

**Jaskirat Singh**
[LinkedIn](https://www.linkedin.com/in/jaskirat-singhkirat) |
[GitHub](https://github.com/kirat-bit)
