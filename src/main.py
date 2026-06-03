import pygame
import sys
import os
from jugador import Jugador
from enemigo import Enemigo

pygame.init()
pygame.mixer.init()
pygame.font.init() # 1. Inicializamos el módulo de fuentes tipográficas

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invader - IA Engineering")

reloj = pygame.time.Clock()
FPS = 60
NEGRO = (0, 0, 0)

# 2. Configuramos la fuente (usamos 'impact' para un estilo más Arcade)
fuente_puntuacion = pygame.font.SysFont("impact", 32)

def main():
    directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    ruta_icono = os.path.join(directorio_base, "assets", "title_icon.png")
    try:
        icono = pygame.image.load(ruta_icono).convert_alpha()
        pygame.display.set_icon(icono)
    except FileNotFoundError:
        pass

    ruta_fondo = os.path.join(directorio_base, "assets", "background.png")
    try:
        fondo = pygame.image.load(ruta_fondo).convert()
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except FileNotFoundError:
        fondo = None

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
    
    # 3. Variable inicial para llevar la cuenta de los puntos
    puntuacion = 0
    
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
        
        # 4. Lógica de puntuación en colisiones
        if choques:
            if sonido_explosion:
                sonido_explosion.play()
            
            # choques devuelve un diccionario. Iteramos sobre los valores para sumar 10 puntos por cada enemigo destruido
            for aliens_destruidos in choques.values():
                puntuacion += len(aliens_destruidos) * 10
        
        if fondo:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(NEGRO)
            
        grupo_sprites.draw(pantalla)
        
        # 5. Renderizado del texto de puntuación en pantalla
        # render(texto, antialiasing (para bordes suaves), color RGB)
        texto_superficie = fuente_puntuacion.render(f"SCORE: {puntuacion}", True, (255, 255, 255))
        pantalla.blit(texto_superficie, (20, 20))
        
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()