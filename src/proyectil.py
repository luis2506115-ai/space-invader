import pygame

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Un láser delgado y alargado
        self.image = pygame.Surface((4, 20)) 
        self.image.fill((255, 255, 0)) # Color amarillo
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad = -10 # Negativo porque va hacia arriba en la pantalla

    def update(self):
        self.rect.y += self.velocidad
        # Si el láser sale por la parte superior de la pantalla, lo destruimos
        # Esto es vital para no llenar tu memoria de objetos invisibles
        if self.rect.bottom < 0:
            self.kill()