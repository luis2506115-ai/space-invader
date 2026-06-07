import pygame
import sys
import os

class MenuPuntajes:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.ANCHO = 800
        self.ALTO = 600
        
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.GRIS = (200, 200, 200)
        self.ROJO = (255, 0, 0)
        self.VERDE = (0, 255, 0)

        # Lógica especial para leer el archivo .txt desde donde esté el .exe
        if getattr(sys, 'frozen', False):
            directorio_txt = os.path.dirname(sys.executable)
            # Y para cargar la imagen de fondo, usamos _MEIPASS
            self.directorio_base = sys._MEIPASS
        else:
            directorio_txt = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.directorio_base = directorio_txt
            
        self.archivo_puntajes = os.path.join(directorio_txt, "puntajes.txt")

        
    def cargar_puntajes(self):
        registros = []
        try:
            # Abrimos con codificación segura
            with open(self.archivo_puntajes, 'r', encoding='utf-8') as file:
                for line in file:
                    if "," in line:
                        # Separación idéntica a la guía del cuaderno
                        nombre, puntuacion = line.strip().split(",")
                        registros.append((nombre, int(puntuacion)))
        except FileNotFoundError:
            print("El archivo puntajes.txt no existe aún. Se creará al guardar.")
            
        # Ordenamos de mayor a menor y retornamos el TOP 5
        return sorted(registros, key=lambda x: x[1], reverse=True)[:5]

    def mostrar_texto(self, texto, font, color, x, y):
        texto_objeto = font.render(texto, True, color)
        rectangulo_texto = texto_objeto.get_rect()
        rectangulo_texto.center = (x, y)
        self.pantalla.blit(texto_objeto, rectangulo_texto)

    def dibujar_boton(self, texto, font, color_fondo, color_texto, x, y, ancho, alto):
        pygame.draw.rect(self.pantalla, color_fondo, (x, y, ancho, alto))
        self.mostrar_texto(texto, font, color_texto, x + ancho / 2, y + alto / 2)

    def mostrar_pantalla(self, puntajes):
        self.pantalla.fill(self.NEGRO)

        ruta_fondo = os.path.join(self.directorio_base, "assets", "background.png")
        try:
            fondo = pygame.image.load(ruta_fondo).convert()
            fondo = pygame.transform.scale(fondo, (self.ANCHO, self.ALTO))
            self.pantalla.blit(fondo, (0, 0))
        except FileNotFoundError:
            pass

        fuente_titulo = pygame.font.SysFont("impact", 48)
        fuente_sub = pygame.font.SysFont("impact", 36)
        
        self.mostrar_texto("MEJORES PUNTAJES", fuente_titulo, self.BLANCO, self.ANCHO // 2, 80)
        self.mostrar_texto("Space Invader - IA Engineering", fuente_sub, self.VERDE, self.ANCHO // 2, 130)

        if not puntajes:
            self.mostrar_texto("Aún no hay registros", fuente_sub, self.ROJO, self.ANCHO // 2, self.ALTO // 2)
        else:
            y_offset = 220
            for i, (nombre, puntaje) in enumerate(puntajes, 1):
                color_texto = self.BLANCO if i == 1 else self.ROJO
                tamano_fuente = 42 if i == 1 else 36 
                fuente_lista = pygame.font.SysFont("impact", tamano_fuente)
                
                self.mostrar_texto(f"{i}. {nombre} : {puntaje}", fuente_lista, color_texto, self.ANCHO // 2, y_offset)
                y_offset += 60

        fuente_boton = pygame.font.SysFont("impact", 36)
        self.dibujar_boton("< VOLVER", fuente_boton, self.GRIS, self.NEGRO, 20, 20, 140, 50)
        pygame.display.update()

    def ejecutar(self):
        puntajes = self.cargar_puntajes()
        viendo_menu = True
        while viendo_menu:
            self.mostrar_pantalla(puntajes)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    x, y = evento.pos
                    if 20 <= x <= 160 and 20 <= y <= 70: 
                        viendo_menu = False