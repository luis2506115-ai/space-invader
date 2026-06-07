import pygame
import sys
import os
import time
from proyectil import Proyectil

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        if getattr(sys, 'frozen', False):
            # Si se está ejecutando como un .exe empaquetado
            directorio_base = sys._MEIPASS
        else:
            # Si se ejecuta como script .py normal
            directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        ruta_imagen = os.path.join(directorio_base, "assets", "player_image.png")
        
        try:
            imagen_original = pygame.image.load(ruta_imagen).convert_alpha()
            self.image = pygame.transform.scale(imagen_original, (90, 90))
        except FileNotFoundError:
            self.image = pygame.Surface((50, 30))
            self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = 5
        
        self.ultimo_disparo = time.time()
        self.cooldown = 0.4 

        # --- CARGAMOS EL SONIDO DEL LÁSER (.mp3) ---
        ruta_laser = os.path.join(directorio_base, "assets", "laser.mp3")
        try:
            self.sonido_disparo = pygame.mixer.Sound(ruta_laser)
            self.sonido_disparo.set_volume(0.3)
        except FileNotFoundError:
            self.sonido_disparo = None
            print("Advertencia: No se encontró laser.mp3")

    def update(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.velocidad

    def disparar(self, grupo_sprites, grupo_laseres):
        tiempo_actual = time.time()
        if tiempo_actual - self.ultimo_disparo >= self.cooldown:
            laser = Proyectil(self.rect.centerx, self.rect.top)
            
            grupo_sprites.add(laser)
            grupo_laseres.add(laser)
            
            # --- REPRODUCIMOS EL SONIDO ---
            if self.sonido_disparo:
                self.sonido_disparo.play()
                
            self.ultimo_disparo = tiempo_actual