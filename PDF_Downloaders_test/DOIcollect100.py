import requests
from Bio import Entrez
import pandas as pd

# Configura tu correo electrónico para usar la API de PubMed
Entrez.email = "juarezkevin8@gmail.com"

def search_pubmed(query, max_results=1000):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record['IdList']

def fetch_article_details(pmids):
    ids = ",".join(pmids)
    handle = Entrez.esummary(db="pubmed", id=ids)
    summaries = Entrez.read(handle)
    handle.close()
    return summaries

def get_dois(summaries):
    dois = []
    for article in summaries['DocSum']:
        for item in article['Item']:
            if item.attributes['Name'] == 'ELocationID' and item.attributes['Type'] == 'doi':
                dois.append(item.title)
    return dois

def save_dois_to_csv(dois, filename="dois.csv"):
    df = pd.DataFrame(dois, columns=["DOI"])
    df.to_csv(filename, index=False)
    print(f"Guardado {len(dois)} DOIs en {filename}")

def main(query, max_results=1000):
    pmids = search_pubmed(query, max_results)
    summaries = fetch_article_details(pmids)
    dois = get_dois(summaries)
    save_dois_to_csv(dois)

if __name__ == "__main__":
    query = "bioprinting"
    main(query, max_results=1000)
