import pygame
import os

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Usamos la imagen del disparo
        ruta_imagen = os.path.join(directorio_base, "assets", "bullet_image.png")
        
        try:
            imagen_original = pygame.image.load(ruta_imagen).convert_alpha()
            # Tamaño del láser
            self.image = pygame.transform.scale(imagen_original, (10, 30)) 
        except FileNotFoundError:
            self.image = pygame.Surface((4, 20)) 
            self.image.fill((255, 255, 0)) 
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad = -10 

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()