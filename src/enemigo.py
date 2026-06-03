import pygame
import os
import random

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Lista con las imágenes disponibles
        opciones_alien = ["enemy_blue_image.png", "enemy_green_image.png", "enemy_purple_image.png"]
        # Selección aleatoria
        alien_elegido = random.choice(opciones_alien)
        
        ruta_imagen = os.path.join(directorio_base, "assets", alien_elegido)
        
        try:
            imagen_original = pygame.image.load(ruta_imagen).convert_alpha()
            self.image = pygame.transform.scale(imagen_original, (50, 50))
        except FileNotFoundError:
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.velocidad_x = random.choice([-3, 3])

    def update(self):
        self.rect.x += self.velocidad_x
        
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.velocidad_x *= -1 
            self.rect.y += 15