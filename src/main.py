import pygame
import sys
import os
from jugador import Jugador
from enemigo import Enemigo

pygame.init()
pygame.mixer.init() 

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invader - IA Engineering")

reloj = pygame.time.Clock()
FPS = 60
NEGRO = (0, 0, 0)

def main():
    directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # --- CARGAR ÍCONO Y FONDO ---
    ruta_icono = os.path.join(directorio_base, "assets", "title_icon.png")
    try:
        icono = pygame.image.load(ruta_icono).convert_alpha()
        pygame.display.set_icon(icono)
    except FileNotFoundError:
        pass

    ruta_fondo = os.path.join(directorio_base, "assets", "background.png")
    try:
        # convert() es más rápido que convert_alpha() para fondos opacos
        fondo = pygame.image.load(ruta_fondo).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except FileNotFoundError:
        fondo = None

    # --- CONFIGURACIÓN DE AUDIO ---
    ruta_musica = os.path.join(directorio_base, "assets", "music.mp3")
    ruta_explosion = os.path.join(directorio_base, "assets", "explosion.mp3")
    
    try:
        pygame.mixer.music.load(ruta_musica)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1) 
    except pygame.error:
        pass

    try:
        sonido_explosion = pygame.mixer.Sound(ruta_explosion)
        sonido_explosion.set_volume(0.4)
    except FileNotFoundError:
        sonido_explosion = None

    jugando = True
    nave = Jugador(ANCHO // 2, ALTO - 50)
    
    grupo_sprites = pygame.sprite.Group()
    grupo_enemigos = pygame.sprite.Group()
    grupo_laseres = pygame.sprite.Group() 
    
    grupo_sprites.add(nave)

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
                    nave.disparar(grupo_sprites, grupo_laseres)
                
        teclas_presionadas = pygame.key.get_pressed()
        nave.update(teclas_presionadas)
        
        for sprite in grupo_sprites:
            if sprite != nave: 
                sprite.update()
                
        choques = pygame.sprite.groupcollide(grupo_laseres, grupo_enemigos, True, True)
        
        if choques and sonido_explosion:
            sonido_explosion.play()
        
        # --- RENDERIZADO DEL FONDO ---
        if fondo:
            # blit() 'pega' una imagen sobre la pantalla en la coordenada (0,0)
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(NEGRO)
            
        grupo_sprites.draw(pantalla)
        
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()