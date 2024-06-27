import spacy
from spacy.training.example import Example
import random
import json
import os

path= "Modelv1" #Direccion de la carpeta del modelo si ya existe solo actualizara el modelo si no existe creara uno nuevo
file_path = 'model\data.json' #path para obtener los labels del modelo, todos los modelos lo tienen


def creating_model(new_data, iterations):
    # Crea un nuevo modelo si es que no existe en la direccion
    # Preparar los nuevos datos de entrenamiento
    NEW_TRAIN_DATA = new_data
    nlp = spacy.blank('en') 
    # Agregar etiquetas si es necesario
    if 'ner' not in nlp.pipe_names:
        ner = nlp.add_pipe('ner', last=True)
        
    for _, annotations in NEW_TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # Obtener nombres de otros pipes para deshabilitarlos durante el entrenamiento
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

    with nlp.disable_pipes(*other_pipes):  # Solo entrenar NER
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print(f"Starting iteration {itn}")
            random.shuffle(NEW_TRAIN_DATA)
            losses = {}
            for text, annotations in NEW_TRAIN_DATA:
                # Crear un objeto Example con el texto y las anotaciones
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                # Actualizar el modelo con el objeto Example
                nlp.update(
                    [example],  # Batch de ejemplos
                    drop=0.2,  # Dropout - hacer más difícil memorizar datos
                    sgd=optimizer,  # Callable para actualizar pesos
                    losses=losses
                )
            print(losses)
    return nlp

def continue_training(model_path, new_data, iterations):
    # Cargar el modelo existente
    nlp = spacy.load(model_path)

    # Preparar los nuevos datos de entrenamiento
    NEW_TRAIN_DATA = new_data

    # Agregar etiquetas si es necesario
    ner = nlp.get_pipe("ner")
    for _, annotations in NEW_TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # Obtener nombres de otros pipes para deshabilitarlos durante el entrenamiento
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

    with nlp.disable_pipes(*other_pipes):  # Solo entrenar NER
        optimizer = nlp.resume_training()
        for itn in range(iterations):
            print(f"Starting iteration {itn}")
            random.shuffle(NEW_TRAIN_DATA)
            losses = {}
            for text, annotations in NEW_TRAIN_DATA:
                # Crear un objeto Example con el texto y las anotaciones
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                # Actualizar el modelo con el objeto Example
                nlp.update(
                    [example],  # Batch de ejemplos
                    drop=0.3,  # Dropout - hacer más difícil memorizar datos
                    sgd=optimizer,  # Callable para actualizar pesos
                    losses=losses
                )
            print(losses)
    return nlp

def load_train_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Cargar los nuevos datos de entrenamiento desde el archivo JSON
NEW_TRAIN_DATA = load_train_data_from_json(file_path)
# Continuar el entrenamiento del modelo

#Comprueba en la direccion del la carpeta existe 
if os.path.isdir(path) == True:
    nlp = continue_training(path, NEW_TRAIN_DATA, 20)
    nlp.to_disk(path)
else:
    nlp = creating_model(NEW_TRAIN_DATA, 20)
    modelfile = input("Enter your Model Name: ")
    nlp.to_disk(path)