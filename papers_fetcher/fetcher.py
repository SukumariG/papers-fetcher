import requests
import xml.etree.ElementTree as ET

def fetch_and_process_papers(query, max_results=20, debug=False):
    ids = fetch_pubmed_ids(query, max_results)
    if debug:
        print(f"Fetched IDs: {ids}")

    papers = fetch_paper_details(ids, debug=debug)
    return papers

def fetch_pubmed_ids(query, max_results):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(ids, debug=False):
    if not ids:
        return []

    ids_str = ",".join(ids)
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ids_str,
        "retmode": "xml"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    papers = []
    for article in root.findall(".//PubmedArticle"):
        paper = {}
        medline = article.find("MedlineCitation")
        article_info = medline.find("Article")
        paper["PubmedID"] = medline.findtext("PMID")
        paper["Title"] = article_info.findtext("ArticleTitle")
        paper["Publication Date"] = extract_pub_date(article_info)
        paper["Non-academic Author(s)"], paper["Company Affiliation(s)"] = extract_authors(article_info, debug)
        paper["Corresponding Author Email"] = extract_email(article_info)
        papers.append(paper)
    return papers

def extract_pub_date(article_info):
    journal = article_info.find("Journal/JournalIssue/PubDate")
    year = journal.findtext("Year")
    month = journal.findtext("Month")
    day = journal.findtext("Day")
    return f"{year or ''}-{month or ''}-{day or ''}".strip("-")

def extract_authors(article_info, debug=False):
    non_academic_authors = []
    company_affiliations = []
    for author in article_info.findall("AuthorList/Author"):
        affiliations = [aff.text for aff in author.findall("AffiliationInfo/Affiliation") if aff.text]
        name = f"{author.findtext('ForeName', '')} {author.findtext('LastName', '')}".strip()
        for aff in affiliations:
            if any(keyword in aff.lower() for keyword in ["pharma", "biotech", "therapeutics", "laboratories", "inc.", "corp", "company", "ltd"]):
                company_affiliations.append(aff)
                non_academic_authors.append(name)
    return "; ".join(non_academic_authors), "; ".join(company_affiliations)

def extract_email(article_info):
    for affiliation in article_info.findall(".//AffiliationInfo/Affiliation"):
        text = affiliation.text or ""
        if "@" in text:
            return text.split()[-1]  # crude email extraction
    return ""
