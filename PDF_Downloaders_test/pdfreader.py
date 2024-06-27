import aspose.words as aw
# Import libraries
import requests
from bs4 import BeautifulSoup

# URL from which pdfs to be downloaded
url = "https://api-journal.accscience.com/journal/article/preview?doi=10.36922/ijb.2057"

# Requests URL and get response object
response = requests.get(url)

# Parse text obtained
soup = BeautifulSoup(response.text, 'html.parser')

# Find all hyperlinks present on webpage
links = soup.find_all('a')

i = 0

# From all links check for pdf link and
# if present download file
for link in links:
	if ('.pdf' in link.get('href', [])):
		i += 1
		print("Downloading file: ", i)

		# Get response object for link
		response = requests.get(link.get('href'))

		# Write content in pdf file
		pdf = open("pdf"+str(i)+".pdf", 'wb')
		pdf.write(response.content)
		pdf.close()
		print("File ", i, " downloaded")

print("All PDF files downloaded")


doc = aw.Document("Data\prueba1.pdf")
doc.save("Output1.txt")
i : int
with open('Output1.txt','r',encoding='cp932', errors='ignore') as file:
    # reading each line    
    for line in file:
    # reading each word        
        for word in line.split():
            # displaying the words 
            print("  :",word)