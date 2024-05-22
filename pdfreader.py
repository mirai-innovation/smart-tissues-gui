from pypdf import PdfReader 

# creating a pdf reader object 
reader = PdfReader("Data\prueba2.pdf") 

# printing number of pages in pdf file 
print(len(reader.pages)) 

# getting a specific page from the pdf file 
page = reader.pages[9] 

# extracting text from page 
text = page.extract_text() 
print(text) 

print("---------------------------------")
import pdfplumber
import pandas as pd
table_settings = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text"
}
pdf = pdfplumber.open("Data\prueba2.pdf")
table=pdf.pages[0].extract_table(table_settings)
pd.DataFrame(table[1::],columns=table[0])
print(len(table))
print(table[1::])