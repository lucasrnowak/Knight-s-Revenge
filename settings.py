import pygame

pygame.init()

#===SETTINGS===

#path size and window size
PATH_SIZE = 128
WIDTH = 1280
HEIGHT = 768

#create display
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAY.fill((0,0,0))

#offset for the hero in the main room
starting_camera_offset = (3*PATH_SIZE, 1*PATH_SIZE)

#initialize colors
BLACK = pygame.Color(0,0,0)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)

#initialize fonts
gabriola = pygame.font.SysFont("gabriola", 100)
lucidaconsole = pygame.font.SysFont("lucidaconsole", 25)

#set FPS
frames = 60
FPS = pygame.time.Clock()
