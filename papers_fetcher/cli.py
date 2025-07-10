import typer  # Typer helps in building beautiful CLI programs
from papers_fetcher.fetcher import (
    fetch_pubmed_ids,
    fetch_paper_details,
    save_to_csv
)  # Importing helper functions from fetcher.py module

app = typer.Typer()  # Initializing a Typer app instance


# Defining the 'get' subcommand for the CLI tool
@app.command()
def get(
    query: str = typer.Argument(..., help="PubMed search query"),  # Positional argument for the query
    file: str = typer.Option(None, "--file", "-f", help="Output CSV file (optional)"),  # Optional file path
    max_results: int = typer.Option(20, "--max-results", "-m", help="Maximum number of results to fetch"),  # Optional limit
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug output for troubleshooting")  # Optional debug flag
):
    """
    Fetch papers from PubMed based on the search query and optionally save the results to a CSV file.
    """

    # Debug info (prints extra info if debug mode is enabled)
    if debug:
        print(f"Search Query: {query}")
        print(f"Max Results: {max_results}")

    # Step 1: Fetch PubMed IDs based on query
    pubmed_ids = fetch_pubmed_ids(query, max_results)
    if debug:
        print(f"Fetched PubMed IDs: {pubmed_ids}")

    # Step 2: Fetch detailed information for each paper
    papers = fetch_paper_details(pubmed_ids)

    # Step 3: Save the result to a CSV file or print to console
    if file:
        save_to_csv(papers, file)
        print(f"Results saved to {file}")  # Notify that file has been saved
    else:
        for paper in papers:
            print(paper)  # Print each paper's info to console


# Entry point for running the CLI as a script
if __name__ == "__main__":
    app()
