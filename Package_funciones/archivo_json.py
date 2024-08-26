import json

def guardar_lista_en_json(lista, path:str)->None:
   
    with open(path, 'w', encoding='utf-8') as archivo:
        json.dump(lista, archivo, ensure_ascii=False, indent=4)


def cargar_lista_desde_json(path:str)->list:

    with open(path, 'r', encoding='utf-8') as archivo:
        lista = json.load(archivo)
    return lista


# guardar_lista_en_json(lista_de_diccionarios, 'lista.json')

