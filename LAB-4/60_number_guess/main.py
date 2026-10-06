import pygame
from game.game_engine import GameEngine


WIDTH = 620
HEIGHT = 380
FPS = 60


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Number Guessing Game - Pygame Edition")

    clock = pygame.time.Clock()

    engine = GameEngine(WIDTH, HEIGHT)

    running = True

    while running:

        # Handle events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            engine.handle_event(event)

        # Update game
        engine.update()

        # Draw game
        engine.render(screen)

        # Update display
        pygame.display.flip()

        # Maintain FPS
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()