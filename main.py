import pygame
from pygame.locals import *
from sys import exit

SCREEN_WIDTH = 800
SCREEN_HEIGTH = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption('PicaPau do Iguacu')

class Wood(pygame.sprite.Sprite):
  def __init__(self, x, y, escala):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('images/wood/wood.png')
    self.imagem = pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height()* escala)))
    self.rect = self.imagem.get_rect()
    self.rect.center = (x, y)


player = Wood(200, 200, 0.3)


run = True
while run:

  screen.blit(player.imagem, player.rect)

  for event in pygame.event.get():
    if event.type == QUIT:
        run = False
  
  pygame.display.update()

pygame.quit()