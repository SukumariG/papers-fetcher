import requests  # For API requests
import pandas as pd  # For creating CSV files
from typing import List, Dict, Any  # For type hints


# Function to fetch PubMed IDs based on a query
def fetch_pubmed_ids(query: str, max_results: int = 20) -> List[str]:
    """
    Fetches PubMed IDs using the search query.

    Args:
        query (str): The search query for PubMed.
        max_results (int): Maximum number of results to fetch.

    Returns:
        List[str]: List of PubMed IDs.
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",       # Database to search
        "term": query,        # Search query (PubMed supports advanced queries)
        "retmode": "json",    # Return format as JSON
        "retmax": max_results, # Max number of results to return
    }

    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error for HTTP issues

        # Parse JSON response
        data = response.json()

        # Extract and return the list of PubMed IDs
        return data.get("esearchresult", {}).get("idlist", [])

    except requests.RequestException as e:
        print(f"Network error while fetching PubMed IDs: {e}")
        return []  # Return empty list on error
    except ValueError as e:
        print(f"Error parsing JSON response for PubMed IDs: {e}")
        return []


# Function to fetch details of papers using PubMed IDs
def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Fetches paper details from PubMed based on a list of PubMed IDs.

    Args:
        pubmed_ids (List[str]): List of PubMed IDs.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing paper details.
    """
    if not pubmed_ids:
        return []  # No IDs provided

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),  # Combine all IDs as a comma-separated string
        "retmode": "json",
    }

    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Parse JSON response
        data = response.json()

        papers = []
        for uid in pubmed_ids:
            paper_data = data.get("result", {}).get(uid, {})
            papers.append({
                "PubmedID": paper_data.get("uid"),
                "Title": paper_data.get("title"),
                "Publication Date": paper_data.get("pubdate"),
                # Placeholder fields for company detection (to implement later)
                "Non-academicAuthor(s)": "NA",
                "CompanyAffiliation(s)": "NA",
                "Corresponding Author Email": "NA",
            })

        return papers

    except requests.RequestException as e:
        print(f"Network error while fetching paper details: {e}")
        return []
    except ValueError as e:
        print(f"Error parsing JSON response for paper details: {e}")
        return []


# Function to save paper data into a CSV file
def save_to_csv(papers: List[Dict[str, Any]], filename: str) -> None:
    """
    Saves the fetched paper data to a CSV file.

    Args:
        papers (List[Dict[str, Any]]): List of paper details.
        filename (str): CSV file name to save the data.
    """
    try:
        df = pd.DataFrame(papers)  # Create a DataFrame from the data
        df.to_csv(filename, index=False)  # Save to CSV without row index
        print(f"Results saved successfully to {filename}")
    except Exception as e:
        print(f"Failed to save CSV file: {e}")
