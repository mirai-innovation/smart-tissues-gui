import re
import os
import glob

# Carpeta que contiene los archivos .txt
folder_path = "Dataconvert\\filestxt"

# Especificar la ruta del archivo
file_path = "lista_materiales.txt"

# Usar glob para encontrar todos los archivos .txt en la carpeta
txt_files = glob.glob(os.path.join(folder_path,"*.txt"))

lista=[]
materiales= []
DOIlineas= []

def leer_y_dividir_oraciones(ruta_archivo):
    
    lista = read_txt_to_list(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Quitar los saltos de línea de cada línea
    lines = [line.strip() for line in lines]
    if not txt_files:
        print(f"No se encontraron archivos .txt en la carpeta {folder_path}")
    else:
        # Iterar sobre la lista de archivos .txt y leer su contenido
        for txt_file in txt_files:
            with open(txt_file, 'r', encoding='utf-8') as file:
                contenido = file.read()
                # Usar expresión regular para dividir las oraciones por puntos no precedidos o seguidos de un número
                modified_content = contenido.replace('\n', ' ')
                patron = re.compile(r'(?<!\d)\.(?!\d)')
                oraciones = patron.split(modified_content)
                
                # Limpia las oraciones y elimina las que están vacías después de la limpieza
                oraciones_limpias = [oracion.strip() for oracion in oraciones if oracion.strip()]
                #print( txt_file ,oraciones_limpias)
                Filesent= {
                    txt_file:
                    {
                        "Sentences":oraciones_limpias
                    }
                    }
            DOIlineas.append(Filesent)
            print(Filesent)
    return oraciones_limpias



def read_txt_to_list(file_path):
    # Leer el archivo y obtener una lista de líneas
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Quitar los saltos de línea de cada línea
    return lines


# Ruta del archivo de texto
# Obtener las oraciones
oraciones = leer_y_dividir_oraciones(txt_files)

# Imprimir las oraciones para verificar el resultado
for i, oracion in enumerate(oraciones, 1):
    #print(f"Oración {i}: {oracion}")
    #for lista_materiales in oracion:
        #if(lista_materiales== oracion):
            materiales.append(oracion)
    
##for i, pri in  enumerate(materiales, 1):
  #  print(f"Oración {i}: {pri}")
