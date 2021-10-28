import pygame
import os
from pygame.locals import *
from sys import exit

SCREEN_WIDTH = 800
SCREEN_HEIGTH = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption('PicaPau do Iguacu')

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75

#ESCALAS
WOOD_IDLE = 0.4
WOOD_JUMP = 0.45
WOOD_ATTACK = 0.47
BULLET_SCALE = 0.3

#variaveis do jogador
moving_left = False
moving_rigth = False
shoot = False

#carrega imagens
#bala
bullet_img = pygame.image.load('images/bullet/0.png').convert_alpha()



BG = (144, 201, 120)
RED = (255, 0, 0)


def draw_bg():
  screen.fill(BG)
  pygame.draw.line(screen, RED, (0, 455), (SCREEN_WIDTH, 455))


class Character(pygame.sprite.Sprite):
  def __init__(self, char_type, x, y, scale, speed, ammo):
    pygame.sprite.Sprite.__init__(self)
    self.alive = True
    self.speed = speed
    self.ammo = ammo
    self.start_ammo = ammo
    self.shoot_cooldown = 0
    self.health = 10
    self.max_health = self.health
    self.direction = 1
    self.vel_y = 0
    self.jump = False
    self.in_air = True
    self.flip = False
    self.animation_list = []
    self.frame_index = 0
    self.action = 0
    self.update_time = pygame.time.get_ticks()

    animation_types = ['idle', 'walk', 'jump', 'attack', 'hurt'] 
    for animation in animation_types:
      
      if char_type == "wood":
        temp_list = []
        num_of_frames = len(os.listdir(f'images/{char_type}/{animation}'))

        for i in range(num_of_frames):
          img = pygame.image.load(f'images/{char_type}/{animation}/{i}.png').convert_alpha()
          if animation == 'idle':
            img = pygame.transform.scale(img, (int(img.get_width() * WOOD_IDLE), int(img.get_height()* WOOD_IDLE)))
          elif animation == 'jump':
            img = pygame.transform.scale(img, (int(img.get_width() * WOOD_JUMP), int(img.get_height()* WOOD_JUMP)))
          elif animation == 'attack':
            img = pygame.transform.scale(img, (int(img.get_width() * WOOD_ATTACK), int(img.get_height()* WOOD_ATTACK)))
          else:
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height()* scale)))
          temp_list.append(img)
        self.animation_list.append(temp_list)

      if char_type == "guarda3":
        temp_list = []
        num_of_frames = len(os.listdir(f'images/{char_type}/{animation}'))

        for i in range(num_of_frames):
          img = pygame.image.load(f'images/{char_type}/{animation}/{i}.png').convert_alpha()
          img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height()* scale)))
          temp_list.append(img)
        self.animation_list.append(temp_list)
      
    self.image = self.animation_list[self.action][self.frame_index]
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)

  def update(self):
    self.update_animation()
    self.check_alive()
    if self.shoot_cooldown > 0:
      self.shoot_cooldown -= 1  

  def move(self, moving_left, moving_rigth):
    dx = 0
    dy = 0

    if moving_left:
      dx = -self.speed
      self.flip = True
      self.direction = -1
    if moving_rigth:
      dx = self.speed
      self.flip = False
      self.direction = 1
    
    if self.jump == True and self.in_air == False:
      self.vel_y = -11
      self.jump = False
      self.in_air = True

    
    self.vel_y += GRAVITY
    if self.vel_y > 10:
      self.vel_y
    dy += self.vel_y

    if self.rect.bottom + dy > 455:
      dy = 455 - self.rect.bottom
      self.in_air = False


    self.rect.x += dx
    self.rect.y += dy

  def shoot(self):
    if self.shoot_cooldown == 0 and self.ammo > 0:
      self.shoot_cooldown = 20
      self.update_action(3)
      bullet = Bullet(self.rect.centerx + (self.rect.size[0] + self.direction), self.rect.centery, self.direction)
      bullet_group.add(bullet)
      self.ammo -= 1


  def update_animation(self):
    ANIMATION_COOLDOWN = 100

    self.image = self.animation_list[self.action][self.frame_index]

    if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
      self.update_time = pygame.time.get_ticks()
      self.frame_index += 1
    if self.frame_index >= len(self.animation_list[self.action]):
      if self.action == 4:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
    

  def update_action(self, new_action):
    if new_action != self.action:
      self.action = new_action
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def check_alive(self):
    if self.health <= 0:
      self.health = 0
      self.speed = 0
      self.alive = False
      self.update_action(4)

  def draw(self):
    screen.blit(pygame.transform.flip(self.image ,self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
  def __init__(self, x, y, direction):
    pygame.sprite.Sprite.__init__(self)
    self.speed = 10
    self.image = pygame.transform.scale(bullet_img, (int(bullet_img.get_width() * BULLET_SCALE), int(bullet_img.get_height()* BULLET_SCALE)))
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.direction = direction

  def update(self):
    self.rect.x += (self.direction * self.speed)
    if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
      self.kill()

    if pygame.sprite.spritecollide(player, bullet_group, False):
      if player.alive:
        player.health -= 1
        self.kill()
    if pygame.sprite.spritecollide(enemy, bullet_group, False):
      if enemy.alive:
        enemy.health -= 3
        self.kill()


 
#grupo de sprites
bullet_group = pygame.sprite.Group()



player = Character('wood' ,200, 400, 0.6, 5, 5)
enemy = Character('guarda3', 400, 387, 0.1, 5, 5)


run = True
while run:

  clock.tick(FPS)
  
  draw_bg()

  player.update()
  player.draw()

  enemy.update()
  enemy.draw()

#carrega grupo de sprites
  bullet_group.update()
  bullet_group.draw(screen)
  
  if player.alive:
    if shoot:
      player.shoot()
    elif player.in_air:
      player.update_action(2)
    elif moving_rigth or moving_left:
      player.update_action(1)
    else:
      player.update_action(0)
    player.move(moving_left, moving_rigth)

  for event in pygame.event.get():
    if event.type == QUIT:
        run = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        moving_left = True
      if event.key == pygame.K_d:
        moving_rigth = True
      if event.key == pygame.K_SPACE:
        shoot = True
      if event.key == pygame.K_w and player.alive:
        player.jump = True
      if event.key == pygame.K_ESCAPE:
        run = False

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
        moving_left = False
      if event.key == pygame.K_d:
        moving_rigth = False
      if event.key == pygame.K_SPACE:
        shoot = False


  
  pygame.display.update()

pygame.quit()