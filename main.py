import pygame
from pygame.locals import *
import sys

#imports from my files
from settings import *
import assets
from helpers import *
from entities import *

#===CREATE ALL PERMANENT GAME SPRITES===

#player
hero = Hero((2,2))

#inventory slots
slot_1 = Inventory_slot((-2,5))
slot_2 = Inventory_slot((-1,5))
slot_3 = Inventory_slot((0,5))

#character health
healthbar = Healthbar((-1.5,0), hero)

#create screens
title = TitleScreen()
controls = ControlsScreen()
intro = IntroScreen()
game_win = GameWin()
game_over = GameOver()

#for FSM
state = 0

#GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #clean slate (avoids out-of-map blur)
    DISPLAY.fill((0,0,0))

    #FSM for game loading / movement between screens
    #-1: reset main room or boss room, depending on player progress
    #0: title screen and controls
    #1: intro text
    #2: load main room
    #3: main room gameplay
    #4: erase main sprites and load boss room
    #5: boss room gameplay
    #6: game won

    #MAKE AS MANY WHILES INSTEAD OF IFS!

    #GAME OVER STATE
    if (GameOver.true):

        game_over.update()
        game_over.draw()

    #RESET STATE
    elif (state == -1):

        if not MainRoom.done:
            main_room.reset()
        else:
            boss_room.reset()

    #TITLE SCREEN STATE
    elif (state == 0):
        
        title.update()
        controls.update()

        if (controls.true):
            controls.draw()
        elif (not title.done):
            title.draw()
        else: 
            state = 2
            intro.starting_time = pygame.time.get_ticks()

    #LOAD MAIN ROOM STATE
    elif (state == 1):

        intro.update()
        intro.draw()

        if (intro.done):
            state = 2

    #MAIN ROOM STATE
    elif (state == 2):

        main_room = MainRoom()
        state = 3

    elif (state == 3):

        if (not MainRoom.done):
            main_room.update()
            main_room.draw()
        else:
            main_room.end()
            state = 4
    
    #LOAD BOSS ROOM STATE
    elif (state == 4):

        boss_room = BossRoom()
        state = 5

    #BOSS ROOM STATE
    elif (state == 5):

        if (not BossRoom.done):
            boss_room.update()
            boss_room.draw()
        else: 
            state = 6

    #GAME WON STATE
    elif (state == 6):
        
        if not game_win.done:
            game_win.update()
            game_win.draw()
        else:
            state = 7

    #EXIT GAME STATE
    else:
        sys.exit()
    
    pygame.display.update()
    FPS.tick(frames)
