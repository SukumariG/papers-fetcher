# # Papers Fetcher: A CLI Tool for Fetching Research Papers from PubMed

This repository contains the **Papers Fetcher** project, a command-line tool that retrieves research papers from PubMed using their API.  
It extracts key metadata from papers and identifies non-academic authors and pharmaceutical affiliations using simple heuristics.

This project demonstrates practical applications of API integration, command-line interface (CLI) development, and data processing.

## Overview

Researchers often need quick access to structured research paper data, especially from sources like PubMed.  
This tool enables fetching papers based on specific queries, exporting the results to a CSV file for easy analysis.

Key features:
- Supports advanced PubMed queries.
- Extracts paper details such as:
  - PubMed ID
  - Title
  - Publication Date
  - Non-academic authors
  - Company affiliations
  - Corresponding author email
- CSV export or console output options.
- Debug mode for detailed logs during execution.

## Repository Structure


papers-fetcher/
│
├── papers_fetcher/ # Python package (main code)
│ ├── init.py # Package initializer
│ ├── cli.py # Command-line interface script
│ └── fetcher.py # Core logic for fetching and saving papers
│
├── pyproject.toml # Poetry project configuration
├── README.md # Project documentation (this file)
└── results.csv # Sample output file (optional; generated after running)
```


## Installation

Clone the repository and install dependencies using Poetry:

```bash
git clone https://github.com/SukumariG/papers-fetcher.git
cd papers-fetcher
poetry install


## Command-Line Options

| Option                   | Shorthand | Description                                                       | Required |
|--------------------------|-----------|-------------------------------------------------------------------|----------|
| `--query`                | *(none)*  | PubMed search query to fetch papers.                              |   Yes   |
| `--file`                 | `-f`      | CSV filename to save results. If not provided, prints to console. | No       |
| `--max-results`          | `-m`      | Maximum number of papers to retrieve (default: 20).               | No       |
| `--debug`                | `-d`      | Enable debug logs for detailed tracing.                           | No       |
| `--help`                 | `-h`      | Show help message and exit.                                       | No       |

---

 ### Example Usage:
```bash
poetry run python -m papers_fetcher.cli \
  --query "machine learning in healthcare" \
  --file results.csv \
  --max-results 10 \
  --debug


## Project Motivation
This tool was created to explore automated research data collection, particularly for life sciences and healthcare fields.
It combines API interactions, data processing, and command-line scripting to provide a practical and reusable solution.