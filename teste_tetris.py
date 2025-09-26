import pygame, cores, sys

def main():

    pygame.init()

    tela = pygame.display.set_mode((300, 600))
    pygame.display.set_caption("Python Tritris")
    tela.fill(cores.preto)

    num_linhas = 20

    for i in range(0, num_linhas):
        for j in range(0, num_linhas):
             pygame.draw.rect(tela, cores.azul_petroleo, (30 * i,  30 * j, 30, 30), 1)

    clock = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit
                sys.exit()

        pygame.display.update()
        clock.tick(60)
main()
                