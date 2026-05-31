import pygame
import os
import random # <-- Implementamos el módulo random

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Si tienes una imagen, nómbrala alien.png y ponla en assets/
        ruta_imagen = os.path.join(directorio_base, "assets", "alien.png")
        
        try:
            imagen_original = pygame.image.load(ruta_imagen).convert_alpha()
            self.image = pygame.transform.scale(imagen_original, (40, 40))
        except FileNotFoundError:
            # Si no hay imagen, usamos random para crear cuadros con diferentes tonos de rojo
            self.image = pygame.Surface((40, 40))
            tono_rojo = random.randint(150, 255)
            self.image.fill((tono_rojo, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Usamos random para que la mitad empiece yendo a la izquierda y la otra a la derecha
        velocidad_inicial = random.choice([-3, 3])
        self.velocidad_x = velocidad_inicial

    def update(self):
        self.rect.x += self.velocidad_x
        
        # Lógica de rebote: Si tocan los bordes de la pantalla, invierten su dirección y bajan un poco
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.velocidad_x *= -1 # Invertir dirección
            self.rect.y += 15      # Bajar hacia el jugador