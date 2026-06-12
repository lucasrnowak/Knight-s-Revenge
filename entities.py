import pygame
from pygame.locals import *
import random

from settings import *
import assets
from helpers import *

#===ALL GAME CLASSES HERE===

#global all sprites group
#with layering for renders
all_sprites = pygame.sprite.LayeredUpdates()
#independent all_enemies group for attacking updates
all_enemies = pygame.sprite.Group()
GameOver = 0

# =====HERO=====
class Hero(pygame.sprite.Sprite):
    hero = None
    def __init__(self, pos):
        super().__init__()

        #initialize image, rect, position
        self._layer = 1
        self.image = assets.hero_img
        self.rect = pygame.Rect(0,0, 26*2, 54*2)
        self.rect.center = block_to_coord(pos[0], pos[1])

        self.in_still_room = 0

        #===HERO STATS===
        self.speed = 3
        self.health = 6
        #for taking damage
        self.damage_delay = 1000
        self.last_damage = 0
        #for attacks / interacts
        self.last_attack_time = 0
        self.attack_cooldown = 1000
        self.current_direction = 2
        #0 = punch (no weapon)
        self.weapon_equipped = 0
        #weapons collected?
        self.sword_collected = 0
        self.bow_collected = 0
        self.staff_collected = 0
        
        #===ANIMATION SPRITES===
        self.current_animation = 0
        self.normal_animations_r = [assets.hero_img, assets.hero_rightstep, assets.hero_img, assets.hero_leftstep]
        self.sword_animations_r = [assets.hero_with_sword, assets.hero_with_sword_rightstep, assets.hero_with_sword, assets.hero_with_sword_leftstep]
        self.bow_animations_r = [assets.hero_with_bow, assets.hero_with_bow_rightstep, assets.hero_with_bow, assets.hero_with_bow_leftstep]
        self.staff_animations_r = [assets.hero_with_staff, assets.hero_with_staff_rightstep, assets.hero_with_staff, assets.hero_with_staff_leftstep]
        self.normal_animations_l = [assets.hero_img_f, assets.hero_rightstep_f, assets.hero_img_f, assets.hero_leftstep_f]
        self.sword_animations_l = [assets.hero_with_sword_f, assets.hero_with_sword_rightstep_f, assets.hero_with_sword_f, assets.hero_with_sword_leftstep_f]
        self.bow_animations_l = [assets.hero_with_bow_f, assets.hero_with_bow_rightstep_f, assets.hero_with_bow_f, assets.hero_with_bow_leftstep_f]
        self.staff_animations_l = [assets.hero_with_staff_f, assets.hero_with_staff_rightstep_f, assets.hero_with_staff_f, assets.hero_with_staff_leftstep_f]
        #===ANIMATION VARIABLES===
        self.last_animation_update = 0
        self.animation_frame_delay = 150
        self.moving = 0
        #only for simplicity when parsing all_sprites
        #hero does not move against itself
        self.moves_with_hero = 0

        #===SPRITEGROUPS?===
        self.barriers = None
        all_sprites.add(self)

        #send to static class variable for easy access across other classes!
        Hero.hero = self
    
    def update(self):

        #===POSITION & ANIMATION UPDATE===
        pressed_keys = pygame.key.get_pressed()
        dx, dy = 0,0
        if pressed_keys[K_a]:
            dx += -self.speed
            self.current_direction = 0
        if pressed_keys[K_d]:
            dx += self.speed
            self.current_direction = 2
        if pressed_keys[K_w]:
            dy += -self.speed
            self.current_direction = 1
        if pressed_keys[K_s]:
            dy += self.speed
            self.current_direction = 3
        if (dx,dy) == (0,0): self.moving = 0
        else: self.moving = 1
        
        #===DIFFERENT MOVEMENT MECHANICS DEPENDING ON OCCUPIED ROOM===
        if self.in_still_room:
            self.rect.move_ip(dx,dy)
            if pygame.sprite.spritecollideany(self, self.barriers):
                self.rect.move_ip(-dx,-dy)

        else:
            for sprite in all_sprites:
                if sprite.moves_with_hero and not isinstance(sprite, Hero): sprite.rect.move_ip(-dx,-dy)
            if pygame.sprite.spritecollideany(self, self.barriers):
                for sprite in all_sprites:
                    if sprite.moves_with_hero and not isinstance(sprite, Hero): sprite.rect.move_ip(dx,dy)

        self.animate()

        #===INTERACTION UPDATE===
        #IF SPACE BAR IS PRESSED????!!?!??!?!??!
        current_time = pygame.time.get_ticks()
        if pressed_keys[K_SPACE]:
            if current_time - self.last_attack_time > self.attack_cooldown:
                self.last_attack_time = current_time
                if (self.weapon_equipped == 0 or self.weapon_equipped == 1):
                    Melee_attack(self, all_enemies)
                if (self.weapon_equipped == 2 or self.weapon_equipped == 3):
                    Projectile_attack(self, all_enemies, self.barriers)

        #===HELD WEAPON UPDATE===
        if (pressed_keys[K_1] and self.sword_collected == 1):
            self.weapon_equipped = 1
        elif (pressed_keys[K_2] and self.bow_collected == 1):
            self.weapon_equipped = 2
        elif (pressed_keys[K_3] and self.staff_collected == 1):
            self.weapon_equipped = 3

    def hit(self, damage):
        if pygame.time.get_ticks() - self.last_damage > self.damage_delay:
            self.last_damage = pygame.time.get_ticks()
            self.health -= damage
            if self.health <= 0:
                GameOver.true = 1

    def knockback(self):
        #could probably make a while loop here so that there is still some knockback upon wall collision
        dx,dy = 0,0
        if self.current_direction == 0: dx = 100
        elif self.current_direction == 1: dy = 100
        elif self.current_direction == 2: dx = -100
        elif self.current_direction == 3: dy = -100
        for sprite in all_sprites:
            if sprite.moves_with_hero: sprite.rect.move_ip(-dx,-dy)
        if pygame.sprite.spritecollideany(self, self.barriers):
            for sprite in all_sprites:
                sprite.rect.move_ip(dx,dy)

    def animate(self):
        if pygame.time.get_ticks() - self.last_animation_update > self.animation_frame_delay:
            self.last_animation_update = pygame.time.get_ticks()
            animation_set = self.normal_animations_r
            if self.weapon_equipped == 0:
                if self.current_direction == 2 or self.current_direction == 1 or self.current_direction == 3:
                    animation_set = self.normal_animations_r
                else: animation_set = self.normal_animations_l
            elif self.weapon_equipped == 1:
                if self.current_direction == 2 or self.current_direction == 1 or self.current_direction == 3:
                    animation_set = self.sword_animations_r
                else: animation_set = self.sword_animations_l
            elif self.weapon_equipped == 2:
                if self.current_direction == 2 or self.current_direction == 1 or self.current_direction == 3:
                    animation_set = self.bow_animations_r
                else: animation_set = self.bow_animations_l
            elif self.weapon_equipped == 3:
                if self.current_direction == 2 or self.current_direction == 1 or self.current_direction == 3:
                    animation_set = self.staff_animations_r
                else: animation_set = self.staff_animations_l
            if self.moving:
                self.current_animation = (self.current_animation+1)%len(animation_set)
            else: 
                self.current_animation = 0
            self.image = animation_set[self.current_animation]

# =====ATTACKS=====
class Attack(pygame.sprite.Sprite):
    all_attacks = pygame.sprite.Group()
    def __init__(self, attacker, targets):
        super().__init__()
        self._layer = 1
        self.moves_with_hero = 1
        self.attacker = attacker
        self.targets = targets
        self.image = assets.blank_img
        self.attack_velocity = (0,0)

        all_sprites.add(self)
        Attack.all_attacks.add(self)

    def update(self):
        pass

class Melee_attack(Attack):
    def __init__(self, attacker, targets):
        super().__init__(attacker, targets)
        self.rect = pygame.Rect(0,0, 100,100)

        if Hero.hero.weapon_equipped == 0: self.attack_damage = 0.5
        elif Hero.hero.weapon_equipped == 1: self.attack_damage = 1
        if attacker.current_direction == 0: self.rect.center = (attacker.rect.centerx - 50, attacker.rect.centery)
        elif attacker.current_direction == 1: self.rect.center = (attacker.rect.centerx, attacker.rect.centery - 75)
        elif attacker.current_direction == 2: self.rect.center = (attacker.rect.centerx + 50, attacker.rect.centery)
        elif attacker.current_direction == 3: self.rect.center = (attacker.rect.centerx, attacker.rect.centery + 75)

    def update(self):
        for target in self.targets:
            if pygame.sprite.collide_rect(self, target):
                target.hit(self.attack_damage)
                target.knockback()
        self.kill()

class Projectile_attack(Attack):
    def __init__(self, attacker, targets, barriers, angle=0):
        super().__init__(attacker, targets)

        self.barriers = barriers
        self.attack_speed = 5
        
        if isinstance(attacker, Hero):
            self.rect = pygame.Rect(0,0, 20,20)
            self.rect.center = attacker.rect.center

            if attacker.current_direction == 0: 
                self.attack_velocity = (-self.attack_speed, 0)
                self.image = assets.arrow_img_left
            elif attacker.current_direction == 1: 
                self.attack_velocity = (0, -self.attack_speed)
                self.image = assets.arrow_img_up
            elif attacker.current_direction == 2: 
                self.attack_velocity = (self.attack_speed, 0)
                self.image = assets.arrow_img_right
            elif attacker.current_direction == 3: 
                self.attack_velocity = (0, self.attack_speed)
                self.image = assets.arrow_img_down

            if Hero.hero.weapon_equipped == 2: self.attack_damage = 1
            #replace arrow image if the attack is an orb from the staff
            if Hero.hero.weapon_equipped == 3: 
                self.attack_damage = 5
                self.image = assets.orb_img
        
        if isinstance(attacker, Ghost):
            self.image = assets.shadow_orb_img
            self.rect = pygame.Rect(0,0, 25,25)
            self.rect.center = attacker.rect.center
            self.attack_damage = 1

            if attacker.direction == 0: self.attack_velocity = (-self.attack_speed, 0)
            elif attacker.direction == 1: self.attack_velocity = (0, -self.attack_speed)
            elif attacker.direction == 2: self.attack_velocity = (self.attack_speed, 0)
            elif attacker.direction == 3: self.attack_velocity = (0, self.attack_speed)

        if isinstance(attacker, Dragon):
            self.image = assets.fireball_img
            self.rect = pygame.Rect(0,0, 20,20)
            self.rect.center = attacker.rect.topleft
            self.attack_damage = 1
            self.attack_velocity = (-self.attack_speed, random.randrange(0, self.attack_speed))

    def update(self):
        self.rect.move_ip(self.attack_velocity[0], self.attack_velocity[1])
        for target in self.targets:
            if pygame.sprite.collide_rect(self, target):
                target.hit(self.attack_damage)
                self.kill()
        if pygame.sprite.spritecollideany(self, self.barriers):
            self.kill()

#plenty of shit in this class that can be moved around
#so that super is called later and lines are saved
# =====ENEMIES=====
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self._layer = 1
        self.moves_with_hero = 1
        self.rect.center = block_to_coord(pos[0], pos[1])
        self.direction = 0
        self.target = Hero.hero
        self.physical_damage = 1
        
        #timing for taking attacks from player
        self.moving = 1
        self.knockback_timer = 500
        self.last_hit = 0

        self.barriers = None

        #animations
        self.current_animation = 0
        self.last_update = 0
        self.frame_delay = 150
        self.animation_cycle = []

        #enemy sprite groups
        all_sprites.add(self)
        all_enemies.add(self)

        #create a sprite for its boundaries that will be added to moving group
        self.bounds = pygame.sprite.Sprite()
        self.bounds.rect = pygame.Rect(0,0, self.actual_bounds[0], self.actual_bounds[1])
        self.bounds.rect.center = self.rect.center
        self.bounds.moves_with_hero = 1
        self.bounds.image = assets.blank_img
        all_sprites.add(self.bounds)

    def update(self):

        #===MOVEMENT===
        self.old_position = self.rect.copy()
        if (self.moving):
            dx,dy = 0,0
            #move in current direction
            if (self.direction == 0): dx = -self.speed
            elif (self.direction == 1): dy = -self.speed
            elif (self.direction == 2): dx = self.speed
            elif (self.direction == 3): dy = self.speed
            self.rect.move_ip(dx, dy)
            #if an enemy reaches out of its own bounds, its direction simply changes OR
            #if a wall collision occurs, replace enemy at old location and move its direction so it does not get stuck
            if self.out_of_bounds() or pygame.sprite.spritecollideany(self, self.barriers):
                self.rect = self.old_position
                self.direction = (self.direction+1)%4
        elif (not self.moving):
            if (pygame.time.get_ticks() - self.last_hit > self.knockback_timer):
                self.moving = 1

        #===PHYSICAL ATTACKS===
        #by physical attack, this implies the player got too close to an enemy, thus causing damage
        if pygame.sprite.collide_rect(self, Hero.hero):
            Hero.hero.hit(self.physical_damage)

        #===PROJECTILE ATTACKS===
        if isinstance(self, Ghost):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot > self.shoot_cooldown:
                self.last_shot = current_time
                self.ghost_attack()

        #===ANIMATIONS===
        self.animate()

    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.frame_delay:
            self.last_update = current_time
            self.current_animation = (self.current_animation+1)%len(self.animation_cycle)
            if isinstance(self, Zombie):
                self.image = self.animation_cycle[int(self.direction/2)][self.current_animation]
            else:
                self.image = self.animation_cycle[self.current_animation]

    def out_of_bounds(self):
        if not self.rect.colliderect(self.bounds.rect):
            return True
        else: return False

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            if isinstance(self, Dragon):
                BossRoom.done = 1
            self.kill()

    def knockback(self):
        old_position = self.rect.copy()
        self.last_hit = pygame.time.get_ticks()
        self.moving = 0
        dx,dy = 0,0
        #target points to hero, which is also inherently the attacker to any enemy
        if self.target.current_direction == 0: dx = -100
        elif self.target.current_direction == 1: dy = -100
        elif self.target.current_direction == 2: dx = 100
        elif self.target.current_direction == 3: dy = 100
        self.rect.move_ip(dx,dy)
        if pygame.sprite.spritecollideany(self, self.barriers):
            self.rect = old_position

class Blob(Enemy):
    def __init__(self, pos):
        self.hitbox = (50,10)
        #assign rect before calling parent __init__ since it needs rect
        self.rect = pygame.Rect(0,0, self.hitbox[0], self.hitbox[1])
        self.bounds = (1,1)
        self.actual_bounds = block_to_coord(self.bounds[0], self.bounds[1])
        super().__init__(pos)
        self.image = assets.blob_img
        self.speed = 1
        self.health = 2

        self.animation_cycle = [assets.blob_img, assets.blob_step]

class Zombie(Enemy):
    def __init__(self, pos):
        self.hitbox = (40,80)
        self.rect = pygame.Rect(0,0, self.hitbox[0], self.hitbox[1])
        self.bounds = (1,1)
        self.actual_bounds = block_to_coord(self.bounds[0], self.bounds[1])
        super().__init__(pos)
        self.image = assets.blob_img
        self.speed = 3
        self.health = 4
        self.physical_damage = 2

        self.zombie_animations_l = [assets.zombie_img_f, assets.zombie_rightstep_f, assets.zombie_img_f, assets.zombie_leftstep_f]
        self.zombie_animations_r = [assets.zombie_img, assets.zombie_rightstep, assets.zombie_img, assets.zombie_leftstep]
        self.animation_cycle = [self.zombie_animations_l, self.zombie_animations_r]

class Ghost(Enemy):
    def __init__(self, pos):
        self.hitbox = (40,80)
        self.rect = pygame.Rect(0,0, self.hitbox[0], self.hitbox[1])
        self.bounds = (1,1)
        self.actual_bounds = block_to_coord(self.bounds[0], self.bounds[1])
        super().__init__(pos)
        self.image = assets.blob_img
        self.speed = 2
        self.health = 3
        self.projectile_damage = 0.5

        self.shoot_cooldown = 2500
        self.last_shot = 0

        self.animation_cycle = [assets.ghost_img, assets.ghost_step]

    def ghost_attack(self):
        #pass target as list for structure of method in Projectile class
        Projectile_attack(self, [self.target], self.barriers)

class Dragon(Enemy):
    def __init__(self, pos):
        self.hitbox = (200,300)
        self.rect = pygame.Rect(0,0, self.hitbox[0], self.hitbox[1])
        self.bounds = (1,1)
        self.actual_bounds = block_to_coord(self.bounds[0], self.bounds[1])
        super().__init__(pos)
        self.image = assets.dragon_img
        self.speed = 3
        self.health = 100
        self.physical_damage = 6
        self.projectile_damage = 1

        #movement variables
        self.last_direction_change = 0
        self.direction_timer = 2000

        #attack variables
        self.shot_cooldown = 2000
        self.last_shot = 0

        self.animation_cycle = [assets.dragon_img, assets.dragon_step1, assets.dragon_img, assets.dragon_step2]

    #===SPECIALIZED MOVEMENT FOR DRAGON===
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_direction_change > self.direction_timer:
            self.last_direction_change = current_time
            self.direction = random.randint(0,3)

        #now run the parent update()
        super().update()

        #===DRAGON ATTACK===
        if current_time - self.last_shot > self.shot_cooldown:
            self.last_shot = current_time
            Projectile_attack(self, [self.target], self.barriers)
            Projectile_attack(self, [self.target], self.barriers)
            Projectile_attack(self, [self.target], self.barriers)

# =====WEAPONS=====
class Weapon(pygame.sprite.Sprite):
    weapon_list = [None, None, None]
    def __init__(self, pos):
        super().__init__()
        self._layer = 2
        self.moves_with_hero = 1
        self.rect = pygame.Rect(0,0, 100,100)
        self.rect.center = block_to_coord(pos[0], pos[1])
        self.collected = 0
        self.inventory_slot = None

        all_sprites.add(self)

    def update(self):
        if pygame.sprite.collide_rect(self, Hero.hero):
            self.moves_with_hero = 0
            self.collected = 1
            self.rect.center = block_to_coord(self.inventory_slot[0], self.inventory_slot[1])
            self.collect()

    def collect(self):
        pass

class Sword(Weapon):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = assets.sword_img
        self.inventory_slot = (-2,5)
        Weapon.weapon_list[0] = self

    def collect(self):
        Hero.hero.sword_collected = 1

class Bow(Weapon):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = assets.bow_img
        self.inventory_slot = (-1,5)
        Weapon.weapon_list[1] = self

    def collect(self):
        Hero.hero.bow_collected = 1

class Staff(Weapon):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = assets.staff_img
        self.inventory_slot = (0,5)
        Weapon.weapon_list[2] = self

    def collect(self):
        Hero.hero.staff_collected = 1

# =====BOSS DOOR=====
class Door(pygame.sprite.Sprite):
    def __init__(self, block):
        super().__init__()
        self._layer = 2
        self.moves_with_hero = 1

        self.image = assets.door_img
        self.rect = pygame.Rect(0,0, PATH_SIZE, PATH_SIZE)
        self.rect.center = block_to_coord(block[0], block[1])

        all_sprites.add(self)
    
    def update(self):
        if pygame.sprite.collide_rect(self, Hero.hero):
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[K_SPACE] and Gem.gems_collected:
                self.kill()
                self.complete_main_room()
    
    def complete_main_room(self):
        MainRoom.done = 1

# =====GEM COLLECTIBLES=====
class Gem(pygame.sprite.Sprite):

    gems_collected = 0

    red_collected = 0
    green_collected = 0
    purple_collected = 0

    def __init__(self, pos):
        super().__init__()
        self._layer = 1
        self.moves_with_hero = 1
        self.rect = pygame.Rect(0,0, 50,50)
        self.pos = pos

        all_sprites.add(self)

    def update(self):
        if pygame.sprite.collide_rect(self, Hero.hero):
            self.moves_with_hero = 0
            self.collect()
            Gem.gems_collected = Gem.red_collected and Gem.green_collected and Gem.purple_collected

class Red_gem(Gem):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = assets.red_gem_img
        self.rect.center = block_to_coord(pos[0], pos[1])

    def collect(self):
        Gem.red_collected = 1
        self.rect.center = block_to_coord(6,0)

class Green_gem(Gem):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = assets.green_gem_img
        self.rect.center = block_to_coord(pos[0], pos[1])

    def collect(self):
        Gem.green_collected = 1
        self.rect.center = block_to_coord(6.5,0)

class Purple_gem(Gem):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = assets.purple_gem_img
        self.rect.center = block_to_coord(pos[0], pos[1])

    def collect(self):
        Gem.purple_collected = 1
        self.rect.center = block_to_coord(7,0)

# =====INVENTORY SLOTS=====
class Inventory_slot(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self._layer = 1
        self.moves_with_hero = 0
        self.image = assets.inventory_slot_img
        self.rect = self.image.get_rect()
        self.rect.center = block_to_coord(pos[0], pos[1])
        all_sprites.add(self)

# =====HEALTHBAR=====
class Healthbar(pygame.sprite.Sprite):
    
    def __init__(self, pos, hero):
        super().__init__()
        self._layer = 1
        self.moves_with_hero = 0
        self.image = assets.health_bar_imgs[6]
        self.rect = self.image.get_rect()
        self.rect.center = block_to_coord(pos[0], pos[1])
        self.reference = hero

        all_sprites.add(self)

    def update(self):
        self.image = assets.health_bar_imgs[self.reference.health]

# =====SCREENS=====
class Screen():
    def __init__(self):
        self.done = 0
    def update(self):
        pass

class TitleScreen(Screen):
    def __init__(self):
        super().__init__()
        self.background = pygame.sprite.Group()
        for x in range(0,10):
            for y in range(0,6):
                new_block = pygame.sprite.Sprite()
                new_block.image = assets.brick_wall
                new_block.rect = pygame.Rect(x*PATH_SIZE,y*PATH_SIZE, PATH_SIZE,PATH_SIZE)
                self.background.add(new_block)
        self.title_text = gabriola.render("KNIGHT'S REVENGE", False, GREEN)
        self.title_rect = self.title_text.get_rect(center=(WIDTH/2, HEIGHT/2-140))
        self.text1 = lucidaconsole.render("ENTER - Begin game", True, GREEN)
        self.text2 = lucidaconsole.render("x - View controls", True, GREEN)
        self.text1_rect = self.text1.get_rect(center=(WIDTH/2,HEIGHT/2+30))
        self.text2_rect = self.text2.get_rect(center=(WIDTH/2,HEIGHT/2+60))

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_RETURN]:
            self.done = 1

    def draw(self):
        for sprite in self.background:
            DISPLAY.blit(sprite.image, sprite.rect)
        DISPLAY.blit(self.title_text, self.title_rect)
        DISPLAY.blit(self.text1, self.text1_rect)
        DISPLAY.blit(self.text2, self.text2_rect)

class ControlsScreen(Screen):
    def __init__(self):
        super().__init__()
        self.true = 0
        self.background = pygame.sprite.Group()
        for x in range(0,10):
            for y in range(0,6):
                new_block = pygame.sprite.Sprite()
                new_block.image = assets.brick_wall
                new_block.rect = pygame.Rect(x*PATH_SIZE,y*PATH_SIZE, PATH_SIZE,PATH_SIZE)
                self.background.add(new_block)
        self.text = [
            "CONTROLS",
            "--------",
            "w - up",
            "a - left",
            "s - down",
            "d - right",
            "space - attack / interact",
            "1 - select sword (if obtained)",
            "2 - select bow (if obtained)",
            "3 - select staff (if obtained)",
            "",
            "Attacking with no weapon will still do some melee damage.",
            "",
            "Hint: The staff is the most powerful weapon!",
            "",
            "Another (bigger) hint: You must acquire all three gems before opening the door!!!"
            "",
            "",
            "",
            "",
            "ESC - exit"
        ]   
    
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_x]:
            self.true = 1
        if pressed_keys[K_ESCAPE]:
            self.true = 0

    def draw(self):
        for sprite in self.background:
            DISPLAY.blit(sprite.image, sprite.rect)
        y = 50
        for line in self.text:
            text = lucidaconsole.render(line, True, GREEN)
            DISPLAY.blit(text, (100, y))
            y += 30

class IntroScreen(Screen):
    def __init__(self):
        super().__init__()
        self.text = [
            "You are a midieval knight",
            "from the year 1527.",
            "It is your duty to recover your",
            "family's stolen power gems.",
            "The thief is a cunning young wizard with",
            "his powerful guardian at the dungeon's exit.",
            "You must collect the gems and",
            "defeat the guardian to succeed.",
            "Good luck."
        ]
        self.starting_time = 0
        self.line1 = ""
        self.line2 = ""
        self.render1 = 0
        self.render2 = 0
        self.rect1 = pygame.Rect(0,0, 0,0)
        self.rect2 = pygame.Rect(0,0, 0,0)
    
    def update(self):
        self.time = pygame.time.get_ticks()
        if (self.time - self.starting_time < 5000):
            self.line1 = self.text[0]
            self.line2 = self.text[1]
        elif (self.time - self.starting_time < 10000):
            self.line1 = self.text[2]
            self.line2 = self.text[3]
        elif (self.time - self.starting_time < 15000):
            self.line1 = self.text[4]
            self.line2 = self.text[5]
        elif (self.time - self.starting_time < 20000):
            self.line1 = self.text[6]
            self.line2 = self.text[7]
        elif (self.time - self.starting_time < 25000):
            self.line1 = self.text[8]
            self.line2 = ""
        else: self.done = 1
        self.render1 = lucidaconsole.render(self.line1, True, GREEN)
        self.render2 = lucidaconsole.render(self.line2, True, GREEN)
        self.rect1 = self.render1.get_rect(center=(WIDTH/2,HEIGHT/2-25))
        self.rect2 = self.render2.get_rect(center=(WIDTH/2,HEIGHT/2+25))

    def draw(self):
        DISPLAY.blit(self.render1, self.rect1)
        DISPLAY.blit(self.render2, self.rect2)

class MainRoom(Screen):
    done = 0
    def __init__(self):
        super().__init__()

        blocked_map =  [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
                        [0,1,0,1,0,0,0,0,0,1,1,1,0,1,1,1,1,0,0],
                        [0,1,0,1,0,0,0,1,0,1,1,1,0,0,0,0,1,0,0],
                        [0,1,0,1,0,0,0,1,0,1,1,1,0,1,1,0,1,0,0],
                        [0,1,0,1,1,1,1,1,0,0,0,0,0,1,1,0,1,1,0],
                        [0,1,0,1,0,0,0,0,0,1,1,1,1,1,1,0,1,0,0],
                        [0,1,0,1,0,1,1,1,0,1,1,1,1,0,0,0,1,0,0],
                        [0,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1,0,0],
                        [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

        self.map = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()

        x = len(blocked_map[0])
        y = len(blocked_map)
        create_map(x, y, blocked_map, self.map, 1, 1)
        create_barriers(x, y, blocked_map, self.barriers, 1, 1)

        all_sprites.add(self.map)
        all_sprites.add(self.barriers)

        #create character weapons
        Sword((6,8))
        Bow((8,4))
        Staff((14,5))

        #create gem collectibles
        Red_gem((8,8))
        Green_gem((11,5))
        Purple_gem((15,5))

        #spawn enemies
        blobs = [(6,6), (7,9), (10,4), (11,8), (12,4), (17,10)]
        zombies = [(6,2), (11,3), (12,7)]
        ghosts = [(10,7), (10,10), (15,7)]

        for coord in blobs:
            Blob(coord)
        for coord in zombies:
            Zombie(coord)
        for coord in ghosts:
            Ghost(coord)
        
        #set barriers for any moving entities
        Hero.hero.barriers = self.barriers
        for sprite in all_enemies:
            sprite.barriers = self.barriers

        #create door to the boss room
        self.boss_door = Door((18,6))

    def update(self):
        #display new appearance / individual movements for all sprites
        #also centers images on hitbox / rect
        for sprite in all_sprites:
            sprite.update()

    def draw(self):
        for sprite in all_sprites:
            DISPLAY.blit(sprite.image, sprite.image.get_rect(center=sprite.rect.center))

    def end(self):
        for sprite in all_enemies:
            sprite.kill()
        for sprite in self.map:
            sprite.kill()
        for sprite in self.barriers:
            sprite.kill()

class BossRoom(Screen):
    done = 0
    def __init__(self):
        super().__init__()

        #create new layout
        boss_room_map = [[0,0,0,0,0,0,0,0,0,0],
                         [0,1,1,1,1,1,1,1,1,0],
                         [0,1,1,1,1,1,1,1,1,0],
                         [0,1,1,1,1,1,1,1,1,0],
                         [0,1,1,1,1,1,1,1,1,0],
                         [0,0,0,0,0,0,0,0,0,0]]
        
        x = len(boss_room_map[0])
        y = len(boss_room_map)

        self.map = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()

        create_map(x, y, boss_room_map, self.map, 0, 0)
        create_barriers(x, y, boss_room_map, self.barriers, 0, 0)

        for sprite in self.map:
            all_sprites.add(sprite)
        for sprite in self.barriers:
            all_sprites.add(sprite)

        #move hero into room
        Hero.hero.rect.center = block_to_coord(-1,2.5)

        #set barriers for any moving entities
        Hero.hero.barriers = self.barriers
        Hero.hero.in_still_room = 1

        self.boss = Dragon((5,2))
        self.boss.moves_with_hero = 0
        self.boss.barriers = self.barriers

        all_sprites.add(Hero.hero, self.boss)

    def update(self):
        for sprite in all_sprites:
            sprite.update()

    def draw(self):
        for sprite in all_sprites:
            DISPLAY.blit(sprite.image, sprite.image.get_rect(center=sprite.rect.center))

class GameWin(Screen):
    def __init__(self):
        super().__init__()
        self.text1 = lucidaconsole.render("Congratulations!", True, GREEN)
        self.text2 = lucidaconsole.render("You have slain the dungeon guardian and", True, GREEN)
        self.text3 = lucidaconsole.render("your family's treasures have been returned.", True, GREEN)
        self.text4 = lucidaconsole.render("Press esc to exit.", True, GREEN)
        self.text1_rect = self.text1.get_rect(center=(WIDTH/2,HEIGHT/2-50))
        self.text2_rect = self.text2.get_rect(center=(WIDTH/2,HEIGHT/2-25))
        self.text3_rect = self.text3.get_rect(center=(WIDTH/2,HEIGHT/2))
        self.text4_rect = self.text4.get_rect(center=(WIDTH/2,HEIGHT/2+50))

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            self.done = 1

    def draw(self):
        DISPLAY.blit(self.text1, self.text1_rect)
        DISPLAY.blit(self.text2, self.text2_rect)
        DISPLAY.blit(self.text3, self.text3_rect)
        DISPLAY.blit(self.text4, self.text4_rect)

class GameOver(Screen):
    true = 0
    def __init__(self):
        super().__init__()
        self.disp = gabriola.render("GAME OVER", False, RED)
        self.rect = self.disp.get_rect(center=(WIDTH/2, HEIGHT/2-100))
        self.text = lucidaconsole.render("Press enter to respawn", True, GREEN)
        self.text_rect = self.text.get_rect(center=(WIDTH/2, HEIGHT/2+100))

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_RETURN]:

            #return player to proper location
            Hero.hero.health = 6
            GameOver.true = 0

    def draw(self):
        DISPLAY.blit(self.disp, self.rect)
        DISPLAY.blit(self.text, self.text_rect)
