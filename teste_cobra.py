import pygame, cores, sys
from pygame.locals import *

def main():

    pygame.init()

    largura = 640
    altura = 480

    l1_rect = 40
    l2_rect = 50


    x = largura/2 - l1_rect/2
    y = altura/2 - l2_rect/2

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Teste')

    clock = pygame.time.Clock()

    while True:
        clock.tick(100)
        tela.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if pygame.key.get_pressed()[K_w]:
                y -= 20
            if pygame.key.get_pressed()[K_a]:
                x -= 20
            if pygame.key.get_pressed()[K_s]:
                y += 20
            if pygame.key.get_pressed()[K_d]:
                x += 20
            
            if x > largura:
                x = 0 
            if x < 0:
                x = largura

            if y > altura:
                y = 0 
            if y < 0:
                y = altura

        pygame.draw.rect(tela, cores.vermelho, (x, y, l1_rect, l2_rect))
        pygame.draw.rect(tela, cores.azul, (200, 300, l1_rect, l2_rect))

        pygame.display.update()  

main()
