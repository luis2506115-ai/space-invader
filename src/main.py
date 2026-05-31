import pygame
import sys
from jugador import Jugador
from enemigo import Enemigo

pygame.init()

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invader - IA Engineering")

reloj = pygame.time.Clock()
FPS = 60
NEGRO = (0, 0, 0)

def main():
    jugando = True
    
    nave = Jugador(ANCHO // 2, ALTO - 50)
    
    grupo_sprites = pygame.sprite.Group()
    grupo_enemigos = pygame.sprite.Group()
    grupo_laseres = pygame.sprite.Group() # <-- 1. Creamos el grupo de láseres
    
    grupo_sprites.add(nave)

    # Generar la flota
    for fila in range(4):
        for columna in range(8):
            e_x = 100 + (columna * 70)
            e_y = 50 + (fila * 60)
            alien = Enemigo(e_x, e_y)
            grupo_enemigos.add(alien)
            grupo_sprites.add(alien)

    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    # 2. Le pasamos ambos grupos a la función disparar
                    nave.disparar(grupo_sprites, grupo_laseres)
                
        teclas_presionadas = pygame.key.get_pressed()
        nave.update(teclas_presionadas)
        
        for sprite in grupo_sprites:
            if sprite != nave: 
                sprite.update()
                
        # --- 3. LÓGICA DE COLISIONES ---
        # groupcollide(grupo1, grupo2, dokill1, dokill2)
        # Los dos "True" significan: "Destruye el láser (True) y destruye el enemigo (True)"
        choques = pygame.sprite.groupcollide(grupo_laseres, grupo_enemigos, True, True)
        
        pantalla.fill(NEGRO)
        grupo_sprites.draw(pantalla)
        
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()