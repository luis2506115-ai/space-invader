import pygame
import sys
import os
from jugador import Jugador
from enemigo import Enemigo
from menu_puntajes import MenuPuntajes
from menu_principal import MenuPrincipal
from menu_acerca_de import MenuAcercaDe

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
# Fuente de texto más estilizada para el mensaje largo de felicitaciones
fuente_registro = pygame.font.SysFont("arial", 20, bold=True)

# --- SISTEMA DE PERSISTENCIA SEGURA ---
def obtener_maximo_puntaje(menu_leaderboard):
    lista = menu_leaderboard.cargar_puntajes()
    if lista:
        return lista[0][1] # Retorna la puntuación del primer lugar
    return 0

def guardar_puntaje(nombre, puntuacion):
    if puntuacion > 0: 
        directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        archivo = os.path.join(directorio_base, "puntajes.txt")
        with open(archivo, "a", encoding="utf-8") as f:
            # Formato exacto del cuaderno guía: nombre,puntuación
            f.write(f"{nombre},{puntuacion}\n")

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

    ruta_musica_menu = os.path.join(directorio_base, "assets", "music.mp3")
    ruta_musica_juego = os.path.join(directorio_base, "assets", "background_sound.mp3")
    ruta_explosion = os.path.join(directorio_base, "assets", "explosion.mp3")
    ruta_ganar = os.path.join(directorio_base, "assets", "ganar.mp3")
    
    musica_actual = ""
    def cambiar_musica(nueva_musica):
        nonlocal musica_actual
        if musica_actual != nueva_musica:
            try:
                if nueva_musica == "MENU":
                    pygame.mixer.music.load(ruta_musica_menu)
                elif nueva_musica == "JUEGO":
                    pygame.mixer.music.load(ruta_musica_juego)
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
                musica_actual = nueva_musica
            except pygame.error:
                pass

    cambiar_musica("MENU")

    try:
        sonido_explosion = pygame.mixer.Sound(ruta_explosion)
        sonido_explosion.set_volume(0.4)
    except FileNotFoundError:
        sonido_explosion = None

    # Carga del nuevo audio de victoria/récord
    try:
        sonido_ganar = pygame.mixer.Sound(ruta_ganar)
        sonido_ganar.set_volume(0.5)
    except FileNotFoundError:
        sonido_ganar = None

    menu_leaderboard = MenuPuntajes(pantalla)
    menu_inicio = MenuPrincipal(pantalla) 
    menu_acerca = MenuAcercaDe(pantalla)

    estado = "INICIO" 
    nivel = 1
    MAX_NIVELES = 9
    puntuacion = 0
    nombre_jugador = ""
    estado_post_ingreso = "" 
    es_record_maximo = False # Bandera para personalizar el texto en pantalla
    
    nave = Jugador(ANCHO // 2, ALTO - 50)
    grupo_sprites = pygame.sprite.Group()
    grupo_enemigos = pygame.sprite.Group()
    grupo_laseres = pygame.sprite.Group() 
    
    grupo_sprites.add(nave)
    generar_flota(nivel, grupo_sprites, grupo_enemigos)

    ejecutando = True
    while ejecutando:
        
        if estado == "INICIO":
            opcion_elegida = menu_inicio.ejecutar()
            if opcion_elegida == "Iniciar juego":
                estado = "JUGANDO"
                cambiar_musica("JUEGO")
            elif opcion_elegida == "Puntajes":
                menu_leaderboard.ejecutar()
            elif opcion_elegida == "Acerca de":
                menu_acerca.ejecutar()
            continue

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = evento.pos
                if estado in ["GAME_OVER", "VICTORIA"]:
                    if ANCHO//2 - 120 <= x <= ANCHO//2 + 120 and ALTO//2 + 100 <= y <= ALTO//2 + 150:
                        menu_leaderboard.ejecutar()

            elif evento.type == pygame.KEYDOWN:
                if estado == "JUGANDO":
                    if evento.key == pygame.K_SPACE:
                        nave.disparar(grupo_sprites, grupo_laseres)
                
                elif estado == "INGRESO_NOMBRE":
                    if evento.key == pygame.K_RETURN: 
                        if nombre_jugador.strip() == "":
                            nombre_jugador = "Anónimo"
                        guardar_puntaje(nombre_jugador, puntuacion)
                        estado = estado_post_ingreso
                    elif evento.key == pygame.K_BACKSPACE: 
                        nombre_jugador = nombre_jugador[:-1]
                    else:
                        if len(nombre_jugador) < 12 and evento.unicode.isprintable() and evento.unicode != ",":
                            nombre_jugador += evento.unicode
                            
                elif estado in ["GAME_OVER", "VICTORIA"]:
                    if evento.key == pygame.K_r:
                        estado = "INICIO"
                        cambiar_musica("MENU") 
                        nivel = 1
                        puntuacion = 0
                        nombre_jugador = "" 
                        es_record_maximo = False
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
            
            # --- EVALUACIÓN DE FIN DE PARTIDA ---
            def ir_a_registro(estado_final):
                nonlocal estado, estado_post_ingreso, es_record_maximo
                max_actual = obtener_maximo_puntaje(menu_leaderboard)
                
                # Validación de récord tal como pide el cuaderno
                if puntuacion > max_actual:
                    es_record_maximo = True
                    pygame.mixer.music.stop() # Pausa música ambiental
                    if sonido_ganar:
                        sonido_ganar.play() # Ejecuta sonido ganar.mp3
                
                estado = "INGRESO_NOMBRE"
                estado_post_ingreso = estado_final

            if len(grupo_enemigos) == 0:
                if nivel < MAX_NIVELES:
                    nivel += 1
                    grupo_laseres.empty()
                    grupo_sprites.empty()
                    grupo_sprites.add(nave)
                    generar_flota(nivel, grupo_sprites, grupo_enemigos)
                else:
                    ir_a_registro("VICTORIA")

            if pygame.sprite.spritecollideany(nave, grupo_enemigos):
                ir_a_registro("GAME_OVER")
            
            for enemigo in grupo_enemigos:
                if enemigo.rect.bottom >= ALTO - 40:
                    ir_a_registro("GAME_OVER")
                    break

        # --- CAPA DE RENDERIZADO ---
        if fondo:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(NEGRO)
            
        if estado == "JUGANDO":
            grupo_sprites.draw(pantalla)
            txt_score = fuente_hud.render(f"SCORE: {puntuacion}", True, BLANCO)
            txt_level = fuente_hud.render(f"LEVEL: {nivel}/{MAX_NIVELES}", True, VERDE)
            pantalla.blit(txt_score, (20, 20))
            pantalla.blit(txt_level, (ANCHO - 180, 20))
            
        elif estado == "INGRESO_NOMBRE":
            txt_ingreso = fuente_pantallas.render("FIN DE LA MISIÓN", True, BLANCO)
            
            # Mensaje condicional dinámico según el puntaje obtenido
            if es_record_maximo:
                msg = "¡Felicidades! Has superado el máximo puntaje. Por favor, ingresa tu nombre:"
                color_msg = VERDE
            else:
                msg = "Ingresa tu nombre de piloto para el registro de la federación:"
                color_msg = BLANCO
                
            txt_instruccion = fuente_registro.render(msg, True, color_msg)
            cursor = "_" if pygame.time.get_ticks() % 1000 < 500 else ""
            txt_nombre = fuente_pantallas.render(nombre_jugador + cursor, True, ROJO)
            txt_enter = fuente_subtitulo.render("Presiona ENTER para validar e ingresar", True, GRIS)
            
            pantalla.blit(txt_ingreso, (ANCHO // 2 - txt_ingreso.get_width() // 2, ALTO // 2 - 150))
            pantalla.blit(txt_instruccion, (ANCHO // 2 - txt_instruccion.get_width() // 2, ALTO // 2 - 50))
            pantalla.blit(txt_nombre, (ANCHO // 2 - txt_nombre.get_width() // 2, ALTO // 2 + 10))
            pantalla.blit(txt_enter, (ANCHO // 2 - txt_enter.get_width() // 2, ALTO // 2 + 120))
            
        elif estado == "GAME_OVER":
            cambiar_musica("MENU")
            txt_go = fuente_pantallas.render("GAME OVER", True, ROJO)
            txt_fs = fuente_subtitulo.render(f"PUNTUACIÓN FINAL: {puntuacion}", True, BLANCO)
            txt_rest = fuente_subtitulo.render("Presiona 'R' para regresar al menú principal", True, VERDE)
            pantalla.blit(txt_go, (ANCHO // 2 - txt_go.get_width() // 2, ALTO // 2 - 120))
            pantalla.blit(txt_fs, (ANCHO // 2 - txt_fs.get_width() // 2, ALTO // 2 - 40))
            pantalla.blit(txt_rest, (ANCHO // 2 - txt_rest.get_width() // 2, ALTO // 2 + 20))
            dibujar_boton("VER PUNTAJES", ANCHO//2 - 120, ALTO//2 + 100, 240, 50)
            
        elif estado == "VICTORIA":
            cambiar_musica("MENU")
            txt_vic = fuente_pantallas.render("¡CAMPAÑA COMPLETADA!", True, VERDE)
            txt_fs = fuente_subtitulo.render(f"PUNTUACIÓN PERFECTA: {puntuacion}", True, BLANCO)
            txt_rest = fuente_subtitulo.render("Presiona 'R' para iniciar un nuevo despliegue", True, BLANCO)
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