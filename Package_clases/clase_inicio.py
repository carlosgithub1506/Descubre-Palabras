#https://onlinegdb.com/JSpI66NlZ_

import pygame
from constantes_pantalla import *
from Package_funciones.validaciones import *

# clase inicio ejecuta la primera pantalla de juego donde pide un nombre y lo retorna validado
class Inicio:
    def __init__(self,):

        pygame.init()
        self.pos_fondo_x = 0
        self.nickname = ""
        self.input_activo = True
        self.mensaje_error = "Nickname no válido. No se aceptan espacios vacios"
        self.valido_espacios=""
        self.texto_ingreso = ""
        self.imagen_input = ""
        self.boton_star_rect  = ""

        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.fondo_p_diseño = pygame.image.load("imagenes\\fondo_inicio.png").convert()
        self.fondo_p_diseño = pygame.transform.scale(self.fondo_p_diseño, (ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("DESCUBRE PALABRAS")
        self.icono = pygame.image.load('imagenes\\logo.png')
        pygame.display.set_icon(self.icono)
  
        # Cargar fuentes para el texto
        self.fuente = pygame.font.Font(None, 28)
        self.fuente_pequeña = pygame.font.Font(None, 23)

        self.running = True
    # cargar_imagen_blit recibe una lista por parametos, configura las posiciones y tamaño de las imagen y guardan en 2 variable el rect una imagen
    def cargar_imagen_blit(self,lista:list):
        contador = 0
        for elemento in lista:
            imagen = pygame.image.load(elemento[0])
            imagen = pygame.transform.scale(imagen, elemento[1])
            imagen_rect = imagen.get_rect(topleft=elemento[2])
            self.pantalla.blit(imagen, imagen_rect)

            if contador == len(lista) -1:
                self.imagen_input = imagen
            elif contador == len(lista) -2:
                self.boton_star_rect = imagen_rect
            contador += 1
     # actualizar_fondo_pantalla() fondo en movimiento se calcula la posicion de x del fondo y se renderiza en una nueva posicion.
    def actualizar_fondo_pantalla(self)->None:
        self.pantalla.fill(COLOR_NEGRO)
       
        posicion_relativa_x = self.pos_fondo_x % self.fondo_p_diseño.get_rect().width
        self.pantalla.blit(self.fondo_p_diseño, (posicion_relativa_x - self.fondo_p_diseño.get_rect().width, 0))
        if posicion_relativa_x < ANCHO_VENTANA:
            self.pantalla.blit(self.fondo_p_diseño, (posicion_relativa_x, 0))
        self.pos_fondo_x -= 1
            
    # Se verifica el texto del mensaje  error.
    def mostrar_texto_input_mensaje_errors(self)->None:
            if self.valido_espacios :
                texto_error = self.fuente_pequeña.render(self.mensaje_error, True, COLOR_AMARILLO)
                self.pantalla.blit(texto_error, (410, 450))
                self.nickname =""
            if self.input_activo :
                self.texto_ingreso = self.fuente.render(self.nickname, True, COLOR_BLANCO)
                self.pantalla.blit(self.texto_ingreso, (430, 382))

    def validar_espacios(self,palabra:str)-> bool:
        valido_espacio = palabra.count(" ") 
        espacio = False
        if valido_espacio > 0:
            espacio = True
        return espacio
    
    def capturar_evento(self)->None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False 
            # se verefica entrada del texto para el nombre de un jugador.
            if evento.type == pygame.KEYDOWN : 
                if self.input_activo:
                    if evento.key == pygame.K_RETURN:
                        if validar_nickname(self.nickname):
                            self.input_activo = False
                    elif evento.key == pygame.K_BACKSPACE: 
                        self.nickname = self.nickname[:-1] 
                    else:
                        self.nickname += evento.unicode 
                        self.valido_espacios =  self.validar_espacios(self.nickname)
                    if self.texto_ingreso.get_width() > self.imagen_input.get_width()-20:
                        self.nickname = self.nickname[:-1]
                        self.texto_ingreso = self.fuente.render(self.nickname, True, COLOR_BLANCO)

            if evento.type == pygame.MOUSEBUTTONDOWN:
                posicion_click = evento.pos
                #se verifica la colicion del click del mouse con la ubicacion del boton star
                if self.boton_star_rect.collidepoint(posicion_click) and len(self.nickname) > 3 :
                    # Acciona el boton star
                    pantalla = "juego"
                    return pantalla

    def bucle_pantalla_inicio(self,lista)->None:
        
        while self.running:
           
            evento = self.capturar_evento()

            self.actualizar_fondo_pantalla()

            self.cargar_imagen_blit(lista)

            self.mostrar_texto_input_mensaje_errors()

            if evento == "juego":
                pantalla = "juego"
                self.running = False
                return pantalla

            pygame.display.flip()

        pygame.quit()