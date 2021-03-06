#David
import pygame


def print_debug_info(screen, message, position):
    #display_surface = pygame.display.set_mode((100, 100))
    pygame.display.set_caption('Show Text')
    font = pygame.font.Font('freesansbold.ttf', 12)
    text = font.render(message, True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = position
    screen.blit(text, textRect)