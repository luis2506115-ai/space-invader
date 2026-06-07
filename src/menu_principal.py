import pygame
import sys
import os

class MenuPrincipal:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.ANCHO = 800
        self.ALTO = 600

        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
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

    def ejecutar(self):
        opciones = ["Iniciar juego", "Puntajes", "Acerca de"]
        reloj = pygame.time.Clock()
        fuente_opciones = pygame.font.SysFont("impact", 32)

        fondo = self.cargar_imagen("menu_fondo.jpg", "background.png")
        if fondo:
            fondo = pygame.transform.scale(fondo, (self.ANCHO, self.ALTO))

        imagen = self.cargar_imagen("hybridge.gif", "title_icon.png")
        if imagen:
            imagen = pygame.transform.scale(imagen, (80, 80))

        viendo_menu = True
        while viendo_menu:
            # Obtenemos la posición actual del ratón
            mouse_pos = pygame.mouse.get_pos()
            
            if fondo:
                self.pantalla.blit(fondo, (0, 0))
            else:
                self.pantalla.fill(self.NEGRO)

            self.mostrar_texto("Space Invader", pygame.font.SysFont("impact", 64), self.VERDE, self.ANCHO // 2, self.ALTO // 4)
            self.mostrar_texto("Hybridge", pygame.font.SysFont("impact", 36), self.BLANCO, self.ANCHO // 2, self.ALTO // 4 + 40)

            if imagen:
                self.pantalla.blit(imagen, (self.ANCHO // 2 - 40, self.ALTO // 4 + 60))

            rectangulos_texto = []
            for i, opcion in enumerate(opciones):
                # Calculamos temporalmente el rectángulo para saber si el ratón está encima
                texto_temporal = fuente_opciones.render(opcion, True, self.BLANCO)
                rect_temporal = texto_temporal.get_rect(center=(self.ANCHO // 2, self.ALTO // 4 + 90 * (i + 1) + 100))
                
                # Efecto Hover: Cambia a ROJO si el ratón toca el área del texto
                color_texto = self.ROJO if rect_temporal.collidepoint(mouse_pos) else self.BLANCO
                
                # Renderizamos el texto final con el color correcto
                rect_texto = self.mostrar_texto(opcion, fuente_opciones, color_texto, self.ANCHO // 2, self.ALTO // 4 + 90 * (i + 1) + 100)
                
                # Guardamos el rectángulo y el nombre de la opción para usarlos en el clic
                rectangulos_texto.append((rect_texto, opcion))

            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Lógica de detección de clics del ratón
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for rect, opcion in rectangulos_texto:
                        if rect.collidepoint(evento.pos):
                            return opcion # Regresa la opción seleccionada al main.py
            
            reloj.tick(60)