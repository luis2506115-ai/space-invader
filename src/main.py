import pygame
import sys
import os
from jugador import Jugador
from enemigo import Enemigo

pygame.init()
pygame.mixer.init()
pygame.font.init() 

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invader - IA Engineering")

reloj = pygame.time.Clock()
FPS = 60
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Fuentes para el HUD y pantallas de estado
fuente_hud = pygame.font.SysFont("impact", 30)
fuente_pantallas = pygame.font.SysFont("impact", 64)
fuente_subtitulo = pygame.font.SysFont("impact", 24)

def generar_flota(nivel, grupo_sprites, grupo_enemigos):
    # Asegura la limpieza de remanentes antes de poblar la nueva oleada
    grupo_enemigos.empty()
    
    # Renderizado de la cuadrícula de 4x8
    for fila in range(4):
        for columna in range(8):
            e_x = 100 + (columna * 70)
            e_y = 50 + (fila * 60)
            alien = Enemigo(e_x, e_y, nivel)
            grupo_enemigos.add(alien)
            grupo_sprites.add(alien)

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
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1) 
    except pygame.error:
        pass

    try:
        sonido_explosion = pygame.mixer.Sound(ruta_explosion)
        sonido_explosion.set_volume(0.4)
    except FileNotFoundError:
        sonido_explosion = None

    # --- CONFIGURACIÓN DEL SISTEMA DE JUEGO ---
    estado = "JUGANDO" # Estados posibles: "JUGANDO", "GAME_OVER", "VICTORIA"
    nivel = 1
    MAX_NIVELES = 9
    puntuacion = 0
    
    nave = Jugador(ANCHO // 2, ALTO - 50)
    
    grupo_sprites = pygame.sprite.Group()
    grupo_enemigos = pygame.sprite.Group()
    grupo_laseres = pygame.sprite.Group() 
    
    grupo_sprites.add(nave)
    generar_flota(nivel, grupo_sprites, grupo_enemigos)

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and estado == "JUGANDO":
                    nave.disparar(grupo_sprites, grupo_laseres)
                # Reinicio del sistema con la tecla 'R' en pantallas de fin de juego
                elif evento.key == pygame.K_r and estado in ["GAME_OVER", "VICTORIA"]:
                    estado = "JUGANDO"
                    nivel = 1
                    puntuacion = 0
                    grupo_sprites.empty()
                    grupo_enemigos.empty()
                    grupo_laseres.empty()
                    nave = Jugador(ANCHO // 2, ALTO - 50)
                    grupo_sprites.add(nave)
                    generar_flota(nivel, grupo_sprites, grupo_enemigos)

        if estado == "JUGANDO":
            teclas_presionadas = pygame.key.get_pressed()
            nave.update(teclas_presionadas)
            
            for sprite in grupo_sprites:
                if sprite != nave: 
                    sprite.update()
                    
            # Colisiones de armamento vs objetivos
            choques = pygame.sprite.groupcollide(grupo_laseres, grupo_enemigos, True, True)
            if choques:
                if sonido_explosion:
                    sonido_explosion.play()
                for aliens_destruidos in choques.values():
                    puntuacion += len(aliens_destruidos) * 10
            
            # --- EVALUACIÓN DE CONTROL DE NIVEL ---
            if len(grupo_enemigos) == 0:
                if nivel < MAX_NIVELES:
                    nivel += 1
                    grupo_laseres.empty()
                    grupo_sprites.empty()
                    grupo_sprites.add(nave)
                    generar_flota(nivel, grupo_sprites, grupo_enemigos)
                else:
                    estado = "VICTORIA"

            # --- VERIFICACIÓN DE CONDICIONES DE DERROTA ---
            # 1. Intersección física de un enemigo con la nave
            if pygame.sprite.spritecollideany(nave, grupo_enemigos):
                estado = "GAME_OVER"
            
            # 2. Invasión de la línea de defensa (límite inferior de pantalla)
            for enemigo in grupo_enemigos:
                if enemigo.rect.bottom >= ALTO - 40:
                    estado = "GAME_OVER"
                    break

        # --- CAPA DE RENDERIZADO ---
        if fondo:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(NEGRO)
            
        if estado == "JUGANDO":
            grupo_sprites.draw(pantalla)
            
            # Dibujar textos del HUD
            txt_score = fuente_hud.render(f"SCORE: {puntuacion}", True, BLANCO)
            txt_level = fuente_hud.render(f"LEVEL: {nivel}/{MAX_NIVELES}", True, VERDE)
            pantalla.blit(txt_score, (20, 20))
            pantalla.blit(txt_level, (ANCHO - 180, 20))
            
        elif estado == "GAME_OVER":
            txt_go = fuente_pantallas.render("GAME OVER", True, ROJO)
            txt_fs = fuente_subtitulo.render(f"PUNTUACIÓN FINAL: {puntuacion}", True, BLANCO)
            txt_rest = fuente_subtitulo.render("Presiona 'R' para reiniciar la simulación", True, VERDE)
            
            pantalla.blit(txt_go, (ANCHO // 2 - txt_go.get_width() // 2, ALTO // 2 - 80))
            pantalla.blit(txt_fs, (ANCHO // 2 - txt_fs.get_width() // 2, ALTO // 2))
            pantalla.blit(txt_rest, (ANCHO // 2 - txt_rest.get_width() // 2, ALTO // 2 + 50))
            
        elif estado == "VICTORIA":
            txt_vic = fuente_pantallas.render("¡CAMPAÑA COMPLETADA!", True, VERDE)
            txt_fs = fuente_subtitulo.render(f"PUNTUACIÓN PERFECTA: {puntuacion}", True, BLANCO)
            txt_rest = fuente_subtitulo.render("Presiona 'R' para iniciar un nuevo despliegue", True, BLANCO)
            
            pantalla.blit(txt_vic, (ANCHO // 2 - txt_vic.get_width() // 2, ALTO // 2 - 80))
            pantalla.blit(txt_fs, (ANCHO // 2 - txt_fs.get_width() // 2, ALTO // 2))
            pantalla.blit(txt_rest, (ANCHO // 2 - txt_rest.get_width() // 2, ALTO // 2 + 50))
            
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()