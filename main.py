import pygame
from pygame.locals import *
from sys import exit

SCREEN_WIDTH = 800
SCREEN_HEIGTH = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption('PicaPau do Iguacu')

clock = pygame.time.Clock()
FPS = 60


moving_left = False
moving_rigth = False

BG = (144, 201, 120)


def draw_bg():
  screen.fill(BG)


class Character(pygame.sprite.Sprite):
  def __init__(self, char_type, x, y, scale, speed):
    pygame.sprite.Sprite.__init__(self)
    self.speed = speed
    self.direction = 1
    self.flip = False
    img = pygame.image.load(f'images/{char_type}/idle/0.png')
    self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height()* scale)))
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)

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

    self.rect.x += dx
    self.rect.y += dy

  
  def draw(self):
    screen.blit(pygame.transform.flip(self.image ,self.flip, False), self.rect)

player = Character('wood' ,200, 200, 0.4, 5)
enemy = Character('guarda3' ,400, 200, 0.1, 5)


run = True
while run:

  clock.tick(FPS)
  
  draw_bg()

  player.draw()
  enemy.draw()
  player.move(moving_left, moving_rigth)

  for event in pygame.event.get():
    if event.type == QUIT:
        run = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        moving_left = True
      if event.key == pygame.K_d:
        moving_rigth = True
      if event.key == pygame.K_ESCAPE:
        run = False

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
        moving_left = False
      if event.key == pygame.K_d:
        moving_rigth = False


  
  pygame.display.update()

pygame.quit()