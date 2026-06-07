import pygame
import sys
import os
from jugador import Jugador
from enemigo import Enemigo
from menu_puntajes import MenuPuntajes

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
AZUL_OSCURO = (0, 50, 100)
GRIS = (150, 150, 150)

fuente_hud = pygame.font.SysFont("impact", 30)
fuente_pantallas = pygame.font.SysFont("impact", 64)
fuente_subtitulo = pygame.font.SysFont("impact", 24)

# Modificamos guardar_puntaje para que reciba el nombre dinámico
def guardar_puntaje(nombre, puntuacion):
    if puntuacion > 0: 
        directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        archivo = os.path.join(directorio_base, "puntajes.txt")
        # Usamos utf-8 por si escriben acentos
        with open(archivo, "a", encoding="utf-8") as f:
            f.write(f"{nombre}, {puntuacion}\n")

def generar_flota(nivel, grupo_sprites, grupo_enemigos):
    grupo_enemigos.empty()
    for fila in range(4):
        for columna in range(8):
            e_x = 100 + (columna * 70)
            e_y = 50 + (fila * 60)
            alien = Enemigo(e_x, e_y, nivel)
            grupo_enemigos.add(alien)
            grupo_sprites.add(alien)

def dibujar_boton(texto, x, y, ancho, alto):
    mouse_pos = pygame.mouse.get_pos()
    color = AZUL_OSCURO
    if x <= mouse_pos[0] <= x + ancho and y <= mouse_pos[1] <= y + alto:
        color = VERDE
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    pygame.draw.rect(pantalla, BLANCO, (x, y, ancho, alto), 2) 
    texto_render = fuente_subtitulo.render(texto, True, BLANCO)
    rect_texto = texto_render.get_rect(center=(x + ancho//2, y + alto//2))
    pantalla.blit(texto_render, rect_texto)


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

    menu_leaderboard = MenuPuntajes(pantalla)

    estado = "INICIO" 
    nivel = 1
    MAX_NIVELES = 9
    puntuacion = 0
    
    # Variables para la caja de texto
    nombre_jugador = ""
    estado_post_ingreso = "" # Para saber si vamos a GAME_OVER o VICTORIA después de escribir
    
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
            
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = evento.pos
                if estado == "INICIO":
                    if ANCHO//2 - 100 <= x <= ANCHO//2 + 100 and 300 <= y <= 350:
                        estado = "JUGANDO"
                    elif ANCHO//2 - 100 <= x <= ANCHO//2 + 100 and 380 <= y <= 430:
                        menu_leaderboard.ejecutar() 
                elif estado in ["GAME_OVER", "VICTORIA"]:
                    if ANCHO//2 - 120 <= x <= ANCHO//2 + 120 and ALTO//2 + 100 <= y <= ALTO//2 + 150:
                        menu_leaderboard.ejecutar()

            elif evento.type == pygame.KEYDOWN:
                if estado == "JUGANDO":
                    if evento.key == pygame.K_SPACE:
                        nave.disparar(grupo_sprites, grupo_laseres)
                
                # --- NUEVO: CAPTURA DE TEXTO EN INGRESO_NOMBRE ---
                elif estado == "INGRESO_NOMBRE":
                    if evento.key == pygame.K_RETURN: # Al presionar Enter
                        if nombre_jugador.strip() == "":
                            nombre_jugador = "Anónimo"
                        guardar_puntaje(nombre_jugador, puntuacion)
                        estado = estado_post_ingreso
                    elif evento.key == pygame.K_BACKSPACE: # Al borrar
                        nombre_jugador = nombre_jugador[:-1]
                    else:
                        # Limitamos a 12 caracteres y evitamos las comas
                        if len(nombre_jugador) < 12 and evento.unicode.isprintable() and evento.unicode != ",":
                            nombre_jugador += evento.unicode
                            
                elif estado in ["GAME_OVER", "VICTORIA"]:
                    if evento.key == pygame.K_r:
                        estado = "JUGANDO"
                        nivel = 1
                        puntuacion = 0
                        nombre_jugador = "" # Limpiamos el nombre para la próxima partida
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
                    
            choques = pygame.sprite.groupcollide(grupo_laseres, grupo_enemigos, True, True)
            if choques:
                if sonido_explosion:
                    sonido_explosion.play()
                for aliens_destruidos in choques.values():
                    puntuacion += len(aliens_destruidos) * 10
            
            if len(grupo_enemigos) == 0:
                if nivel < MAX_NIVELES:
                    nivel += 1
                    grupo_laseres.empty()
                    grupo_sprites.empty()
                    grupo_sprites.add(nave)
                    generar_flota(nivel, grupo_sprites, grupo_enemigos)
                else:
                    estado = "INGRESO_NOMBRE"
                    estado_post_ingreso = "VICTORIA"

            if pygame.sprite.spritecollideany(nave, grupo_enemigos):
                estado = "INGRESO_NOMBRE"
                estado_post_ingreso = "GAME_OVER"
            
            for enemigo in grupo_enemigos:
                if enemigo.rect.bottom >= ALTO - 40:
                    estado = "INGRESO_NOMBRE"
                    estado_post_ingreso = "GAME_OVER"
                    break

        # --- RENDERIZADO ---
        if fondo:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(NEGRO)
            
        if estado == "INICIO":
            txt_titulo = fuente_pantallas.render("SPACE INVADER", True, VERDE)
            pantalla.blit(txt_titulo, (ANCHO // 2 - txt_titulo.get_width() // 2, 150))
            dibujar_boton("JUGAR", ANCHO//2 - 100, 300, 200, 50)
            dibujar_boton("PUNTAJES", ANCHO//2 - 100, 380, 200, 50)

        elif estado == "JUGANDO":
            grupo_sprites.draw(pantalla)
            txt_score = fuente_hud.render(f"SCORE: {puntuacion}", True, BLANCO)
            txt_level = fuente_hud.render(f"LEVEL: {nivel}/{MAX_NIVELES}", True, VERDE)
            pantalla.blit(txt_score, (20, 20))
            pantalla.blit(txt_level, (ANCHO - 180, 20))
            
        # --- NUEVO: PANTALLA DE INGRESO DE TEXTO ---
        elif estado == "INGRESO_NOMBRE":
            txt_ingreso = fuente_pantallas.render("NUEVO RÉCORD", True, BLANCO)
            txt_instruccion = fuente_subtitulo.render("Ingresa tu nombre de piloto:", True, VERDE)
            
            # Efecto de parpadeo del cursor usando el reloj de Pygame
            cursor = "_" if pygame.time.get_ticks() % 1000 < 500 else ""
            txt_nombre = fuente_pantallas.render(nombre_jugador + cursor, True, ROJO)
            
            txt_enter = fuente_subtitulo.render("Presiona ENTER para guardar", True, GRIS)
            
            pantalla.blit(txt_ingreso, (ANCHO // 2 - txt_ingreso.get_width() // 2, ALTO // 2 - 150))
            pantalla.blit(txt_instruccion, (ANCHO // 2 - txt_instruccion.get_width() // 2, ALTO // 2 - 50))
            pantalla.blit(txt_nombre, (ANCHO // 2 - txt_nombre.get_width() // 2, ALTO // 2 + 10))
            pantalla.blit(txt_enter, (ANCHO // 2 - txt_enter.get_width() // 2, ALTO // 2 + 120))
            
        elif estado == "GAME_OVER":
            txt_go = fuente_pantallas.render("GAME OVER", True, ROJO)
            txt_fs = fuente_subtitulo.render(f"PUNTUACIÓN FINAL: {puntuacion}", True, BLANCO)
            txt_rest = fuente_subtitulo.render("Presiona 'R' para reiniciar", True, VERDE)
            pantalla.blit(txt_go, (ANCHO // 2 - txt_go.get_width() // 2, ALTO // 2 - 120))
            pantalla.blit(txt_fs, (ANCHO // 2 - txt_fs.get_width() // 2, ALTO // 2 - 40))
            pantalla.blit(txt_rest, (ANCHO // 2 - txt_rest.get_width() // 2, ALTO // 2 + 20))
            dibujar_boton("VER PUNTAJES", ANCHO//2 - 120, ALTO//2 + 100, 240, 50)
            
        elif estado == "VICTORIA":
            txt_vic = fuente_pantallas.render("¡CAMPAÑA COMPLETADA!", True, VERDE)
            txt_fs = fuente_subtitulo.render(f"PUNTUACIÓN PERFECTA: {puntuacion}", True, BLANCO)
            txt_rest = fuente_subtitulo.render("Presiona 'R' para jugar de nuevo", True, BLANCO)
            pantalla.blit(txt_vic, (ANCHO // 2 - txt_vic.get_width() // 2, ALTO // 2 - 120))
            pantalla.blit(txt_fs, (ANCHO // 2 - txt_fs.get_width() // 2, ALTO // 2 - 40))
            pantalla.blit(txt_rest, (ANCHO // 2 - txt_rest.get_width() // 2, ALTO // 2 + 20))
            dibujar_boton("VER PUNTAJES", ANCHO//2 - 120, ALTO//2 + 100, 240, 50)
            
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()