import requests

def download_pdf(doi, output_dir="pdfs"):
    headers = {
        "Accept": "application/pdf"
    }
    url = f"https://doi.org/{doi}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.headers['Content-Type'] == 'application/pdf':
        with open(f"{output_dir}/{doi.replace('/', '_')}.pdf", 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {doi}")
    else:
        print(f"Failed to download {doi}")

# Crear el directorio de salida si no existe
import os
os.makedirs("pdfs", exist_ok=True)

# Leer DOIs del archivo
with open("extracted_sections\dois.txt", "r") as f:
    dois = f.read().splitlines()

# Descargar cada PDF
for doi in dois:
    download_pdf(doi)
