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


class Wood(pygame.sprite.Sprite):
  def __init__(self, x, y, scale, speed):
    pygame.sprite.Sprite.__init__(self)
    self.speed = speed
    img = pygame.image.load('images/wood/wood.png')
    self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height()* scale)))
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)

  def move(self, moving_left, moving_rigth):
    dx = 0
    dy = 0

    if moving_left:
      dx = -self.speed
    if moving_rigth:
      dx = self.speed

    self.rect.x += dx
    self.rect.y += dy

  
  def draw(self):
    screen.blit(self.image, self.rect)

player = Wood(200, 200, 0.3, 5)


run = True
while run:

  clock.tick(FPS)
  
  draw_bg()

  player.draw()
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