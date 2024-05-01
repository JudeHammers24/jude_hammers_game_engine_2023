# This file was created by: Jude Hammers
# This code was inspired by Zelda and informed by Chris Bradfield

import pygame as pg
from settings import *
from settings import TILESIZE
from settings import GREEN
from settings import BROWN
from settings import YELLOW
from settings import PLAYER_SPEED
from settings import BGCOLOR
vec =pg.math.Vector2
# allows us to use pygame
# imports game settings


# player class
class Player(pg.sprite.Sprite):
    # creates the blueprint for the player
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        self.speed = 0
        self.max_speed = 600
        self.power_up_multiplier = 4
        # initializes the player class
        pg.sprite.Sprite.__init__(self, self.groups)
        # init super class
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # setting player dimensions
        self.image.fill(GREEN)
        # setting player color
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.x = x * TILESIZE
        self.y = y * TILESIZE


    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_groups('x')
        self.collide_with_groups('y')


    def collide_with_groups(self, dir, screen):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.mobs, False)
            if hits:
                self.show_start_screen(screen)

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        # Normalize diagonal movement
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071  # roughly 1/sqrt(2)
            self.vy *= 0.7071
    
    def check_internal_wall_collisions(self):
        # Check for collisions with internal walls within the game border
        internal_wall_collisions = pg.sprite.spritecollide(self, self.game.walls, False)
        print("Number of internal wall collisions:", len(internal_wall_collisions))
        return len(internal_wall_collisions) > 0

    def update(self):
        self.get_keys()
        
        # Update player's position based on velocity and time
        self.rect.x += self.vx * self.game.dt
        self.rect.y += self.vy * self.game.dt

        # Wrap player around the screen if no collisions with internal walls
        if not self.check_internal_wall_collisions():
            screen_width = self.game.screen.get_width()
            screen_height = self.game.screen.get_height()
            
            if self.rect.right < 0:  # If player moves off the left side of the screen
                self.rect.left = screen_width  # Move player to the right side
            elif self.rect.left > screen_width:  # If player moves off the right side of the screen
                self.rect.right = 0  # Move player to the left side

            if self.rect.bottom < 0:  # If player moves off the top of the screen
                self.rect.top = screen_height  # Move player to the bottom
            elif self.rect.top > screen_height:  # If player moves off the bottom of the screen
                self.rect.bottom = 0  # Move player to the top






    def apply_power_up(self):
        # Increase speed by a fraction
        self.speed *= self.power_up_multiplier
        self.speed = min(self.speed, self.max_speed)
    
   
    def draw_text(self, surface, text, size, color, x, y):
         font_name = pg.font.match_font('arial')
         font = pg.font.Font(font_name, size)
         text_surface = font.render(text, True, color)
         text_rect = text_surface.get_rect()
         text_rect.topleft = (x,y)
         surface.blit(text_surface, text_rect)
        

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
        
            
    
    def collide_with_groups(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.power_ups, False)
            if hits:
                self.apply_power_up()
                hits[0].kill()

    # def show_start_screen(self, screen):
    #      screen.fill(BGCOLOR)
    #      self.draw_text(screen, "Press any button to start game", 48, BLUE, WIDTH/4.3, HEIGHT/2.2)
    #      pg.display.flip()
    #      self.wait_for_key()
    

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # add wall to groups via the Sprite class parameter
        self.groups = game.all_sprites, game.walls
        # init superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        # add game to properties of wall class
        self.game = game
        # setup image in pygame using Surface class
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # fill the image
        self.image.fill(BLUE)
        # get the rectangular dimensions and locations using the get_rect method
        self.rect = self.image.get_rect()
        # create the x and y coordinate properties for use below
        self.x = x
        self.y = y
        # set the x and y coordinate properties using the rect from get_rect
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y

class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.mob_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(ORANGE)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # self.hit_rect = MOB_HIT_RECT.copy()
        # self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.chase_distance = 500
        # added
        self.speed = 200
        self.chasing = False
        # self.health = MOB_HEALTH
    def sensor(self):
        if abs(self.rect.x - self.game.player.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False
    def update(self):
        self.sensor()
        if self.chasing:
            self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
            # self.image = pg.transform.rotate(self.image, 45)
            # self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            # self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            # self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            # self.rect.center = self.hit_rect.center
            # if self.health <= 0:
            #     self.kill()