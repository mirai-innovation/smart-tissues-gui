from __future__ import unicode_literals, print_function
from spacy.lang.en import English # updated
import glob
import re
import os
import csv
import spacy 
import json


file_path = "lista_materiales.txt" # archivo txt donde se agregan todo los componentes conocidos, 
final= "Complete.txt"  #nombre del archivo donde se van a guardar las oracione separadas por sntsplit:
final_path = "extracted_sections" # carpeta donde se quiere guardar el archivo  final
folder_path = "Dataconvert\\filestxt" # Carpeta donde se encuentra los pdfs convertidos a txt

##Variables a buscar dentro de los papers
materialsandmethods = ["methods", "materials", "materials and methods" ,"Materials and Methods"] #No modicar,Crea banderas para no recolectar informacion antes de que se encuentre "Materials and methods en todos los papers"
units = ["w/v" , "g/ml", "mg/ml" , "gr/ml" , "wt" ] #Modiciar si desea agregar mas opciones de unidades de medida
cells =[ "cells/ml" , "cells per ml", " cells ml"]#NO modificar a menos que desee agregar mas formas en las que se escriban  celulas por millon de mil 
entities=[]
training_data =[]

nombre_archivo = 'datos.csv' #nombre del archivo donde se guardaran los datos en un csv, si desea cambiar el nombre conserver el ".csv"
txt_files = glob.glob(os.path.join(folder_path,"*.txt")) #No modificar
carpeta_save = 'Dataconvert\\txtpost' #ubicacion de la carpeta de donse se estan adquiriendo los txt
complete="" #variable goblar para guardar todas las oraciones en un txt separados por "sntsplit:"
pathmodel= "Modelv1" # IMPORTANTE UBICACION DE DONSE SE ESTA OBTENIENDO EL MODELO PARA PASAR LOS DATOS A UN CSV
ruta_meta_json = pathmodel + "\meta.json" #NO MODIFICAR si existe el modelo se obtiene el model.json para obtener el header de cada columna
json_output_file= "model\output.json" #Ubicacion y nombre donde se desea guardar el  archivo json para seguir entrenando el modelo


with open(ruta_meta_json, 'r', encoding='utf-8') as jsonner: # solo se esta obteniendo leyendo el archivo meta json como variable global em meta_data
    meta_data = json.load(jsonner)

def read_txt_to_list(file_path):
    # Leer el archivo y obtener una lista de líneas
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Quitar los saltos de línea de cada línea
    return lines


def listamat(): # esta funcion obtiene la lista de los componente que se conocen del archivo lista_materiales.txt (archivo que no se debe eliminar)
    lista = read_txt_to_list(file_path)
    elementos=[]
    with open(file_path, 'r', encoding='utf-8') as file:
        listademateriales = file.read().splitlines()
        for elemento in listademateriales:
            elementos.append(elemento.lower())
    return elementos


listaele= listamat() #guardamos los matariales en esta variable listaele

ner_labels = meta_data.get('labels', {}).get('ner') # se realiza la adquisicion de los headers de archivo meta.json
salto= "\n"
with open(nombre_archivo, 'w', newline='', encoding='utf-8') as csvfile: #creamos el archivo csv y cargamos los header del json y agregamos los header DOI y texto 
    csv_writer = csv.DictWriter(csvfile, fieldnames=['DOI'] + ner_labels + ['Texto'])
    csv_writer.writeheader()

for txt_file in txt_files:  # leemos todos los txt de la carpeta filestxt en Dataconvert 
                flag = 0 #declaramos las variables de las banderas si ya se encontro materiales y metodos
                flagner=1 
                output_file = txt_file.replace("Dataconvert\\filestxt\\", "") #eliminamos  "Dataconvert\\filestxt\\" del path de cada txt para obtener solo el nombre del archivo que analizamos
                modelner = spacy.load(pathmodel) #Cargamos el modelo que previamente entrenamos 
                texto_completo = '' #creamos una variable para guardar las oraciones 
                with open(txt_file, 'r', encoding='utf-8') as file: # abrimos el txt que vamos a anlizar 
                    contenido = file.read()
                    modified_content = contenido.replace('-\n', '') #eliminamos una  los saltos de linea que cortan las palabras por un -
                    modified_content = contenido.replace('\n', ' ') #eliminamos los saltos de linea para evitar tener muchos saltos de linea en una oracion 
                    nlp = English()  # *1
                    nlp.add_pipe('sentencizer')
                    doc = nlp(modified_content)
                    sentences = [sent.text.strip() for sent in doc.sents] #* 1 : hacemos particion de los oraciones  y la guardamos en una variable llamada sentences
                    print(txt_file, ": ")
                    
                    for i, oracion in enumerate(sentences, 1): #recorremos la variable sentences por cada oracion que contenga 
                            oracionlow=oracion.lower() # pasamos  la oracion que obtuvimos a minusculas
                            if ( flag==0):
                                    for met in materialsandmethods:
                                        count=0
                                        indice = oracionlow.find(met)
                                        if indice != -1:
                                            if indice < 5:
                                                if salto in oracionlow:
                                                    print("indice :", indice)
                                                    print(f'-----------------------------------------------------------------------------------------\n oracion {i} : "{met}" está en la oración :{oracionlow}')
                                                    print("==========================================================================================")
                                                    flag=1
                                                    break
                                            
                                            
                            if (flag == 1) : # flag == 1, si en el flag se detecta que su valor es 1 quiere decir que encontro alguna de las variantes de materials and methods
                                for elemento in listaele:
                                    for unit in units:
                                        if elemento and unit in oracionlow:
                                                #print(" elemento :", elemento ,"unidad : ", unit)
                                                print(f"oracion bioink {i} : {oracion}")
                                                texto_completo += "\n sntsplit:\n"
                                                texto_completo += oracion
                                                flagner=1   #segunda bandera para pasar la oracion por el modelo, la activamos a 1
                                        break
                                    break
                                
                            for cell in cells: # si en la oracio encontramos alguno de las variantes de celular per million , recorrem
                                if (len(oracion)>50):
                                    if cell in oracionlow:
                                        print(f"oracion  cell {i} : {oracion}")
                                        texto_completo += "\n sntsplit:\n"
                                        texto_completo += oracion
                                        flagner=1
                                break
                            
                            if(flagner==1):
                                #print("entro al if")
                                doc = modelner(oracionlow)
                                row = {'Texto': oracion ,'DOI': output_file}
                                print("doc ent" , doc.ents)
                                for ent in doc.ents: 
                                    if ent.label_ in ner_labels:
                                        print(ent.text, ent.label_)
                                        row[ent.label_] = ent.text
                                        entities.append((ent.start_char, ent.end_char, ent.label_))
                                if entities:
                                    training_data.append((oracionlow, {"entities": entities}))
                                    entities= []
                                with open(nombre_archivo, 'a', newline='', encoding='utf-8') as csvfile:
                                            csv_writer = csv.DictWriter(csvfile, fieldnames=['DOI'] + ner_labels + ['Texto'])
                                            csv_writer.writerow(row)        
                            flagner=0
                complete +=texto_completo          
                # Modifica el nombre del archivo de salida según sea necesario
                output_path = os.path.join(carpeta_save, output_file)  # Especifica la ruta de salida
                with open(output_path, 'w', encoding='utf-8') as outfile:
                    outfile.write(texto_completo)

# Modifica el nombre del archivo de salida según sea necesario
output_path = os.path.join(final_path, final)  # Especifica la ruta de salida
with open(output_path, 'w', encoding='utf-8') as outfile:
    outfile.write(complete)

#Salida del json
with open(json_output_file, 'w', encoding='utf-8') as jsonfile:
    json.dump(training_data, jsonfile, ensure_ascii=False, indent=4)
    