import pygame
from sys import exit

from game_board_screen import GameScreen

SCREEN_SIZE = (1200,800)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill('light gray')
pygame.display.set_caption("4 in a row")
pygame_icon = pygame.image.load("./img/game_icon.jpg").convert()
pygame.display.set_icon(pygame_icon)
clock = pygame.time.Clock()

game_board_screen = GameScreen(screen)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #if game_board_screen.game_state.is_running():
    game_board_screen.draw(events)

    pygame.display.update()
    clock.tick(60)

