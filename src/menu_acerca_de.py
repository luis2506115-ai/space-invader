import pygame
import sys
import os
import webbrowser
import platform # Agregado para detectar el sistema operativo
import subprocess # Agregado para enlaces web multiplataforma

class MenuAcercaDe:
    def __init__(self, pantalla):
        # Recibimos la pantalla principal del juego
        self.pantalla = pantalla
        self.ANCHO = 800
        self.ALTO = 600

        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.GRIS = (150, 150, 150)
        self.ROJO = (255, 0, 0)
        self.VERDE = (0, 255, 0)

        self.directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def cargar_imagen(self, nombre_archivo, fallback):
        ruta = os.path.join(self.directorio_base, "assets", nombre_archivo)
        ruta_fallback = os.path.join(self.directorio_base, "assets", fallback)
        try:
            return pygame.image.load(ruta).convert_alpha()
        except FileNotFoundError:
            try:
                return pygame.image.load(ruta_fallback).convert_alpha()
            except FileNotFoundError:
                return None

    def mostrar_texto(self, texto, font, color, x, y):
        texto_objeto = font.render(texto, True, color)
        rectangulo_texto = texto_objeto.get_rect()
        rectangulo_texto.center = (x, y)
        self.pantalla.blit(texto_objeto, rectangulo_texto)
        return rectangulo_texto

    def dibujar_boton(self, texto, font, color_fondo, color_texto, x, y, ancho, alto):
        pygame.draw.rect(self.pantalla, color_fondo, (x, y, ancho, alto))
        texto_objeto = font.render(texto, True, color_texto)
        rect_texto = texto_objeto.get_rect(center=(x + ancho // 2, y + alto // 2))
        self.pantalla.blit(texto_objeto, rect_texto)

    def mostrar_contenido(self, contenido, font_contenido, y_offset):
        espacio_horizontal_disponible = self.ANCHO - 100 
        for linea in contenido.split('\n'):
            palabras = linea.split()
            texto_linea = ""
            for palabra in palabras:
                texto_linea_temp = texto_linea + palabra + " "
                texto_ancho_temp = font_contenido.size(texto_linea_temp)[0]
                if texto_ancho_temp < espacio_horizontal_disponible:
                    texto_linea = texto_linea_temp
                else:
                    self.mostrar_texto(texto_linea.strip(), font_contenido, self.BLANCO, self.ANCHO // 2, y_offset)
                    y_offset += font_contenido.size(texto_linea.strip())[1] + 5
                    texto_linea = palabra + " "
            # Muestra la última línea del párrafo
            self.mostrar_texto(texto_linea.strip(), font_contenido, self.BLANCO, self.ANCHO // 2, y_offset)
            y_offset += font_contenido.size(texto_linea.strip())[1] + 5

    def ejecutar(self):
        fondo = self.cargar_imagen("menu_fondo.jpg", "background.png")
        if fondo:
            fondo = pygame.transform.scale(fondo, (self.ANCHO, self.ALTO))

        titulo_font = pygame.font.SysFont("impact", 48)
        subtitulo_font = pygame.font.SysFont("impact", 36)
        # Arial es más legible para párrafos largos
        font_contenido = pygame.font.SysFont("arial", 22) 
        font_enlace = pygame.font.SysFont("impact", 30)
        font_boton = pygame.font.SysFont("impact", 36)

        viendo_menu = True
        while viendo_menu:
            mouse_pos = pygame.mouse.get_pos()

            if fondo:
                self.pantalla.blit(fondo, (0, 0))
            else:
                self.pantalla.fill(self.NEGRO)

            self.mostrar_texto("ACERCA DE", titulo_font, self.VERDE, self.ANCHO // 2, 80)
            self.mostrar_texto("Space Invader - IA Engineering", subtitulo_font, self.BLANCO, self.ANCHO // 2, 140)

            # Contenido del profesor
            contenido = "¡Explora la galaxia y aprende Programación Orientada a Objetos (POO)\ncon nuestro emocionante Space Invaders!\n\nCada nave, cada disparo, ¡todo es un objeto interactivo!\nÚnete a nosotros para una experiencia divertida y educativa en\neste emocionante cruce de juego y aprendizaje.\n¡Prepárate para salvar el universo!"
            
            self.mostrar_contenido(contenido, font_contenido, 220)

            # Enlace web interactivo
            color_enlace = self.VERDE if 300 <= mouse_pos[1] <= 520 else self.ROJO
            rect_enlace = self.mostrar_texto("¡Haz clic aquí para visitar Hybridge!", font_enlace, color_enlace, self.ANCHO // 2, 500)

            # Botón atrás interactivo
            color_boton = self.VERDE if 20 <= mouse_pos[0] <= 160 and 20 <= mouse_pos[1] <= 70 else self.GRIS
            self.dibujar_boton("< VOLVER", font_boton, color_boton, self.NEGRO, 20, 20, 140, 50)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        # Si hace clic en volver
                        if 20 <= event.pos[0] <= 160 and 20 <= event.pos[1] <= 70:
                            viendo_menu = False 
                        # Si hace clic en el enlace usando la colisión del rectángulo
                        elif rect_enlace.collidepoint(event.pos):

                            # Verificamos si estamos dentro del subsistema de Windows (WSL)
                            if 'microsoft' in platform.uname().release.lower(): 
                                # Usamos el estándar moderno en lugar de os.system
                                subprocess.run(["explorer.exe", "https://hybridge.education"])
                            else:
                                # Para Windows nativo, macOS y Linux puro
                                webbrowser.open("https://hybridge.education")