import pygame
from constantes_pantalla import *

class Continuar:
    def __init__(self, juego=None, pantalla=None):
        if juego and pantalla:
            self.contador_partidas = 0
            self.juego = juego
            self.pantalla = pantalla
            pygame.font.init()  
            self.fuente_popup = pygame.font.SysFont(None, 40)  # type: ignore 

    def mostrar_popup_continuar(self):
        ancho_popup = 400
        alto_popup = 200
        x_popup = (ANCHO_VENTANA - ancho_popup) // 2
        y_popup = (ALTO_VENTANA - alto_popup) // 2

        popup_surface = pygame.Surface((ancho_popup, alto_popup))
        popup_surface.fill((0, 0, 0))

        texto = self.fuente_popup.render("¿Deseas continuar?", True, (255, 255, 255))
        boton_si = pygame.Rect(x_popup + 50, y_popup + 100, 100, 50)
        boton_no = pygame.Rect(x_popup + 250, y_popup + 100, 100, 50)

        self.pantalla.blit(popup_surface, (x_popup, y_popup))
        self.pantalla.blit(texto, (x_popup + (ancho_popup - texto.get_width()) // 2, y_popup + 50))
        pygame.draw.rect(self.pantalla, (0, 255, 0), boton_si)
        pygame.draw.rect(self.pantalla, (255, 0, 0), boton_no)
        texto_si = self.fuente_popup.render("Sí", True, (0, 0, 0))
        texto_no = self.fuente_popup.render("No", True, (0, 0, 0))
        self.pantalla.blit(texto_si, (boton_si.x + (boton_si.width - texto_si.get_width()) // 2, boton_si.y + (boton_si.height - texto_si.get_height()) // 2))
        self.pantalla.blit(texto_no, (boton_no.x + (boton_no.width - texto_no.get_width()) // 2, boton_no.y + (boton_no.height - texto_no.get_height()) // 2))

        pygame.display.flip()

        continuar = False
        esperando_respuesta = True
        while esperando_respuesta:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    posicion_click = evento.pos
                    if boton_si.collidepoint(posicion_click):
                        continuar = True
                        self.contador_partidas += 1
                        esperando_respuesta = False
                    elif boton_no.collidepoint(posicion_click):
                        continuar = False
                        esperando_respuesta = False
        
        return continuar
