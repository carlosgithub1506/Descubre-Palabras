import pygame
from constantes_pantalla import *


# clase interfaz configura los graficos y muestra las imagenes de la clase juego
class InterfazJuegos:
    def __init__(self):
        pygame.init()
        self.configurar_pantalla()
        
    def configurar_pantalla(self)->None:
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("DESCUBRE PALABRAS")
        self.fondo_p_diseño = pygame.image.load("imagenes\\fondo.png").convert()
        self.fondo_p_diseño = pygame.transform.scale(self.fondo_p_diseño, (ANCHO_VENTANA, ALTO_VENTANA))
        self.icono = pygame.image.load('imagenes\\logo.png')
        pygame.display.set_icon(self.icono)
        self.boton = pygame.image.load('imagenes\\burbuja_fucsia.png')
        self.boton = pygame.transform.scale(self.boton, (151, 151))
        self.boton_huella = pygame.image.load('imagenes\\Huella.png')
        self.boton_huella = pygame.transform.scale(self.boton_huella, (149, 149))
        self.fuente_tiempo = pygame.font.SysFont("consolas", 50)
        self.font_letras = pygame.font.SysFont(None, TAMAÑO_LETRAS_BURBUJAS)
        self.font_puntaje = pygame.font.SysFont(None, TAMAÑO_SCORE)
        self.font_acertadas = pygame.font.SysFont(None, TAMAÑO_ACERTADA)
        self.fuente_tiempo = pygame.font.SysFont("consolas", 50)

    def mostrar_imagenes_estaticas(self, lista:list, pantalla, boton_borrar_rect:str, boton_submit_rect:str, boton_shufle_rect:str)->str:
        contador = 0
        for elemento in lista:
            imagen = pygame.image.load(elemento[0])
            imagen = pygame.transform.scale(imagen, elemento[1])
            imagen_rect = imagen.get_rect(topleft=elemento[2])
            pantalla.blit(imagen, imagen_rect)
            if contador == 1:
                boton_borrar_rect = imagen_rect
            elif contador == 2:
                boton_submit_rect = imagen_rect
            elif contador == 3:
                boton_shufle_rect = imagen_rect
            contador += 1
        return boton_borrar_rect, boton_submit_rect, boton_shufle_rect

    def mostrar_burbujas_botones(self, pantalla, boton_huella, boton, matriz_posiciones_letra_burbujas, estado_botones, posiciones_ocupadas)->None:
        for i in range(len(matriz_posiciones_letra_burbujas[2])):
            if estado_botones[i]:
                indice = posiciones_ocupadas.index(i)
                nueva_pos = matriz_posiciones_letra_burbujas[3][indice]
            else:
                nueva_pos = matriz_posiciones_letra_burbujas[2][i]
            pantalla.blit(boton_huella, matriz_posiciones_letra_burbujas[2][i])
            pantalla.blit(boton_huella, matriz_posiciones_letra_burbujas[3][i])
            pantalla.blit(boton, nueva_pos)

    def mostrar_letras_burbujas(self, pantalla, texto_desordenado, matriz_posiciones_letra_burbujas, estado_botones, posiciones_ocupadas, font_letras):
        if isinstance(texto_desordenado, tuple) and len(texto_desordenado) > 0:
            palabra, _ = texto_desordenado
            for i, caracter in enumerate(palabra):
                if i < len(matriz_posiciones_letra_burbujas[1]):
                    superficie_letra = font_letras.render(caracter, True, (255, 0, 0))
                    if estado_botones[i]:
                        posicion = posiciones_ocupadas.index(i)
                        nueva_pos_letras = matriz_posiciones_letra_burbujas[1][posicion]
                    else:
                        nueva_pos_letras =  matriz_posiciones_letra_burbujas[0][i]
                    pantalla.blit(superficie_letra, nueva_pos_letras)

    def actualizar_tiempo(self, pantalla, fuente_tiempo, tiempo_restante):
        texto_tiempo = fuente_tiempo.render(f"{int(tiempo_restante)}", False, COLOR_ROJO)
        pantalla.blit(texto_tiempo, (575, 425))

    def mostrar_score_acertadas(self, pantalla, puntaje, font_puntaje, font_acertadas, lista_palabras_acertadas):
        score_text = font_puntaje.render(f"{puntaje}", True, COLOR_AMARILLO)
        pantalla.blit(score_text, (180, 450))
        pos_x_acertadas = 40
        pos_y_acertadas = 520
        if len(lista_palabras_acertadas) > 0:
            for string in lista_palabras_acertadas:
                texto = font_acertadas.render(f"{string}", True, COLOR_AMARILLO)
                pantalla.blit(texto, (pos_x_acertadas, pos_y_acertadas))
                pos_x_acertadas += 100
                if pos_x_acertadas + texto.get_width() > pantalla.get_width() - 10:
                    pos_x_acertadas = 30
                    pos_y_acertadas += 60