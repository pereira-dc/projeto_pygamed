import pygame, cores, sys, random 
from pygame.locals import *

def main():
    pygame.init()
    
    largura, altura = 1000, 600  
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Cobrathon')
    clock = pygame.time.Clock()
    som_colisao = pygame.mixer.Sound('smw_fireball.wav')
    tam_quadrado = 20

    def gerar_comida():
        comida_x = round(random.randrange(0, largura - tam_quadrado) / tam_quadrado) * tam_quadrado
        comida_y = round(random.randrange(0, altura - tam_quadrado) / tam_quadrado) * tam_quadrado
        return comida_x, comida_y

    def draw_comida(tam, comida_x, comida_y):
        pygame.draw.rect(tela, cores.vermelho, [comida_x, comida_y, tam, tam])

    def draw_cobra(tam, pixels):
        for pixel in pixels:
            pygame.draw.rect(tela, cores.verde, [pixel[0], pixel[1], tam, tam])

    def draw_pontos(pontos):
        fonte = pygame.font.SysFont('Gabriola', 40, bold=False, italic=True)
        texto = fonte.render(f'Pontos: {pontos}', True, cores.branco)
        tela.blit(texto, (10, 10))

    def select_dir(key, dir_xc, dir_yc, next_dir_x, next_dir_y):
        if (key == pygame.K_DOWN or key == pygame.K_s) and dir_yc != -1:
            return 0, 1
        elif (key == pygame.K_UP or key == pygame.K_w) and dir_yc != 1:
            return 0, -1
        elif (key == pygame.K_RIGHT or key == pygame.K_d) and dir_xc != -1:
            return 1, 0
        elif (key == pygame.K_LEFT or key == pygame.K_a) and dir_xc != 1:
            return -1, 0
        return dir_xc, dir_yc

    def rodar_jogo():
        x_cobra = int(largura / 2)
        y_cobra = int(altura / 2)
        dir_xc, dir_yc = 0, 0
        next_dir_x, next_dir_y = dir_xc, dir_yc

        tam_cobra = 1
        pixels = []
        comida_x, comida_y = gerar_comida()

        velocidade = 4   # pixels por frame → controla suavidade
        clock_tick = 60  # FPS fixo

        while True:
            tela.fill(cores.preto)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    next_dir_x, next_dir_y = select_dir(event.key, dir_xc, dir_yc, next_dir_x, next_dir_y)

            # só troca a direção quando estiver alinhado na grade
            if x_cobra % tam_quadrado == 0 and y_cobra % tam_quadrado == 0:
                dir_xc, dir_yc = next_dir_x, next_dir_y

            # movimento suave (pixel a pixel)
            x_cobra += dir_xc * velocidade
            y_cobra += dir_yc * velocidade

            # colisão com borda
            if x_cobra > largura - tam_quadrado or x_cobra < 0 or y_cobra > altura - tam_quadrado or y_cobra < 0:
                pygame.quit()
                sys.exit()

            # atualiza corpo
            pixels.append([x_cobra, y_cobra])
            if len(pixels) > tam_cobra:
                del pixels[0]

            # colisão consigo mesmo
            for pixel in pixels[:-1]:
                if pixel == [x_cobra, y_cobra]:
                    pygame.quit()
                    sys.exit()

            # desenha
            comida_rect = pygame.Rect(comida_x, comida_y, tam_quadrado, tam_quadrado)
            draw_comida(tam_quadrado, comida_x, comida_y)

            cobra_rect = pygame.Rect(x_cobra, y_cobra, tam_quadrado, tam_quadrado)
            draw_cobra(tam_quadrado, pixels)

            draw_pontos(tam_cobra - 1)
            pygame.display.update()

            # colisão com comida
            if cobra_rect.colliderect(comida_rect):
                tam_cobra += 1
                comida_x, comida_y = gerar_comida()
                som_colisao.play()
                if velocidade < tam_quadrado:  # limite para não pular blocos
                    velocidade += 1

            clock.tick(clock_tick)


    rodar_jogo()

if __name__ == '__main__':
    main()
