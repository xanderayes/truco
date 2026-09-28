import random
import pygame

# Definindo a ordem base de força das cartas do Truco Paulista
ORDEM_BASE = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']

# Na manilha, a força do naipe define o desempate (Paus > Copas > Espadas > Ouros)
FORCA_NAIPES = {'Paus': 4, 'Copas': 3, 'Espadas': 2, 'Ouros': 1}

NAIPES = ['Ouros', 'Espadas', 'Copas', 'Paus']

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE_MESA = (34, 139, 34)
VERMELHO = (220, 20, 60)
AZUL = (30, 144, 255)
AMARELO = (255, 215, 0)
CINZA = (128, 128, 128)
MARROM = (139, 69, 19)

class Carta:
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    def __repr__(self):
        return f"{self.valor} de {self.naipe}"

class Baralho:
    def __init__(self):
        self.cartas = [Carta(v, n) for v in ORDEM_BASE for n in NAIPES]
        random.shuffle(self.cartas)

    def comprar(self, quantidade=3):
        mao = self.cartas[:quantidade]
        self.cartas = self.cartas[quantidade:]
        return mao

class CartaVisual:
    def __init__(self, carta, x, y, width=80, height=120):
        self.carta = carta
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False
        self.selected = False

    def draw(self, surface, face_up=True):
        # Sombra
        shadow_rect = pygame.Rect(self.x + 3, self.y + 3, self.width, self.height)
        pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=8)
        
        if face_up:
            # Fundo da carta
            color = BRANCO if not self.selected else AMARELO
            if self.hovered:
                color = (240, 240, 255)
            pygame.draw.rect(surface, color, self.rect, border_radius=8)
            pygame.draw.rect(surface, PRETO, self.rect, 2, border_radius=8)
            
            # Cor do naipe
            naipe_color = VERMELHO if self.carta.naipe in ['Copas', 'Ouros'] else PRETO
            
            # Desenha o valor
            font = pygame.font.Font(None, 36)
            valor_text = font.render(self.carta.valor, True, naipe_color)
            surface.blit(valor_text, (self.x + 8, self.y + 8))
            
            # Desenha o naipe geometricamente
            self.draw_naipe(surface, self.carta.naipe, naipe_color)
            
            # Valor invertido no canto inferior direito
            valor_text_rot = pygame.transform.rotate(valor_text, 180)
            surface.blit(valor_text_rot, (self.x + self.width - valor_text_rot.get_width() - 8,
                                         self.y + self.height - valor_text_rot.get_height() - 8))
        else:
            # Verso da carta
            pygame.draw.rect(surface, (50, 50, 150), self.rect, border_radius=8)
            pygame.draw.rect(surface, BRANCO, self.rect, 2, border_radius=8)
            # Padrão no verso
            for i in range(0, self.width, 10):
                pygame.draw.line(surface, (70, 70, 170), 
                                (self.x + i, self.y), 
                                (self.x + i, self.y + self.height), 1)

    def get_simbolo_naipe(self, naipe):
        simbolos = {
            'Ouros': '♦',
            'Espadas': '♠',
            'Copas': '♥',
            'Paus': '♣'
        }
        return simbolos.get(naipe, '?')
    
    def draw_naipe(self, surface, naipe, color):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        size = 20
        
        if naipe == 'Ouros':
            # Desenha losango (ouros)
            points = [
                (center_x, center_y - size),
                (center_x + size, center_y),
                (center_x, center_y + size),
                (center_x - size, center_y)
            ]
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, color, points, 2)
            
        elif naipe == 'Espadas':
            # Desenha espada
            # Ponta
            pygame.draw.polygon(surface, color, [
                (center_x, center_y - size),
                (center_x - size//2, center_y),
                (center_x + size//2, center_y)
            ])
            # Haste
            pygame.draw.line(surface, color, (center_x, center_y), (center_x, center_y + size), 3)
            # Base
            pygame.draw.line(surface, color, (center_x - size//2, center_y + size), 
                            (center_x + size//2, center_y + size), 3)
            pygame.draw.line(surface, color, (center_x, center_y + size), 
                            (center_x, center_y + size - 5), 3)
            
        elif naipe == 'Copas':
            # Desenha coração
            pygame.draw.circle(surface, color, (center_x - size//2, center_y - size//3), size//2)
            pygame.draw.circle(surface, color, (center_x + size//2, center_y - size//3), size//2)
            pygame.draw.polygon(surface, color, [
                (center_x - size, center_y - size//6),
                (center_x + size, center_y - size//6),
                (center_x, center_y + size)
            ])
            
        elif naipe == 'Paus':
            # Desenha trevo (paus)
            # Três círculos
            pygame.draw.circle(surface, color, (center_x, center_y - size//2), size//2)
            pygame.draw.circle(surface, color, (center_x - size//2, center_y + size//4), size//2)
            pygame.draw.circle(surface, color, (center_x + size//2, center_y + size//4), size//2)
            # Haste
            pygame.draw.line(surface, color, (center_x, center_y + size//4), 
                            (center_x, center_y + size), 3)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered

class JogoTrucoVisual:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)
        self.font_grande = pygame.font.Font(None, 48)
        
        # Estado do jogo
        self.placar_nos = 0
        self.placar_eles = 0
        self.estado = 'jogando'  # menu, jogando, fim_jogo
        
        # Estado da mão atual
        self.baralho = None
        self.vira = None
        self.manilha_valor = None
        self.maos = {}
        self.mesa = []
        self.vitorias_queda = {0: 0, 1: 0}
        self.rodada_atual = 1
        self.primeiro_a_jogar = 0
        self.jogador_atual = 0
        self.primeira_cangada = False
        self.vencedor_primeira = None
        
        # Estado do truco
        self.valor_rodada = 1  # 1, 3, 6, 9, 12
        self.quem_pediu_truco = None  # jogador que pediu truco
        self.esperando_resposta_truco = False  # se está esperando aceitar/fugir
        self.pode_pedir_truco = True  # se ainda pode pedir truco nesta queda
        
        # Cartas visuais
        self.cartas_visuais = []
        self.cartas_mesa = []
        
        # Mensagens
        self.mensagem = ""
        self.mensagem_timer = 0
        
        # Timer para bots
        self.bot_timer = 0
        
        # Botões de truco
        self.btn_pedir_truco = pygame.Rect(self.width - 200, self.height - 100, 180, 50)
        self.btn_aumentar_truco = pygame.Rect(self.width - 200, self.height - 160, 180, 50)
        self.btn_aceitar = pygame.Rect(self.width // 2 - 100, self.height // 2 + 50, 90, 50)
        self.btn_fugir = pygame.Rect(self.width // 2 + 10, self.height // 2 + 50, 90, 50)
        
        # Inicia nova mão
        self.nova_mao()

    def nova_mao(self):
        self.baralho = Baralho()
        self.vira, self.manilha_valor = self.obter_manilha_e_vira(self.baralho)
        self.maos = {i: self.baralho.comprar(3) for i in range(4)}
        self.mesa = []
        self.vitorias_queda = {0: 0, 1: 0}
        self.rodada_atual = 1
        self.primeiro_a_jogar = 0  # Jogador humano sempre começa
        self.jogador_atual = 0
        self.primeira_cangada = False
        self.vencedor_primeira = None
        self.cartas_mesa = []
        
        # Reseta estado do truco
        self.valor_rodada = 1
        self.quem_pediu_truco = None
        self.esperando_resposta_truco = False
        self.pode_pedir_truco = True
        
        # Cria cartas visuais para o jogador
        self.criar_cartas_jogador()
        
        self.mensagem = f"Nova mão! Vira: {self.vira}"
        self.mensagem_timer = 120

    def obter_manilha_e_vira(self, baralho):
        vira = baralho.cartas.pop()
        idx = ORDEM_BASE.index(vira.valor)
        prox_idx = (idx + 1) % len(ORDEM_BASE)
        manilha_valor = ORDEM_BASE[prox_idx]
        return vira, manilha_valor

    def forca_carta(self, carta, manilha_valor):
        if carta.valor == manilha_valor:
            return 100 + FORCA_NAIPES[carta.naipe]
        return ORDEM_BASE.index(carta.valor)

    def criar_cartas_jogador(self):
        self.cartas_visuais = []
        start_x = self.width // 2 - 140
        y = self.height - 150
        
        for i, carta in enumerate(self.maos[0]):
            carta_vis = CartaVisual(carta, start_x + i * 100, y)
            self.cartas_visuais.append(carta_vis)

    def handle_event(self, event):
        if self.estado == 'fim_jogo':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.placar_nos = 0
                self.placar_eles = 0
                self.estado = 'jogando'
                self.nova_mao()
            return

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for carta_vis in self.cartas_visuais:
                carta_vis.check_hover(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            # Se está esperando resposta de truco
            if self.esperando_resposta_truco and self.jogador_atual == 0:
                if self.btn_aceitar.collidepoint(mouse_pos):
                    self.responder_truco(aceitar=True)
                elif self.btn_fugir.collidepoint(mouse_pos):
                    self.responder_truco(aceitar=False)
                return
            
            # Se é a vez do jogador humano e não está esperando truco
            if self.jogador_atual == 0 and not self.esperando_resposta_truco:
                # Verifica clique no botão de pedir truco
                if self.pode_pedir_truco and self.valor_rodada == 1 and self.btn_pedir_truco.collidepoint(mouse_pos):
                    self.pedir_truco(0)
                    return
                # Verifica clique no botão de aumentar truco
                if self.pode_pedir_truco and self.valor_rodada >= 3 and self.valor_rodada < 12:
                    # Verifica se pode aumentar (equipe oposta)
                    if self.quem_pediu_truco is not None and (0 % 2 != self.quem_pediu_truco % 2):
                        if self.btn_aumentar_truco.collidepoint(mouse_pos):
                            self.aumentar_truco(0)
                            return
                
                # Verifica clique nas cartas
                for i, carta_vis in enumerate(self.cartas_visuais):
                    if carta_vis.check_hover(mouse_pos):
                        self.jogar_carta_humano(i)
                        break

    def jogar_carta_humano(self, indice):
        carta = self.maos[0].pop(indice)
        self.mesa.append((carta, 0))
        
        # Adiciona carta visual à mesa
        carta_mesa = CartaVisual(carta, self.width//2 - 40, self.height//2 - 60)
        self.cartas_mesa.append((carta_mesa, 0))
        
        # Remove carta visual da mão
        self.cartas_visuais.pop(indice)
        self.reposicionar_cartas_jogador()
        
        # Próximo jogador
        self.proximo_jogador()

    def reposicionar_cartas_jogador(self):
        start_x = self.width // 2 - (len(self.cartas_visuais) * 100) // 2
        y = self.height - 150
        for i, carta_vis in enumerate(self.cartas_visuais):
            carta_vis.x = start_x + i * 100
            carta_vis.y = y
            carta_vis.rect = pygame.Rect(carta_vis.x, carta_vis.y, carta_vis.width, carta_vis.height)

    def proximo_jogador(self):
        self.jogador_atual = (self.jogador_atual + 1) % 4
        
        # Se voltou ao primeiro jogador, processa a rodada
        if self.jogador_atual == self.primeiro_a_jogar:
            self.processar_rodada()

    def pedir_truco(self, jogador_id):
        """Jogador pede truco."""
        if not self.pode_pedir_truco:
            return
        
        proximo_jogador = (jogador_id + 1) % 4
        self.quem_pediu_truco = jogador_id
        self.esperando_resposta_truco = True
        self.jogador_atual = proximo_jogador
        
        self.mensagem = f"Jogador {jogador_id} pediu TRUCO!"
        self.mensagem_timer = 180

    def responder_truco(self, aceitar):
        """Responde ao truco (aceita ou foge)."""
        if not self.esperando_resposta_truco:
            return
        
        self.esperando_resposta_truco = False
        
        if not aceitar:
            # Fugiu - equipe que pediu ganha os pontos atuais
            dupla_vencedora = self.quem_pediu_truco % 2
            if dupla_vencedora == 0:
                self.placar_nos += self.valor_rodada
                self.mensagem = f"Eles fugiram! NÓS ganhamos {self.valor_rodada} ponto(s)!"
            else:
                self.placar_eles += self.valor_rodada
                self.mensagem = f"Fugimos! ELES ganham {self.valor_rodada} ponto(s)!"
            self.mensagem_timer = 120
            
            # Verifica fim do jogo
            if self.placar_nos >= 12 or self.placar_eles >= 12:
                self.estado = 'fim_jogo'
            else:
                self.nova_mao()
        else:
            # Aceitou - aumenta o valor da rodada
            if self.valor_rodada == 1:
                self.valor_rodada = 3
                self.mensagem = "TRUCO ACEITO! Rodada vale 3 pontos!"
            elif self.valor_rodada == 3:
                self.valor_rodada = 6
                self.mensagem = "SEIS ACEITO! Rodada vale 6 pontos!"
            elif self.valor_rodada == 6:
                self.valor_rodada = 9
                self.mensagem = "NOVE ACEITO! Rodada vale 9 pontos!"
            elif self.valor_rodada == 9:
                self.valor_rodada = 12
                self.mensagem = "DOZE ACEITO! Rodada vale 12 pontos!"
            self.mensagem_timer = 120
            
            # Quem pediu truco não pode pedir novamente na mesma queda
            self.pode_pedir_truco = True
            
            # O jogo continua normalmente
            self.jogador_atual = self.quem_pediu_truco

    def aumentar_truco(self, jogador_id):
        """Aumenta o valor do truco (seis, nove, doze)."""
        if self.valor_rodada >= 12:
            return
        
        # Apenas a equipe oposta a quem pediu pode aumentar
        if self.quem_pediu_truco is not None and (jogador_id % 2 == self.quem_pediu_truco % 2):
            return
        
        proximo_jogador = (jogador_id + 1) % 4
        self.quem_pediu_truco = jogador_id
        self.esperando_resposta_truco = True
        self.jogador_atual = proximo_jogador
        
        if self.valor_rodada == 3:
            self.mensagem = f"Jogador {jogador_id} pediu SEIS!"
        elif self.valor_rodada == 6:
            self.mensagem = f"Jogador {jogador_id} pediu NOVE!"
        elif self.valor_rodada == 9:
            self.mensagem = f"Jogador {jogador_id} pediu DOZE!"
        self.mensagem_timer = 180

    def processar_rodada(self):
        # Determina vencedor da vaza
        maior_forca = -1
        vencedores = []
        for carta, jog in self.mesa:
            f = self.forca_carta(carta, self.manilha_valor)
            if f > maior_forca:
                maior_forca = f
                vencedores = [jog]
            elif f == maior_forca:
                vencedores.append(jog)

        if len(vencedores) > 1 and (vencedores[0] % 2 != vencedores[1] % 2):
            self.mensagem = "Rodada CANGADA!"
            self.mensagem_timer = 90
            
            if self.rodada_atual == 1:
                self.primeira_cangada = True
            elif self.vencedor_primeira is not None:
                dupla_vencedora = self.vencedor_primeira % 2
                self.vitorias_queda[dupla_vencedora] += 1
                self.finalizar_queda()
                return
        else:
            vencedor_vaza = vencedores[0]
            dupla_vencedora = vencedor_vaza % 2
            
            if self.primeira_cangada and self.rodada_atual == 2:
                self.vitorias_queda[dupla_vencedora] += 1
                self.primeiro_a_jogar = vencedor_vaza
                self.finalizar_queda()
                return
            else:
                self.vitorias_queda[dupla_vencedora] += 1
                self.primeiro_a_jogar = vencedor_vaza
                
                if self.rodada_atual == 1:
                    self.vencedor_primeira = vencedor_vaza

        # Limpa mesa para próxima rodada
        self.mesa = []
        self.cartas_mesa = []
        self.rodada_atual += 1
        self.jogador_atual = self.primeiro_a_jogar
        
        # Verifica fim da queda
        if self.vitorias_queda[0] == 2:
            self.placar_nos += self.valor_rodada
            self.mensagem = f"NÓS ganhamos a mão! (+{self.valor_rodada})"
            self.mensagem_timer = 120
            self.nova_mao()
        elif self.vitorias_queda[1] == 2:
            self.placar_eles += self.valor_rodada
            self.mensagem = f"ELES ganharam a mão! (+{self.valor_rodada})"
            self.mensagem_timer = 120
            self.nova_mao()
        elif self.rodada_atual > 3:
            # Empate na terceira
            if self.vencedor_primeira is not None:
                dupla_vencedora = self.vencedor_primeira % 2
                self.vitorias_queda[dupla_vencedora] += 1
            self.finalizar_queda()

    def finalizar_queda(self):
        if self.vitorias_queda[0] == 2:
            self.placar_nos += self.valor_rodada
            self.mensagem = f"NÓS ganhamos a mão! (+{self.valor_rodada})"
        else:
            self.placar_eles += self.valor_rodada
            self.mensagem = f"ELES ganharam a mão! (+{self.valor_rodada})"
        
        self.mensagem_timer = 120
        
        # Verifica fim do jogo
        if self.placar_nos >= 12 or self.placar_eles >= 12:
            self.estado = 'fim_jogo'
        else:
            self.nova_mao()

    def escolher_bot(self, jogador_id):
        cartas_ordenadas = sorted(self.maos[jogador_id], 
                                 key=lambda c: self.forca_carta(c, self.manilha_valor))
        
        if not self.mesa:
            carta = cartas_ordenadas[0]
        else:
            melhor_carta_mesa, dono_melhor = max(self.mesa, 
                                                key=lambda item: self.forca_carta(item[0], self.manilha_valor))
            forca_melhor_mesa = self.forca_carta(melhor_carta_mesa, self.manilha_valor)
            
            dupla_parceira = (jogador_id % 2 == dono_melhor % 2)
            if dupla_parceira:
                carta = cartas_ordenadas[0]
            else:
                for c in cartas_ordenadas:
                    if self.forca_carta(c, self.manilha_valor) > forca_melhor_mesa:
                        carta = c
                        break
                else:
                    carta = cartas_ordenadas[0]
        
        self.maos[jogador_id].remove(carta)
        self.mesa.append((carta, jogador_id))
        
        # Posição na mesa baseada no jogador
        posicoes = {
            1: (self.width - 150, self.height // 2 - 60),  # Oponente 1 (direita)
            2: (self.width // 2 - 40, 100),  # Parceiro (topo)
            3: (50, self.height // 2 - 60)  # Oponente 2 (esquerda)
        }
        x, y = posicoes[jogador_id]
        carta_mesa = CartaVisual(carta, x, y)
        self.cartas_mesa.append((carta_mesa, jogador_id))
        
        self.proximo_jogador()

    def bot_deve_pedir_truco(self, jogador_id):
        """Decide se o bot deve pedir truco baseado na força da mão."""
        cartas = self.maos[jogador_id]
        forcas = [self.forca_carta(c, self.manilha_valor) for c in cartas]
        
        # Se tem pelo menos uma manilha ou carta muito forte
        tem_manilha = any(f >= 100 for f in forcas)
        tem_carta_forte = any(f >= 7 for f in forcas)  # A, 2, 3
        
        # Pede truco se tem boas cartas e ainda não pediu nesta queda
        if (tem_manilha or tem_carta_forte) and self.pode_pedir_truco:
            # Não pede se já pediu antes
            if self.quem_pediu_truco is not None and (jogador_id % 2 == self.quem_pediu_truco % 2):
                return False
            return True
        return False

    def bot_decidir_truco(self, jogador_id):
        """Decide se o bot aceita ou foge do truco."""
        cartas = self.maos[jogador_id]
        forcas = [self.forca_carta(c, self.manilha_valor) for c in cartas]
        
        # Se o valor já está alto, só aceita com cartas muito boas
        if self.valor_rodada >= 6:
            tem_manilha = any(f >= 100 for f in forcas)
            return tem_manilha
        
        # Para truco normal (3 pontos), aceita se tem cartas razoáveis
        tem_carta_boa = any(f >= 5 for f in forcas)  # K, A, 2, 3 ou manilha
        return tem_carta_boa

    def update(self):
        if self.mensagem_timer > 0:
            self.mensagem_timer -= 1
        
        # Se está esperando resposta de truco de um bot
        if self.esperando_resposta_truco and self.jogador_atual != 0 and self.estado == 'jogando':
            self.bot_timer += 1
            if self.bot_timer >= 30:
                self.bot_timer = 0
                # Bot decide se aceita ou foge
                aceitar = self.bot_decidir_truco(self.jogador_atual)
                self.responder_truco(aceitar)
        # Bots jogam normalmente
        elif self.jogador_atual != 0 and self.estado == 'jogando' and not self.esperando_resposta_truco:
            self.bot_timer += 1
            if self.bot_timer >= 30:  # ~0.5 segundos a 60 FPS
                self.bot_timer = 0
                # Bot pode pedir truco antes de jogar
                if self.pode_pedir_truco and self.bot_deve_pedir_truco(self.jogador_atual):
                    if self.valor_rodada == 1:
                        self.pedir_truco(self.jogador_atual)
                    else:
                        self.aumentar_truco(self.jogador_atual)
                else:
                    self.escolher_bot(self.jogador_atual)

    def draw(self):
        # Fundo da mesa
        self.screen.fill(VERDE_MESA)
        
        # Desenha informações do jogo
        self.draw_placar()
        self.draw_info_mao()
        
        # Desenha cartas na mesa
        for carta_vis, jogador in self.cartas_mesa:
            carta_vis.draw(self.screen, face_up=True)
        
        # Desenha mãos dos bots (cartas ocultas)
        self.draw_mao_bot(1, self.width - 120, self.height // 2)
        self.draw_mao_bot(2, self.width // 2, 50)
        self.draw_mao_bot(3, 80, self.height // 2)
        
        # Desenha mão do jogador
        for carta_vis in self.cartas_visuais:
            carta_vis.draw(self.screen, face_up=True)
        
        # Desenha botão de pedir truco (apenas para jogador humano)
        if self.jogador_atual == 0 and self.pode_pedir_truco and not self.esperando_resposta_truco:
            if self.valor_rodada == 1:
                pygame.draw.rect(self.screen, AZUL, self.btn_pedir_truco, border_radius=8)
                pygame.draw.rect(self.screen, BRANCO, self.btn_pedir_truco, 2, border_radius=8)
                texto_truco = self.font.render("Pedir Truco", True, BRANCO)
                self.screen.blit(texto_truco, (self.btn_pedir_truco.x + 10, self.btn_pedir_truco.y + 10))
            elif self.valor_rodada >= 3 and self.valor_rodada < 12:
                # Verifica se pode aumentar (equipe oposta)
                if self.quem_pediu_truco is not None and (0 % 2 != self.quem_pediu_truco % 2):
                    texto_aumentar = ""
                    if self.valor_rodada == 3:
                        texto_aumentar = "Pedir Seis"
                    elif self.valor_rodada == 6:
                        texto_aumentar = "Pedir Nove"
                    elif self.valor_rodada == 9:
                        texto_aumentar = "Pedir Doze"
                    
                    pygame.draw.rect(self.screen, AZUL, self.btn_aumentar_truco, border_radius=8)
                    pygame.draw.rect(self.screen, BRANCO, self.btn_aumentar_truco, 2, border_radius=8)
                    texto_btn = self.font.render(texto_aumentar, True, BRANCO)
                    self.screen.blit(texto_btn, (self.btn_aumentar_truco.x + 10, self.btn_aumentar_truco.y + 10))
        
        # Desenha botões de aceitar/fugir quando esperando resposta
        if self.esperando_resposta_truco and self.jogador_atual == 0:
            pygame.draw.rect(self.screen, (0, 200, 0), self.btn_aceitar, border_radius=8)
            pygame.draw.rect(self.screen, BRANCO, self.btn_aceitar, 2, border_radius=8)
            texto_aceitar = self.font.render("Aceitar", True, BRANCO)
            self.screen.blit(texto_aceitar, (self.btn_aceitar.x + 10, self.btn_aceitar.y + 10))
            
            pygame.draw.rect(self.screen, VERMELHO, self.btn_fugir, border_radius=8)
            pygame.draw.rect(self.screen, BRANCO, self.btn_fugir, 2, border_radius=8)
            texto_fugir = self.font.render("Fugir", True, BRANCO)
            self.screen.blit(texto_fugir, (self.btn_fugir.x + 15, self.btn_fugir.y + 10))
        
        # Desenha mensagem
        if self.mensagem_timer > 0:
            self.draw_mensagem()
        
        # Desenha estado do jogo
        if self.estado == 'fim_jogo':
            self.draw_fim_jogo()

    def draw_placar(self):
        # Placar
        texto_nos = self.font.render(f"Nós: {self.placar_nos}", True, BRANCO)
        texto_eles = self.font.render(f"Eles: {self.placar_eles}", True, BRANCO)
        
        self.screen.blit(texto_nos, (20, 20))
        self.screen.blit(texto_eles, (self.width - texto_eles.get_width() - 20, 20))
        
        # Valor da rodada
        texto_valor = self.font.render(f"Rodada vale: {self.valor_rodada} ponto(s)", True, AMARELO)
        self.screen.blit(texto_valor, (self.width // 2 - texto_valor.get_width() // 2, 20))
        
        # Vitórias na queda atual
        texto_vitorias = self.font.render(
            f"Rodadas: Nós {self.vitorias_queda[0]} x {self.vitorias_queda[1]} Eles", 
            True, AMARELO
        )
        self.screen.blit(texto_vitorias, (self.width // 2 - texto_vitorias.get_width() // 2, 50))

    def draw_info_mao(self):
        # Vira e manilha
        if self.vira:
            texto_vira = self.font.render(f"Vira: {self.vira}", True, BRANCO)
            texto_manilha = self.font.render(f"Manilha: {self.manilha_valor}", True, AMARELO)
            
            self.screen.blit(texto_vira, (20, self.height - 200))
            self.screen.blit(texto_manilha, (20, self.height - 170))
        
        # Rodada atual
        texto_rodada = self.font.render(f"Rodada {self.rodada_atual}/3", True, BRANCO)
        self.screen.blit(texto_rodada, (self.width // 2 - texto_rodada.get_width() // 2, 60))

    def carta_e_alta(self, carta):
        """Verifica se a carta é alta (A, 2, 3 ou manilha)."""
        e_manilha = (carta.valor == self.manilha_valor)
        idx_base = ORDEM_BASE.index(carta.valor)
        idx_as = ORDEM_BASE.index('A')
        return e_manilha or idx_base >= idx_as

    def draw_mao_bot(self, jogador_id, x, y):
        quantidade = len(self.maos[jogador_id])
        for i in range(quantidade):
            rect = pygame.Rect(x - quantidade * 15 + i * 30, y, 60, 90)
            
            # Se for o parceiro (jogador 2) e tiver carta alta, mostra a carta
            if jogador_id == 2 and i < len(self.maos[2]) and self.carta_e_alta(self.maos[2][i]):
                carta_vis = CartaVisual(self.maos[2][i], rect.x, rect.y, 60, 90)
                carta_vis.draw(self.screen, face_up=True)
            else:
                # Carta oculta
                pygame.draw.rect(self.screen, (50, 50, 150), rect, border_radius=6)
                pygame.draw.rect(self.screen, BRANCO, rect, 2, border_radius=6)

    def draw_mensagem(self):
        texto = self.font_grande.render(self.mensagem, True, AMARELO)
        fundo = pygame.Rect(
            self.width // 2 - texto.get_width() // 2 - 20,
            self.height // 2 - texto.get_height() // 2 - 20,
            texto.get_width() + 40,
            texto.get_height() + 40
        )
        pygame.draw.rect(self.screen, PRETO, fundo, border_radius=10)
        pygame.draw.rect(self.screen, AMARELO, fundo, 2, border_radius=10)
        self.screen.blit(texto, (fundo.x + 20, fundo.y + 20))

    def draw_fim_jogo(self):
        fundo = pygame.Rect(0, 0, self.width, self.height)
        s = pygame.Surface((self.width, self.height))
        s.set_alpha(200)
        s.fill(PRETO)
        self.screen.blit(s, (0, 0))
        
        if self.placar_nos >= 12:
            texto = self.font_grande.render("PARABÉNS! Você venceu!", True, VERDE_MESA)
        else:
            texto = self.font_grande.render("Você perdeu!", True, VERMELHO)
        
        texto2 = self.font.render("Pressione ESPAÇO para jogar novamente", True, BRANCO)
        
        self.screen.blit(texto, (self.width // 2 - texto.get_width() // 2, self.height // 2 - 50))
        self.screen.blit(texto2, (self.width // 2 - texto2.get_width() // 2, self.height // 2 + 20))
