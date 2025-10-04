import pygame, sys, random, cores
from pygame.locals import *

# Configurações
largura, altura = 1000, 600
tam_quadrado = 20
fps = 30

def gerar_comida():
    comida_x = random.randrange(0, largura - tam_quadrado, tam_quadrado)
    comida_y = random.randrange(0, altura - tam_quadrado, tam_quadrado)
    return comida_x, comida_y

def draw_comida(tela, comida_x, comida_y):
    pygame.draw.rect(tela, cores.vermelho, (comida_x, comida_y, tam_quadrado, tam_quadrado))

def draw_cobra(tela, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, cores.verde, (pixel[0], pixel[1], tam_quadrado, tam_quadrado))

def draw_pontos(tela, pontos):
    fonte = pygame.font.SysFont('Courier New', 40, bold=False, italic=True)
    texto = fonte.render(f'Pontos: {pontos}', True, cores.preto)
    tela.blit(texto, (10, 10))

def select_dir(key, dir_x, dir_y, velocidade):
    if (key == K_DOWN or key == K_s) and dir_y != -velocidade:
        return 0, velocidade
    elif (key == K_UP or key == K_w) and dir_y != velocidade:
        return 0, -velocidade
    elif (key == K_RIGHT or key == K_d) and dir_x != -velocidade:
        return velocidade, 0
    elif (key == K_LEFT or key == K_a) and dir_x != velocidade:
        return -velocidade, 0
    return dir_x, dir_y

def reiniciar_jogo():
    x_cobra = largura // 2
    y_cobra = altura // 2
    dir_x, dir_y = tam_quadrado, 0
    pixels = []
    comprimento = 5
    comida_x, comida_y = gerar_comida()
    pontos = 0
    return x_cobra, y_cobra, dir_x, dir_y, pixels, comprimento, comida_x, comida_y, pontos

def rodar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Cobrathon')
    clock = pygame.time.Clock()
    som_colisao = pygame.mixer.Sound('smw_fireball.wav')

    x_cobra, y_cobra, dir_x, dir_y, pixels, comprimento, comida_x, comida_y, pontos = reiniciar_jogo()

    morreu = False

    while True:
        clock.tick(fps)
        tela.fill(cores.branco)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if morreu and event.key == K_r:
                    x_cobra, y_cobra, dir_x, dir_y, pixels, comprimento, comida_x, comida_y, pontos = reiniciar_jogo()
                    morreu = False
                else:
                    dir_x, dir_y = select_dir(event.key, dir_x, dir_y, tam_quadrado)

        if not morreu:
            # Movimento da cobra
            x_cobra += dir_x
            y_cobra += dir_y

            # Colisão com parede → Game Over
            if x_cobra < 0 or x_cobra >= largura or y_cobra < 0 or y_cobra >= altura:
                morreu = True

            # Atualiza corpo
            pixels.append([x_cobra, y_cobra])
            if len(pixels) > comprimento:
                del pixels[0]

            # Colisão consigo mesma
            if [x_cobra, y_cobra] in pixels[:-1]:
                morreu = True

            # Desenhos do jogo
            draw_comida(tela, comida_x, comida_y)
            draw_cobra(tela, pixels)
            draw_pontos(tela, pontos)

            # Colisão com comida
            cobra_rect = pygame.Rect(x_cobra, y_cobra, tam_quadrado, tam_quadrado)
            comida_rect = pygame.Rect(comida_x, comida_y, tam_quadrado, tam_quadrado)
            if cobra_rect.colliderect(comida_rect):
                comida_x, comida_y = gerar_comida()
                comprimento += 1
                pontos += 1
                som_colisao.play()

        else:
            # Tela de Game Over
            tela.fill(cores.preto)
            fonte = pygame.font.SysFont('Arial', 28, True, True)
            texto = fonte.render("Game Over! Pressione R para reiniciar", True, cores.branco)
            rect = texto.get_rect(center=(largura//2, altura//2))
            tela.blit(texto, rect)

            # Aguarda input para reiniciar
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        x_cobra, y_cobra, dir_x, dir_y, pixels, comprimento, comida_x, comida_y, pontos = reiniciar_jogo()
                        morreu = False

        pygame.display.update()

if __name__ == "__main__":
    rodar_jogo()
