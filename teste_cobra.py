import pygame, cores, sys
from random import randint
from pygame.locals import *

def main():

    pygame.init()

    fonte = pygame.font.SysFont('gabriola', 40, False, False)

    largura = 640
    altura = 480

    h_rect = 50
    w_rect = 50

    x = largura/2 - w_rect/2
    y = altura/2 - h_rect/2

    x_azul = randint(0, largura - w_rect)
    y_azul = randint(0, altura - h_rect)

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Teste')

    pontos = 0

    clock = pygame.time.Clock()

    while True:
        clock.tick(100)
        tela.fill((0, 0, 0))
        mensagem = f'Pontos: {pontos}'
        texto_formatado = fonte.render(mensagem, True, cores.branco)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if pygame.key.get_pressed()[K_w]:
                y -= 10
            if pygame.key.get_pressed()[K_a]:
                x -= 10
            if pygame.key.get_pressed()[K_s]:
                y += 10
            if pygame.key.get_pressed()[K_d]:
                x += 10
            
            if x > largura:
                x = 0 
            if x < 0:
                x = largura

            if y > altura:
                y = 0 
            if y < 0:
                y = altura

        ret_vermelho = pygame.draw.rect(tela, cores.vermelho, (x, y, w_rect, h_rect))
        ret_azul = pygame.draw.rect(tela, cores.azul, (x_azul, y_azul, w_rect, h_rect))

        if ret_vermelho.colliderect(ret_azul):
            x_azul = randint(0, largura - w_rect)
            y_azul = randint(0, altura - h_rect)
            pontos += 1

        tela.blit(texto_formatado, (10, 10))

        pygame.display.update()  

if __name__ == '__main__':
    main()
