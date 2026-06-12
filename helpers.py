import pygame
from settings import *
import assets

#===ALL HELPER FUNCTIONS===
#most functions are constructed as class methods within entities.py

def block_to_coord(x, y):
    """Called when an entity needs to be placed in a specific location on the map. Converts an
    easily understood map coordinate to a pixel value.

    """
    return (PATH_SIZE*((2*x-1)/2)+starting_camera_offset[0], PATH_SIZE*((2*y-1)/2)+starting_camera_offset[1])

#creates images for rendering
def create_map(x, y, list, sprite_group, moves_with_hero, main_room):
    """Builds the visual map for any room. Does not include physical barriers.

    Parameters:
    -x (width) and y (height) of the map
    -2D list, containing 0s and 1s, representing either barriers or walkable paths, respectively
    -sprite_group to which each new_wall sprite will be added
    -moves_with_hero, to determine whether the room moves upon hero movement, or if the hero itself moves (scrolling room versus static)
    -main_room, a simple bool determining the camera offset of the room

    """
    if main_room: offset = starting_camera_offset
    else: offset = (0,0)
    for row in range(y):
        for col in range(x):
            if list[row][col] == 0:
                new_wall = pygame.sprite.Sprite()
                new_wall._layer = 0
                new_wall.moves_with_hero = moves_with_hero
                new_wall.image = assets.brick_wall
                new_wall.rect = pygame.Rect(col*PATH_SIZE+offset[0], row*PATH_SIZE+offset[1], PATH_SIZE, PATH_SIZE)
                sprite_group.add(new_wall)
            if list[row][col] == 1:
                new_wall = pygame.sprite.Sprite()
                new_wall._layer = 0
                new_wall.moves_with_hero = moves_with_hero
                new_wall.image = assets.path
                new_wall.rect = pygame.Rect(col*PATH_SIZE+offset[0], row*PATH_SIZE+offset[1], PATH_SIZE, PATH_SIZE)
                sprite_group.add(new_wall)

#stores actual barriers (sprite rects)
def create_barriers(x, y, list, sprite_group, moves_with_hero, main_room):
    """Identical concept to the above, but these sprites are created to represents the actual physical, invisible barriers. Walls
    and barriers are only separated due to the structure of the program (drawings of all_sprites became an issue), and in another iteration
    would certainly just be combined.

    """
    if main_room: offset = starting_camera_offset
    else: offset = (0,0)
    for row in range(y):
        for col in range(x):
            if list[row][col] == 0:
                new_wall = pygame.sprite.Sprite()
                new_wall.moves_with_hero = moves_with_hero
                new_wall.image = assets.blank_img
                new_wall.rect = pygame.Rect(col*PATH_SIZE+offset[0], row*PATH_SIZE+offset[1], PATH_SIZE, PATH_SIZE)
                sprite_group.add(new_wall)
