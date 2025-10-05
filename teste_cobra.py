import pygame, sys, random, cores
from pygame.locals import *

largura, altura = 1000, 600
tam_quadrado = 20

def tela_inicio(tela):
    tela.fill(cores.preto)
    fonte_titulo = pygame.font.SysFont('Arial', 60, True, True)
    fonte_instrucao = pygame.font.SysFont('Arial', 28, True, True)

    texto_titulo = fonte_titulo.render("Cobrathon", True, cores.verde)
    texto_instrucao = fonte_instrucao.render("Pressione ENTER para começars ou ESC para sair", True, cores.branco)

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
                if event.key == K_RETURN:  # Enter para iniciar
                    som_inicial.stop()
                    esperando = False
    
        tempo = pygame.time.get_ticks()
        if (tempo % (pisca * 2)) < pisca: # tempo % 1000 < pisca(500): Retorna a mensagem, caso contrário, some.
            tela.blit(texto_titulo, ret_titulo) # Desenha a mensagem na tela
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
    lista_cobra = []
    comida_x, comida_y = gerar_comida()
    pontos = 0
    return x_cobra, y_cobra, dir_x, dir_y, pixels, comprimento, lista_cobra, comida_x, comida_y, pontos

def rodar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Cobrathon')
    clock = pygame.time.Clock()
    som_colisao = pygame.mixer.Sound('smw_yoshi_swallow.wav')
    fps = 20
    x_cobra, y_cobra, dir_x, dir_y, pixels, comprimento, lista_cobra, comida_x, comida_y, pontos = reiniciar_jogo()
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
                    x_cobra, y_cobra, dir_x, dir_y, pixels, comprimento,lista_cobra, comida_x, comida_y, pontos = reiniciar_jogo()
                    morreu = False
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    dir_x, dir_y = select_dir(event.key, dir_x, dir_y, tam_quadrado)


        if not morreu:
            x_cobra += dir_x
            y_cobra += dir_y

            #Teletransporte da Cobra
            if x_cobra >= largura:
                x_cobra = 0
            if x_cobra < 0:
                x_cobra = largura - tam_quadrado
            if y_cobra < 0:
                y_cobra = altura - tam_quadrado
            if y_cobra >= altura:
                y_cobra = 0

            pixels.append([x_cobra, y_cobra])
            if len(pixels) > comprimento:
                del pixels[0]

            if [x_cobra, y_cobra] in pixels[:-1]:
                morreu = True

            draw_comida(tela, comida_x, comida_y)
            draw_cobra(tela, pixels)
            draw_pontos(tela, pontos)

            cobra_rect = pygame.Rect(x_cobra, y_cobra, tam_quadrado, tam_quadrado)
            comida_rect = pygame.Rect(comida_x, comida_y, tam_quadrado, tam_quadrado)
            if cobra_rect.colliderect(comida_rect):
                comida_x, comida_y = gerar_comida()
                comprimento += 1
                pontos += 1
                som_colisao.play()

                if fps < 50:
                    fps += 1

        else:
            tela.fill(cores.preto)
            fonte_txt = pygame.font.SysFont('Arial', 28, True, True)
            fonte_msg = pygame.font.SysFont('Arial', 16, True, True)
            texto = f"Game Over! Você fez {pontos} ponto(s)"
            txt_formatado = fonte_txt.render(texto, True, (cores.branco))
            ret_txt = txt_formatado.get_rect(center=(largura//2, altura//2 - 50))
            msg = "Pressione R para reiniciar ou ESC para sair"
            msg_formatado = fonte_msg.render(msg, True, (cores.branco))
            ret_msg = msg_formatado.get_rect(center=(largura//2, altura//2 + 50))

            tempo = pygame.time.get_ticks() #retorna o tempo em milissegundos desde a inicialização do jogo
            pisca = 500 # intervalo de tempo em 500 milissegundos
            if (tempo % (pisca * 2)) < pisca: # tempo % 1000 < pisca(500): Retorna a mensagem, caso contrário, some.
                tela.blit(msg_formatado, ret_msg) # Desenha a mensagem na tela
            morreu = True
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        x_cobra, y_cobra, dir_x, dir_y, pixels, comprimento,lista_cobra, comida_x, comida_y, pontos = reiniciar_jogo()
                        morreu = False

            ret_txt.center = largura//2, altura//2
            tela.blit(txt_formatado, ret_txt)
        
        if len(lista_cobra) > comprimento:
            del lista_cobra[0]
        
        pygame.display.update()

if __name__ == "__main__":
    rodar_jogo()
