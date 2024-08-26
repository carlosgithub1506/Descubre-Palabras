import pygame
import time
import random
from constantes_pantalla import *
from Package_funciones.carga_de_jugadores import *
from Package_clases.clase_continuar import Continuar
from Package_clases.classe_interfaz import *

# clase juego contiene la funcionalidad central del juego recibe 2 lista por parametros retorna score de jugador
class Juego:
    def __init__(self, lista_palabras:list, matriz_posiciones:list)->None:
        self.interfaz = InterfazJuegos()
        self.configurar_pantalla()
        self.continuar = Continuar(self,self.pantalla)
        self.puntaje = 0
        self.boton_borrar_rect = ""
        self.boton_submit_rect = ""
        self.boton_shufle_rect = ""
        self.palabra_elegida = ""
        self.lista_palabras = lista_palabras
        self.bandera = True
        self.running = True
        self.flag = False
        self.lista_palabras_acertadas = []
        self.pos_x_acertadas = 50
        self.pos_y_acertadas = 500
        self.tiempo_inicio = time.time()
        self.tiempo_limite = 10
        self.contador_nuevo = 0
        self.matriz_posiciones_letra_burbujas = matriz_posiciones
        self.reset_estados_botones()
        self.texto_desordenado = None
        self.contador_partidas_jugadas = 0
        self.fuente_tiempo = pygame.font.SysFont("consolas", 50)

    def configurar_pantalla(self)->None:
        self.pantalla = self.interfaz.pantalla

    def desordenar_palabra(self, lista_palabras:list)->tuple:
        retorno = False
        if isinstance(lista_palabras, list) and len(lista_palabras) > 0:
            lista_elementos = random.choice(lista_palabras)
            retorno = self.desordenar_letras(lista_elementos)
        return retorno

    def desordenar_letras(self, lista:list)->tuple:
        lista_de_letras = list(lista[0])
        random.shuffle(lista_de_letras)
        cadena_desordenada = "".join(lista_de_letras)
        tupla = (cadena_desordenada, lista)
        return tupla

    def reset_estados_botones(self)->None:
        self.estado_botones = [False] * len(self.matriz_posiciones_letra_burbujas[0])
        self.posiciones_ocupadas = [None] * len(self.matriz_posiciones_letra_burbujas[0])
        self.letras_destino = [None] * len(self.matriz_posiciones_letra_burbujas[0])

    def obtener_palabra_formada(self)->None:
        palabra_formada = ""
        for letra in self.letras_destino:
            if letra != None:
                palabra_formada += letra
            else:
                palabra_formada += ""
        self.palabra_elegida = palabra_formada

    def validar_palabra(self)->None:
        encontrada = False
        lista_palabras_validas = self.texto_desordenado[1]
        for palabras in lista_palabras_validas:
            if palabras == self.palabra_elegida:
                suma = lambda x,y : x + y
                encontrada = True
        if encontrada:
                cadena_guardada = False
                for i in self.lista_palabras_acertadas:
                    if  i == self.palabra_elegida:
                        cadena_guardada = True
                if cadena_guardada == False:
                    self.puntaje = suma(self.puntaje, len(self.palabra_elegida))
                    self.lista_palabras_acertadas.append(self.palabra_elegida)

    def actualizar_tiempo(self)->None:
        # Calcular el tiempo transcurrido desde el inicio del juego
        tiempo_transcurrido = time.time() - self.tiempo_inicio

        self.tiempo_restante = self.tiempo_limite - tiempo_transcurrido
    
        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0
        self.texto_tiempo = self.fuente_tiempo.render(f"{int(self.tiempo_restante)}", False, COLOR_ROJO)
        self.pantalla.blit(self.texto_tiempo,(575, 425))
        
        # Verificar si el tiempo se ha agotado completamente
        if self.tiempo_restante == 0 and self.contador_nuevo < 2:
            self.contador_nuevo +=1
            self.continuar.mostrar_popup_continuar()

    def nueva_partida(self)->None:
        self.tiempo_inicio = time.time()
        self.tiempo_limite = 90
        self.en_juego = True
        self.entrada_jugador = ""
        self.palabras_acertadas = []
        self.reset_estados_botones()
        self.tiempo_restante = self.tiempo_limite - (time.time() - self.tiempo_inicio)
        self.bandera = True
        self.lista_palabras_acertadas = []

    def seguir_jugando(self)->None:
        if self.tiempo_restante == 0:
        
                if self.contador_partidas_jugadas < 2:
                    continuar = self.continuar.mostrar_popup_continuar()
                    if continuar:
                        self.nueva_partida()
                        self.contador_partidas_jugadas += 1
                    else:
                        self.running = False
                else:
                    self.running = False
                                
    def capturar_eventos(self)->None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                posicion_click = evento.pos
                if self.boton_borrar_rect.collidepoint(posicion_click):
                    self.reset_estados_botones()
                elif self.boton_submit_rect.collidepoint(posicion_click):
                    if len(self.palabra_elegida) > 2:
                        self.validar_palabra()
                        self.reset_estados_botones()
                elif self.boton_shufle_rect.collidepoint(posicion_click):
                    lista = self.texto_desordenado[1]
                    self.texto_desordenado = self.desordenar_letras(lista)
                    self.reset_estados_botones()
                else:
                    self.capturar_click_burbujas(evento, posicion_click)

    def capturar_click_burbujas(self, evento:list,posicion_click:tuple)->None:
        for i, (pos_x, pos_y) in enumerate(self.matriz_posiciones_letra_burbujas[2]):
            boton_rect = pygame.Rect(pos_x, pos_y, 150, 150)
            if boton_rect.collidepoint(posicion_click):
                if self.estado_botones[i]:
                    self.estado_botones[i] = False
                    indice = self.posiciones_ocupadas.index(i)
                    self.posiciones_ocupadas[indice] = None
                    self.letras_destino[indice] = None
                else:
                    for j in range(len(self.posiciones_ocupadas)):
                        if self.posiciones_ocupadas[j] == None:
                            self.posiciones_ocupadas[j] = i
                            self.estado_botones[i] = True
                            self.letras_destino[j] = self.texto_desordenado[0][i]
                            break
                break
    print()
    def bucle_juego(self, lista:list)->None:
        while self.running:
            self.capturar_eventos()
            self.pantalla.fill(COLOR_NEGRO)
            self.pantalla.blit(self.interfaz.fondo_p_diseño, POSICION_FONDO)
            
            if self.bandera:
                self.texto_desordenado = self.desordenar_palabra(self.lista_palabras)
                self.bandera = False

            self.interfaz.mostrar_burbujas_botones(self.pantalla, self.interfaz.boton_huella, self.interfaz.boton, self.matriz_posiciones_letra_burbujas, self.estado_botones, self.posiciones_ocupadas)
            self.interfaz.mostrar_letras_burbujas(self.pantalla, self.texto_desordenado, self.matriz_posiciones_letra_burbujas, self.estado_botones, self.posiciones_ocupadas, self.interfaz.font_letras)
            self.boton_borrar_rect, self.boton_submit_rect, self.boton_shufle_rect = self.interfaz.mostrar_imagenes_estaticas(lista, self.pantalla, self.boton_borrar_rect, self.boton_submit_rect, self.boton_shufle_rect)
            self.obtener_palabra_formada()
            self.actualizar_tiempo()
            self.interfaz.actualizar_tiempo(self.pantalla, self.interfaz.fuente_tiempo, self.tiempo_restante)
            self.seguir_jugando()
            self.interfaz.mostrar_score_acertadas(self.pantalla, self.puntaje, self.interfaz.font_puntaje, self.interfaz.font_acertadas, self.lista_palabras_acertadas)
            pygame.display.flip()
