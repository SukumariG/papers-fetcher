import typer
from .fetcher import fetch_and_process_papers

app = typer.Typer(add_completion=False)

@app.command()
def fetch(
    query: str = typer.Argument(..., help="Search query for PubMed"),
    file: str = typer.Option(None, "--file", "-f", help="Filename to save the results (CSV)"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode"),
    max_results: int = typer.Option(20, "--max-results", "-m", help="Maximum number of results to fetch"),
):
    """
    Fetch PubMed papers based on the query.
    """
    papers = fetch_and_process_papers(query, max_results=max_results, debug=debug)

    if not papers:
        typer.echo("No papers found.")
        return

    if file:
        import pandas as pd
        pd.DataFrame(papers).to_csv(file, index=False)
        typer.echo(f"Saved {len(papers)} papers to '{file}'.")
    else:
        for paper in papers:
            typer.echo(paper)

if __name__ == "__main__":
    app()
