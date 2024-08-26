from Package_clases.clase_juego import *
from Package_clases.clase_inicio import *
from Package_clases.clase_continuar import *
from Package_clases.clase_final import *
from constantes_pantalla import *
from Package_funciones.archivo_csv import *
from Package_funciones.archivo_json import *
import pygame

# funcion que ejecuta las clase de inicio, juego y final recibe 6 parametros
def juego_palabras(path_1:str, path_2:str, list_img_ini:list, lista_img_jue:list, matriz_posiciones:list, lista_final:list)->None:

    lista = csv_a_matriz(path_1)
    lista_jugadores = cargar_lista_desde_json(path_2)
    inicio = Inicio()
    pantalla_actual = "inicio"

    while True:
        if pantalla_actual == "inicio":
            pantalla_actual = inicio.bucle_pantalla_inicio(list_img_ini)
            if pantalla_actual == "juego":
                nickname = inicio.nickname
                juego = Juego(lista, matriz_posiciones)

        elif pantalla_actual == "juego":
            juego.bucle_juego(lista_img_jue)
            if juego.running == False:
                puntuacion = juego.puntaje
                lista_jugadores = cargar_jugadores(lista_jugadores, nickname, puntuacion)
                guardar_lista_en_json(lista_jugadores, path_2)
                pantalla_actual = "final"

        elif pantalla_actual == "final":
            pantalla_final = PantallaFinal()
            pantalla_final.bucle_pantalla_final(lista_final)
            guardar_matriz_a_csv("matriz_palabra.csv",lista)

            pantalla_actual = "fin"
            break
    pygame.quit()
juego_palabras("matriz_palabra.csv",'lista_jugadores.json',list_imagenes_inicio, list_imagenes_juegos, matriz_posiciones_burbujas_letras,list_imagenes_final)


