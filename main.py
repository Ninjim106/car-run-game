import pygame
import math
import random

# Inicialização
pygame.init()

LARGURA = 900
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Corrida de Rua 2D")

relogio = pygame.time.Clock()

# Cores
PRETO = (20, 20, 20)
CINZA = (70, 70, 70)
CINZA_CLARO = (110, 110, 110)
BRANCO = (255, 255, 255)
VERDE = (40, 150, 60)
VERMELHO = (220, 40, 40)
AZUL = (40, 80, 220)
AMARELO = (255, 220, 40)

# Fonte
fonte = pygame.font.SysFont("Arial", 28)
fonte_grande = pygame.font.SysFont("Arial", 50)


# =========================
# CARRO DO JOGADOR
# =========================

class Carro:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.largura = 40
        self.altura = 70
        self.velocidade = 5
        self.cor = cor

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidade

        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidade

        if teclas[pygame.K_UP]:
            self.y -= self.velocidade

        if teclas[pygame.K_DOWN]:
            self.y += self.velocidade

        # Não deixar sair da tela
        self.x = max(0, min(LARGURA - self.largura, self.x))
        self.y = max(0, min(ALTURA - self.altura, self.y))

    def desenhar(self):
        pygame.draw.rect(
            tela,
            self.cor,
            (self.x, self.y, self.largura, self.altura)
        )

        # Vidro
        pygame.draw.rect(
            tela,
            (120, 200, 255),
            (self.x + 7, self.y + 10, 26, 18)
        )

        # Rodas
        pygame.draw.rect(
            tela,
            PRETO,
            (self.x - 5, self.y + 10, 7, 18)
        )

        pygame.draw.rect(
            tela,
            PRETO,
            (self.x + self.largura - 2, self.y + 10, 7, 18)
        )

        pygame.draw.rect(
            tela,
            PRETO,
            (self.x - 5, self.y + 45, 7, 18)
        )

        pygame.draw.rect(
            tela,
            PRETO,
            (self.x + self.largura - 2, self.y + 45, 7, 18)
        )

    def retangulo(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )


# =========================
# CARRO DA POLÍCIA
# =========================

class Policia:
    def __init__(self):
        self.x = random.randint(100, 700)
        self.y = -100
        self.largura = 45
        self.altura = 75
        self.velocidade = 2.2
        self.ativa = False

    def perseguir(self, jogador):

        if not self.ativa:
            return

        # Calcula a direção até o jogador
        dx = jogador.x - self.x
        dy = jogador.y - self.y

        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if distancia > 0:
            dx /= distancia
            dy /= distancia

        self.x += dx * self.velocidade
        self.y += dy * self.velocidade

    def desenhar(self):

        if not self.ativa:
            return

        # Corpo
        pygame.draw.rect(
            tela,
            AZUL,
            (self.x, self.y, self.largura, self.altura)
        )

        # Parte branca
        pygame.draw.rect(
            tela,
            BRANCO,
            (self.x + 5, self.y + 25, 35, 20)
        )

        # Sirene
        pygame.draw.rect(
            tela,
            VERMELHO,
            (self.x + 7, self.y + 5, 13, 8)
        )

        pygame.draw.rect(
            tela,
            AZUL,
            (self.x + 25, self.y + 5, 13, 8)
        )

    def retangulo(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )


# =========================
# FUNÇÃO PARA DESENHAR A PISTA
# =========================

def desenhar_pista():

    # Grama
    tela.fill(VERDE)

    # Estrada
    pygame.draw.rect(
        tela,
        CINZA,
        (150, 0, 600, ALTURA)
    )

    # Bordas
    pygame.draw.rect(
        tela,
        BRANCO,
        (150, 0, 8, ALTURA)
    )

    pygame.draw.rect(
        tela,
        BRANCO,
        (742, 0, 8, ALTURA)
    )

    # Faixas da estrada
    for y in range(0, ALTURA, 80):
        pygame.draw.rect(
            tela,
            BRANCO,
            (445, y, 10, 45)
        )


# =========================
# LINHA DE CHEGADA
# =========================

def desenhar_chegada():

    y = 100

    tamanho = 30

    for x in range(150, 750, tamanho):

        if (x // tamanho) % 2 == 0:
            cor = BRANCO
        else:
            cor = PRETO

        pygame.draw.rect(
            tela,
            cor,
            (x, y, tamanho, tamanho)
        )


# =========================
# JOGO
# =========================

jogador = Carro(430, 500, VERMELHO)
policia = Policia()

corrida_terminou = False
policia_ativa = False
game_over = False

tempo_inicio = pygame.time.get_ticks()

rodando = True

while rodando:

    relogio.tick(60)

    # Eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        # Reiniciar
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_r:

                jogador = Carro(430, 500, VERMELHO)
                policia = Policia()

                corrida_terminou = False
                policia_ativa = False
                game_over = False

                tempo_inicio = pygame.time.get_ticks()

    teclas = pygame.key.get_pressed()

    # =========================
    # MOVIMENTO DO JOGADOR
    # =========================

    if not game_over:

        jogador.mover(teclas)

    # =========================
    # VERIFICA A CHEGADA
    # =========================

    linha_chegada = pygame.Rect(
        150,
        100,
        600,
        30
    )

    if jogador.retangulo().colliderect(linha_chegada):

        if not corrida_terminou:

            corrida_terminou = True
            policia_ativa = True
            policia.ativa = True

    # =========================
    # POLÍCIA PERSEGUE
    # =========================

    if policia_ativa and not game_over:

        policia.perseguir(jogador)

    # =========================
    # COLISÃO
    # =========================

    if policia.ativa:

        if jogador.retangulo().colliderect(
            policia.retangulo()
        ):

            game_over = True

    # =========================
    # DESENHAR
    # =========================

    desenhar_pista()

    desenhar_chegada()

    jogador.desenhar()

    policia.desenhar()

    # =========================
    # TEMPO
    # =========================

    if not corrida_terminou:

        tempo = (
            pygame.time.get_ticks() - tempo_inicio
        ) / 1000

        texto_tempo = fonte.render(
            f"Tempo: {tempo:.1f}s",
            True,
            BRANCO
        )

        tela.blit(
            texto_tempo,
            (20, 20)
        )

    else:

        texto_police = fonte.render(
            "🚨 A POLÍCIA ESTÁ TE PERSEGUINDO!",
            True,
            VERMELHO
        )

        tela.blit(
            texto_police,
            (210, 20)
        )

    # =========================
    # GAME OVER
    # =========================

    if game_over:

        texto = fonte_grande.render(
            "VOCÊ FOI ALCANÇADO!",
            True,
            VERMELHO
        )

        tela.blit(
            texto,
            (230, 250)
        )

        reiniciar = fonte.render(
            "Pressione R para reiniciar",
            True,
            BRANCO
        )

        tela.blit(
            reiniciar,
            (300, 320)
        )

    pygame.display.update()


pygame.quit()
