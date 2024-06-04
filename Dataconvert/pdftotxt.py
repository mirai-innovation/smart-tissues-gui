import os
import PyPDF2

def pdf_a_txt(pdf_path, txt_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            lector_pdf = PyPDF2.PdfFileReader(pdf_file)
            texto_completo = ''
            for num_pagina in range(lector_pdf.getNumPages()):
                pagina = lector_pdf.getPage(num_pagina)
                texto_completo += pagina.extractText()

        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(texto_completo)
        print(f'Archivo {pdf_path} convertido a {txt_path}')
    except Exception as e:
        print(f'Error al procesar {pdf_path}: {e}')

def convertir_pdfs_en_carpeta(carpeta_pdf, carpeta_txt):
    if not os.path.exists(carpeta_txt):
        os.makedirs(carpeta_txt)

    for nombre_archivo in os.listdir(carpeta_pdf):
        if nombre_archivo.lower().endswith('.pdf'):
            ruta_pdf = os.path.join(carpeta_pdf, nombre_archivo)
            nombre_txt = os.path.splitext(nombre_archivo)[0] + '.txt'
            ruta_txt = os.path.join(carpeta_txt, nombre_txt)
            pdf_a_txt(ruta_pdf, ruta_txt)

# Ruta de la carpeta que contiene los PDFs
carpeta_pdf = 'Dataconvert\\DataPDF'

# Ruta de la carpeta donde se guardarán los archivos TXT
carpeta_txt = 'Dataconvert\\filestxt'

convertir_pdfs_en_carpeta(carpeta_pdf, carpeta_txt)
