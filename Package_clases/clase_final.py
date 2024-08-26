import pygame
from constantes_pantalla import *
from Package_funciones.archivo_json import *

# clase pantalla final muestra el escore de los 5 mejores jugadores
class PantallaFinal:
    def __init__(self):
        self.configurar_pantalla()
        self.lista_puntuaciones = []
        self.running = True
        self.boton_close_rect = ""
    
    def configurar_pantalla(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("DESCUBRE PALABRAS")
        self.fondo_p_diseño = pygame.image.load("imagenes\\fondo_pantalla_continuar.png").convert()
        self.fondo_p_diseño = pygame.transform.scale(self.fondo_p_diseño, (ANCHO_VENTANA, ALTO_VENTANA))
        self.icono = pygame.image.load('imagenes\\logo_pantalla_continuar.png')
        pygame.display.set_icon(self.icono)
        self.fuente = pygame.font.Font(None, 48)

    def cargar_mostrar_imagenes(self,lista:list)->None:
        contador = 0
        for elemento in lista:
            imagen = pygame.image.load(elemento[0])
            imagen = pygame.transform.scale(imagen, elemento[1])
            imagen_rect = imagen.get_rect(topleft=elemento[2])
            self.pantalla.blit(imagen, imagen_rect)
            if contador == 3:
                self.boton_close_rect = imagen_rect
            contador += 1

    def mostrar_puntuacion(self)->None:
        y_pos = 250
        for jugador in self.lista_puntuaciones:
            nombre = jugador["nickname"]
            puntuacion = jugador["puntuacion"]
            texto = self.fuente.render(f"{nombre}: {puntuacion}", True, COLOR_NARANJA)
            texto_rect = texto.get_rect(center=(ANCHO_VENTANA // 2, y_pos))
            self.pantalla.blit(texto, texto_rect)
            y_pos += 50 

    def ordenar_lista(self,lista:list)->list:
        clave = "puntuacion"
        for i in range(len(lista)):
            for j in range(i+1, len(lista)):
                if lista[i][clave] < lista[j][clave]:
                    lista[j], lista[i] = lista[i], lista[j]
        return  lista

    def obtener_top_puntuaciones(self)->None:
        puntuaciones = cargar_lista_desde_json("lista_jugadores.json")
        puntuaciones_ordenadas = self.ordenar_lista(puntuaciones)
        self.lista_puntuaciones = puntuaciones_ordenadas[:5]

    def bucle_pantalla_final(self,lista:list)->None:
        self.obtener_top_puntuaciones()
        while self.running:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.running = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    posicion_click = evento.pos
                    if self.boton_close_rect.collidepoint(posicion_click):
                        self.running = False

            self.pantalla.fill(COLOR_NEGRO)
            self.pantalla.blit(self.fondo_p_diseño, (0, 0))
            self.cargar_mostrar_imagenes(lista)
            self.mostrar_puntuacion()
            
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    pantalla_final = PantallaFinal()
    pantalla_final.bucle_pantalla_final()
