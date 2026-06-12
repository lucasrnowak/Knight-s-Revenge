import pygame

#===IMPORT ALL IMAGES===
#spritesheets NOT yet implemented

##WALLS/PATHS/DOORS
brick_wall = pygame.image.load("images/brick_wall.png")
path = pygame.image.load("images/path.png")
door_img = pygame.image.load("images/door.png")
inventory_slot_img = pygame.image.load("images/inventory_slot.png")

##HERO IMAGES
hero_img = pygame.image.load("images/hero_img.png")
hero_leftstep = pygame.image.load("images/hero_leftstep.png")
hero_rightstep = pygame.image.load("images/hero_rightstep.png")

hero_img_f = pygame.transform.flip(hero_img, True, False)
hero_leftstep_f = pygame.transform.flip(hero_leftstep, True, False)
hero_rightstep_f = pygame.transform.flip(hero_rightstep, True, False)

hero_with_sword = pygame.image.load("images/hero_with_sword.png")
hero_with_sword_leftstep = pygame.image.load("images/hero_with_sword_leftstep.png")
hero_with_sword_rightstep = pygame.image.load("images/hero_with_sword_rightstep.png")

hero_with_sword_f = pygame.transform.flip(hero_with_sword, True, False)
hero_with_sword_leftstep_f = pygame.transform.flip(hero_with_sword_leftstep, True, False)
hero_with_sword_rightstep_f = pygame.transform.flip(hero_with_sword_rightstep, True, False)

hero_with_bow = pygame.image.load("images/hero_with_bow.png")
hero_with_bow_leftstep = pygame.image.load("images/hero_with_bow_leftstep.png")
hero_with_bow_rightstep = pygame.image.load("images/hero_with_bow_rightstep.png")

hero_with_bow_f = pygame.transform.flip(hero_with_bow, True, False)
hero_with_bow_leftstep_f = pygame.transform.flip(hero_with_bow_leftstep, True, False)
hero_with_bow_rightstep_f = pygame.transform.flip(hero_with_bow_rightstep, True, False)

hero_with_staff = pygame.image.load("images/hero_with_staff.png")
hero_with_staff_leftstep = pygame.image.load("images/hero_with_staff_leftstep.png")
hero_with_staff_rightstep = pygame.image.load("images/hero_with_staff_rightstep.png")

hero_with_staff_f = pygame.transform.flip(hero_with_staff, True, False)
hero_with_staff_leftstep_f = pygame.transform.flip(hero_with_staff_leftstep, True, False)
hero_with_staff_rightstep_f = pygame.transform.flip(hero_with_staff_rightstep, True, False)

##ENEMY IMAGES
blob_img = pygame.image.load("images/blob.png")
blob_step = pygame.image.load("images/blob_step.png")

zombie_img = pygame.image.load("images/zombie.png")
zombie_leftstep = pygame.image.load("images/zombie_leftstep.png")
zombie_rightstep = pygame.image.load("images/zombie_rightstep.png")

zombie_img_f = pygame.transform.flip(zombie_img, True, False)
zombie_leftstep_f = pygame.transform.flip(zombie_leftstep, True, False)
zombie_rightstep_f = pygame.transform.flip(zombie_rightstep, True, False)

ghost_img = pygame.image.load("images/ghost.png")
ghost_step = pygame.image.load("images/ghost_step.png")

dragon_img = pygame.image.load("images/dragon.png")
dragon_step1 = pygame.image.load("images/dragon_step1.png")
dragon_step2 = pygame.image.load("images/dragon_step2.png")

##HEALTH BAR/GEMS
health_bar_imgs = [
    pygame.image.load("images/0_hit.png"),
    pygame.image.load("images/1_hit.png"),
    pygame.image.load("images/2_hit.png"),
    pygame.image.load("images/3_hit.png"),
    pygame.image.load("images/4_hit.png"),
    pygame.image.load("images/5_hit.png"),
    pygame.image.load("images/6_hit.png")
]

red_gem_img = pygame.image.load("images/red_gem_disp.png")
green_gem_img = pygame.image.load("images/green_gem_disp.png")
purple_gem_img = pygame.image.load("images/purple_gem_disp.png")

##WEAPONS
sword_img = pygame.image.load("images/sword.png")
bow_img = pygame.image.load("images/bow.png")
staff_img = pygame.image.load("images/staff.png")

##PROJECTILES
arrow_img_right = pygame.image.load("images/arrow.png")
arrow_img_up = pygame.transform.rotate(arrow_img_right, 90)
arrow_img_left = pygame.transform.rotate(arrow_img_right, 180)
arrow_img_down = pygame.transform.rotate(arrow_img_right, 270)

orb_img = pygame.image.load("images/orb.png")
fireball_img = pygame.image.load("images/fireball.png")
shadow_orb_img = pygame.image.load("images/shadow_orb.png")

##BLANK FOR PLACEHOLDER
blank_img = pygame.image.load("images/blank.png")
