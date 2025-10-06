import pygame, sys, random, cores
from pygame.locals import *

largura, altura = 1000, 600
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

    pisca = 500
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
                elif event.key == K_ESCAPE:
                    som_inicial.stop()
                    pygame.quit()
                    sys.exit()

        tempo = pygame.time.get_ticks()
        if (tempo % (pisca * 2)) < pisca:
            tela.blit(texto_titulo, ret_titulo)

        pygame.display.update()

def gerar_comida(pixels, pixels_npc):
    while True:
        comida_x = random.randrange(0, largura - tam_quadrado, tam_quadrado)
        comida_y = random.randrange(0, altura - tam_quadrado, tam_quadrado)
        if [comida_x, comida_y] not in pixels and [comida_x, comida_y] not in pixels_npc:
            return comida_x, comida_y

def draw_comida(tela, comida_x, comida_y):
    pygame.draw.rect(tela, cores.vermelho, (comida_x, comida_y, tam_quadrado, tam_quadrado))

def draw_cobra(tela, pixels, cor):
    for pixel in pixels:
        pygame.draw.rect(tela, cor, (pixel[0], pixel[1], tam_quadrado, tam_quadrado))

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

def select_dir_npc(dirnpc_x, dirnpc_y, velocidade):
    direcoes = [(velocidade, 0), (-velocidade, 0), (0, velocidade), (0, -velocidade)]
    direcoes_validas = [d for d in direcoes if d != (-dirnpc_x, -dirnpc_y)]
    return random.choice(direcoes_validas)

def reiniciar_jogo():
    x_cobra = largura // 2
    y_cobra = altura // 2
    dir_x, dir_y = tam_quadrado, 0
    comprimento = 5
    pixels = [[x_cobra - i * tam_quadrado, y_cobra] for i in range(comprimento)]

    comida_x, comida_y = gerar_comida(pixels, [])

    x_cobranpc = random.randrange(0, largura - tam_quadrado, tam_quadrado)
    y_cobranpc = random.randrange(0, altura - tam_quadrado, tam_quadrado)
    while [x_cobranpc, y_cobranpc] == [x_cobra, y_cobra] or [x_cobranpc, y_cobranpc] == [comida_x, comida_y]:
        x_cobranpc = random.randrange(0, largura - tam_quadrado, tam_quadrado)
        y_cobranpc = random.randrange(0, altura - tam_quadrado, tam_quadrado)
    dirnpc_x, dirnpc_y = tam_quadrado, 0
    comprimento_npc = 5
    pixels_npc = [[x_cobranpc - i * tam_quadrado, y_cobranpc] for i in range(comprimento_npc)]

    pontos = 0
    npc_ativa = False

    return (x_cobra, y_cobra, dir_x, dir_y, pixels, comprimento,
            x_cobranpc, y_cobranpc, dirnpc_x, dirnpc_y, pixels_npc,
            comprimento_npc, comida_x, comida_y, pontos, npc_ativa)

def rodar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Cobrathon')
    clock = pygame.time.Clock()
    #som_colisao = pygame.mixer.Sound('smw_yoshi_swallow.wav')
    fps = 20

    (x_cobra, y_cobra, dir_x, dir_y, pixels, comprimento,
     x_cobranpc, y_cobranpc, dirnpc_x, dirnpc_y, pixels_npc,
     comprimento_npc, comida_x, comida_y, pontos, npc_ativa) = reiniciar_jogo()

    morreu = False
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
                    (x_cobra, y_cobra, dir_x, dir_y, pixels, comprimento,
                     x_cobranpc, y_cobranpc, dirnpc_x, dirnpc_y, pixels_npc,
                     comprimento_npc, comida_x, comida_y, pontos, npc_ativa) = reiniciar_jogo()
                    morreu = False
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    dir_x, dir_y = select_dir(event.key, dir_x, dir_y, tam_quadrado)

        if not morreu:
            # Mover a cobra do jogador
            x_cobra += dir_x
            y_cobra += dir_y
            x_cobra %= largura
            y_cobra %= altura
            pixels.append([x_cobra, y_cobra])
            if len(pixels) > comprimento:
                del pixels[0]

            # Verificar colisão da cobra do jogador com ela mesma
            if [x_cobra, y_cobra] in pixels[:-1]:
                morreu = True

            if pontos >= 2:
                npc_ativa = True

            if npc_ativa:
                # Verificar colisões antes de mover a NPC
                for p in pixels_npc:
                    if [x_cobra, y_cobra] == p:
                        morreu = True
                        npc_ativa = False  # Desativa a NPC
                        break

                for p in pixels:
                    if [x_cobranpc, y_cobranpc] == p:
                        npc_ativa = False
                        break

                if [x_cobra, y_cobra] == [x_cobranpc, y_cobranpc]:
                    npc_ativa = False
                    morreu = True

                # Mover a NPC apenas se ela ainda estiver ativa
                if npc_ativa:
                    if random.randint(0, 10) == 0:
                        dirnpc_x, dirnpc_y = select_dir_npc(dirnpc_x, dirnpc_y, tam_quadrado)
                    x_cobranpc += dirnpc_x
                    y_cobranpc += dirnpc_y
                    x_cobranpc %= largura
                    y_cobranpc %= altura
                    pixels_npc.append([x_cobranpc, y_cobranpc])
                    if len(pixels_npc) > comprimento_npc:
                        del pixels_npc[0]

                    # Verificar colisão da NPC com ela mesma
                    if [x_cobranpc, y_cobranpc] in pixels_npc[:-1]:
                        npc_ativa = False

            # Verificar colisão com comida
            cobra_rect = pygame.Rect(x_cobra, y_cobra, tam_quadrado, tam_quadrado)
            comida_rect = pygame.Rect(comida_x, comida_y, tam_quadrado, tam_quadrado)
            if cobra_rect.colliderect(comida_rect):
                comida_x, comida_y = gerar_comida(pixels, pixels_npc)
                comprimento += 1
                pontos += 1
                #som_colisao.play()
                if fps < 50:
                    fps += 1

            if npc_ativa:
                cobranpc_rect = pygame.Rect(x_cobranpc, y_cobranpc, tam_quadrado, tam_quadrado)
                if cobranpc_rect.colliderect(comida_rect):
                    comida_x, comida_y = gerar_comida(pixels, pixels_npc)
                    comprimento_npc += 1

            draw_comida(tela, comida_x, comida_y)
            draw_cobra(tela, pixels, cores.verde)
            if npc_ativa:
                draw_cobra(tela, pixels_npc, cores.azul_petroleo)
            draw_pontos(tela, pontos)

        else:
            tela.fill(cores.preto)
            fonte_txt = pygame.font.SysFont('Arial', 28, True, True)
            fonte_msg = pygame.font.SysFont('Arial', 16, True, True)
            texto = f"Game Over! Você fez {pontos} ponto(s)"
            txt_formatado = fonte_txt.render(texto, True, cores.branco)
            ret_txt = txt_formatado.get_rect(center=(largura//2, altura//2 - 50))
            msg = "Pressione R para reiniciar ou ESC para sair"
            msg_formatado = fonte_msg.render(msg, True, cores.branco)
            ret_msg = msg_formatado.get_rect(center=(largura//2, altura//2 + 50))

            tempo = pygame.time.get_ticks()
            pisca = 500
            if (tempo % (pisca * 2)) < pisca:
                tela.blit(msg_formatado, ret_msg)

            tela.blit(txt_formatado, ret_txt)

        pygame.display.update()

if __name__ == "__main__":
    rodar_jogo()