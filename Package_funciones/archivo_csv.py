

def csv_a_matriz(path:str)->list:
    matriz = []
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            for linea in archivo :
                listas = linea.strip().split(",")
                matriz.append(listas)
            return matriz
    except Exception as e:
        print(f"Error al leer archivo csv: {e}")


def guardar_matriz_a_csv(path:str,matriz:list[list])->None:
    try:
        with open( path, "w",encoding="utf-8" ) as archivo:
            for fila in matriz:
                lista_cadenas = []
                for elemento in fila:
                    lista_cadenas.append(str(elemento))
                linea = ",".join(lista_cadenas)
                archivo.write(f"{linea}\n")
    except Exception as e:
        print(f"Error al guardar archivo csv: {e}")
