import pygame
import sys

# 1. Inicializar Pygame
pygame.init()

# 2. Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invader - IA Engineering")

# 3. Configuración del reloj (para controlar los FPS)
reloj = pygame.time.Clock()
FPS = 60

# Colores básicos (RGB)
NEGRO = (0, 0, 0)

def main():
    jugando = True
    
    # --- GAME LOOP ---
    while jugando:
        # A. Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
                
        # B. Lógica del juego (movimientos, colisiones, etc.)
        # (Por ahora vacío)
        
        # C. Renderizado (Dibujar en pantalla)
        pantalla.fill(NEGRO) # Limpiamos la pantalla con color negro
        
        # Actualizar la pantalla con lo que hemos dibujado
        pygame.display.flip()
        
        # Controlar la velocidad del bucle
        reloj.tick(FPS)

    # 4. Salir de forma limpia
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()