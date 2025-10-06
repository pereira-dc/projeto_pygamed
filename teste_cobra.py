import pygame, sys, random, cores
from pygame.locals import *

largura, altura = 800, 600
tam_quadrado = 20

def tela_inicio(tela):
    tela.fill(cores.preto)
    fonte_titulo = pygame.font.SysFont('Arial', 60, True, True)
    fonte_instrucao = pygame.font.SysFont('Arial', 28, True, True)

    texto_titulo = fonte_titulo.render("Cobrathon", True, cores.verde)
    texto_instrucao = fonte_instrucao.render("Pressione ENTER para começar ou ESC para sair", True, cores.branco)

    ret_titulo = texto_titulo.get_rect(center=(largura//2, altura//2 - 50))
    ret_instrucao = texto_instrucao.get_rect(center=(largura//2, altura//2 + 50))

    tela.blit(texto_titulo, ret_titulo)
    tela.blit(texto_instrucao, ret_instrucao)
    som_inicial = pygame.mixer.Sound('echoesofeternitymix.ogg')
    som_inicial.play(-1)

    esperando = True
    while esperando:
        tela.fill(cores.preto)
        tela.blit(texto_instrucao, ret_instrucao)

        for event in pygame.event.get():
            if event.type == QUIT:
                som_inicial.stop()
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    som_inicial.stop()
                    esperando = False
    
        piscar_texto(tela, texto_titulo, ret_titulo, 500)
        pygame.display.update()

def gerar_comida():
    comida_x = random.randrange(0, largura - tam_quadrado, tam_quadrado)
    comida_y = random.randrange(0, altura - tam_quadrado, tam_quadrado)
    return comida_x, comida_y

def draw_comida(tela, comida_x, comida_y): 
    pygame.draw.rect(tela, cores.vermelho, (comida_x, comida_y, tam_quadrado, tam_quadrado))

def draw_cobra(tela, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, cores.verde, (pixel[0], pixel[1], tam_quadrado, tam_quadrado))

def draw_npc(tela, pixels_npc):
    for pixel in pixels_npc:
        pygame.draw.rect(tela, cores.azul, (pixel[0], pixel[1], tam_quadrado, tam_quadrado))

def draw_pontos(tela, pontos):
    fonte = pygame.font.SysFont('Courier New', 40, bold=False, italic=True)
    texto = fonte.render(f'Pontos: {pontos}', True, cores.preto)
    tela.blit(texto, (10, 10))

def draw_recorde(tela, recorde):
    fonte = pygame.font.SysFont('Courier New', 40, bold=False, italic=True)
    texto = fonte.render(f'Recorde: {recorde}', True, cores.preto)
    tela.blit(texto, (10, 60))

def piscar_texto(tela, texto_renderizado, retangulo_texto, velocidade_pisca):
    tempo = pygame.time.get_ticks()
    if (tempo % (velocidade_pisca * 2)) < velocidade_pisca:
        tela.blit(texto_renderizado, retangulo_texto)

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

def spawn_npc():
    x_npc = random.randrange(0, largura - tam_quadrado, tam_quadrado)
    y_npc = random.randrange(0, altura - tam_quadrado, tam_quadrado)
    direcoes = [(tam_quadrado, 0), (-tam_quadrado, 0), (0, tam_quadrado), (0, -tam_quadrado)]
    dir_x_npc, dir_y_npc = random.choice(direcoes)
    pixels_npc = []
    tam_npc = 7
    return x_npc, y_npc, dir_x_npc, dir_y_npc, pixels_npc, tam_npc, True

def reiniciar_jogo():
    x_cobra = largura // 2
    y_cobra = altura // 2
    dir_x, dir_y = tam_quadrado, 0
    pixels = []
    tam = 5
    comida_x, comida_y = gerar_comida()
    pontos = 0
    npc_ativo = False
    x_npc = y_npc = dir_x_npc = dir_y_npc = None
    pixels_npc = []
    tam_npc = 0
    ultimo_spawn_pontos = 0
    fps = 15
    return x_cobra, y_cobra, dir_x, dir_y, pixels, tam, comida_x, comida_y, pontos, x_npc, y_npc, dir_x_npc, dir_y_npc, pixels_npc, tam_npc, npc_ativo, ultimo_spawn_pontos, fps

def rodar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Cobrathon')
    clock = pygame.time.Clock()
    som_colisao = pygame.mixer.Sound('smw_yoshi_swallow.wav')
    x_cobra, y_cobra, dir_x, dir_y, pixels, tam, comida_x, comida_y, pontos, x_npc, y_npc, dir_x_npc, dir_y_npc, pixels_npc, tam_npc, npc_ativo, ultimo_spawn_pontos, fps = reiniciar_jogo()
    morreu = False
    recorde = 0

    tela_inicio(tela)

    while True:
        clock.tick(fps)
        tela.fill(cores.branco)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if morreu and event.key == K_r:
                    x_cobra, y_cobra, dir_x, dir_y, pixels, tam, comida_x, comida_y, pontos, x_npc, y_npc, dir_x_npc, dir_y_npc, pixels_npc, tam_npc, npc_ativo, ultimo_spawn_pontos, fps = reiniciar_jogo()
                    morreu = False
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    dir_x, dir_y = select_dir(event.key, dir_x, dir_y, tam_quadrado)

        if not morreu:
            if pontos >= 5 and pontos > ultimo_spawn_pontos and pontos % 5 == 0 and not npc_ativo:
                x_npc, y_npc, dir_x_npc, dir_y_npc, pixels_npc, tam_npc, npc_ativo = spawn_npc()
                ultimo_spawn_pontos = pontos 

            x_cobra += dir_x
            y_cobra += dir_y

            if x_cobra >= largura: x_cobra = 0
            if x_cobra < 0: x_cobra = largura - tam_quadrado
            if y_cobra < 0: y_cobra = altura - tam_quadrado
            if y_cobra >= altura: y_cobra = 0

            pixels.append([x_cobra, y_cobra])
            if len(pixels) > tam:
                del pixels[0]

            if [x_cobra, y_cobra] in pixels[:-1]:
                morreu = True

            if npc_ativo and [x_cobra, y_cobra] in pixels_npc:
                morreu = True

            if npc_ativo:
                if random.random() < 0.1:
                    direcoes = [(tam_quadrado, 0), (-tam_quadrado, 0), (0, tam_quadrado), (0, -tam_quadrado)]
                    possiveis_dirs = [d for d in direcoes if d != (-dir_x_npc, -dir_y_npc)]
                    dir_x_npc, dir_y_npc = random.choice(possiveis_dirs)

                x_npc += dir_x_npc
                y_npc += dir_y_npc

                if x_npc >= largura: x_npc = 0
                if x_npc < 0: x_npc = largura - tam_quadrado
                if y_npc < 0: y_npc = altura - tam_quadrado
                if y_npc >= altura: y_npc = 0

                pixels_npc.append([x_npc, y_npc])
                if len(pixels_npc) > tam_npc:
                    del pixels_npc[0]

                if [x_npc, y_npc] in pixels_npc[:-1]:
                    npc_ativo = False

                if [x_npc, y_npc] in pixels:
                    npc_ativo = False

                npc_rect = pygame.Rect(x_npc, y_npc, tam_quadrado, tam_quadrado)
                comida_rect_npc = pygame.Rect(comida_x, comida_y, tam_quadrado, tam_quadrado)
                if npc_rect.colliderect(comida_rect_npc):
                    comida_x, comida_y = gerar_comida()
                    tam_npc += 1
                    som_colisao.play()

            draw_comida(tela, comida_x, comida_y)
            draw_cobra(tela, pixels)
            if npc_ativo:
                draw_npc(tela, pixels_npc)
            draw_pontos(tela, pontos)
            draw_recorde(tela, recorde)

            cobra_rect = pygame.Rect(x_cobra, y_cobra, tam_quadrado, tam_quadrado)
            comida_rect = pygame.Rect(comida_x, comida_y, tam_quadrado, tam_quadrado)
            if cobra_rect.colliderect(comida_rect):
                comida_x, comida_y = gerar_comida()
                tam += 1
                pontos += 1
                som_colisao.play()

                if fps < 50:
                    fps += 1

                if pontos > recorde:
                    recorde = pontos


        else:
            tela.fill(cores.preto)
            fonte_txt = pygame.font.SysFont('Arial', 28, True, True)
            fonte_msg = pygame.font.SysFont('Arial', 16, True, True)
            texto = f"Game Over! Você fez {pontos} ponto(s)"
            txt_formatado = fonte_txt.render(texto, True, (cores.branco))
            ret_txt = txt_formatado.get_rect(center=(largura//2, altura//2 - 50))
            msg = "Pressione R para reiniciar ou ESC para sair"
            msg_formatada = fonte_msg.render(msg, True, (cores.branco))
            ret_msg = msg_formatada.get_rect(center=(largura//2, altura//2 + 50))

            piscar_texto(tela, msg_formatada, ret_msg, 500)

            ret_txt.center = largura//2, altura//2
            tela.blit(txt_formatado, ret_txt)
        
        pygame.display.update()

if __name__ == "__main__":
    rodar_jogo()
