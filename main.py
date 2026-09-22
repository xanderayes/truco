import pygame
from game import JogoTrucoVisual

def main():
    pygame.init()
    
    # Configurações da janela
    WIDTH, HEIGHT = 1200, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Truco Paulista")
    
    # Cores
    VERDE_MESA = (34, 139, 34)
    PRETO = (0, 0, 0)
    
    # Inicializa o jogo
    jogo = JogoTrucoVisual(screen, WIDTH, HEIGHT)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            jogo.handle_event(event)
        
        # Atualiza e desenha
        jogo.update()
        jogo.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
