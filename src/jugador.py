import pygame
import os
import time # <-- Implementamos el módulo time
from proyectil import Proyectil # <-- Importamos nuestra nueva clase

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_imagen = os.path.join(directorio_base, "assets", "nave.png")
        
        try:
            imagen_original = pygame.image.load(ruta_imagen).convert_alpha()
            # ¡Aquí puedes cambiar el tamaño!
            self.image = pygame.transform.scale(imagen_original, (90, 90))
        except FileNotFoundError:
            self.image = pygame.Surface((50, 30))
            self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = 5
        
        # --- LÓGICA DE TIEMPO (COOLDOWN) ---
        # time.time() nos da el tiempo exacto actual en segundos
        self.ultimo_disparo = time.time()
        self.cooldown = 0.4 # 0.4 segundos de espera entre cada disparo

    def update(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.velocidad

    def disparar(self, grupo_sprites, grupo_laseres): # <-- Añadimos grupo_laseres aquí
        tiempo_actual = time.time()
        if tiempo_actual - self.ultimo_disparo >= self.cooldown:
            laser = Proyectil(self.rect.centerx, self.rect.top)
            
            grupo_sprites.add(laser)  # Para que se dibuje en pantalla
            grupo_laseres.add(laser)  # Para calcular las colisiones
            
            self.ultimo_disparo = tiempo_actual   # Actualizamos el tiempo del último disparo