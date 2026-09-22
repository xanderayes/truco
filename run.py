import random

# Definindo a ordem base de força das cartas do Truco Paulista
ORDEM_BASE = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']

# Na manilha, a força do naipe define o desempate (Paus > Copas > Espadas > Ouros)
FORCA_NAIPES = {'Paus': 4, 'Copas': 3, 'Espadas': 2, 'Ouros': 1}

NAIPES = ['Ouros', 'Espadas', 'Copas', 'Paus']

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

class JogoTruco:
    def __init__(self):
        self.placar_nos = 0
        self.placar_eles = 0

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

    def formatar_mao_sinais(self, mao, manilha_valor):
        """Retorna a mão do parceiro mostrando apenas cartas >= Ás ou Manilhas."""
        reveladas = []
        for c in mao:
            e_manilha = (c.valor == manilha_valor)
            idx_base = ORDEM_BASE.index(c.valor)
            idx_as = ORDEM_BASE.index('A')
            
            if e_manilha or idx_base >= idx_as:
                reveladas.append(str(c))
            else:
                reveladas.append("[Oculta]")
        return ", ".join(reveladas)

    def escolher_bot(self, jogador_id, mao, mesa, manilha_valor, eh_parceiro=False, mao_parceiro=None):
        """Heurística simples para tomada de decisão dos bots."""
        cartas_ordenadas = sorted(mao, key=lambda c: self.forca_carta(c, manilha_valor))
        
        # Se a mesa estiver vazia, joga a carta mais fraca
        if not mesa:
            return cartas_ordenadas[0]
        
        melhor_carta_mesa, dono_melhor = max(mesa, key=lambda item: self.forca_carta(item[0], manilha_valor))
        forca_melhor_mesa = self.forca_carta(melhor_carta_mesa, manilha_valor)
        
        # Se o parceiro já está ganhando a mesa, descarta a carta mais fraca
        dupla_parceira = (jogador_id % 2 == dono_melhor % 2)
        if dupla_parceira:
            return cartas_ordenadas[0]

        # Tenta matar a carta da mesa com a menor carta possível que vença
        for c in cartas_ordenadas:
            if self.forca_carta(c, manilha_valor) > forca_melhor_mesa:
                return c

        # Se não consegue matar, descarta a mais fraca
        return cartas_ordenadas[0]

    def jogar_rodada(self):
        baralho = Baralho()
        vira, manilha_valor = self.obter_manilha_e_vira(baralho)

        # Jogadores: 0 = Você, 1 = Oponente 1, 2 = Parceiro Bot, 3 = Oponente 2
        maos = {i: baralho.comprar(3) for i in range(4)}
        vitorias_queda = {0: 0, 1: 0} # 0: Nós (0 e 2), 1: Eles (1 e 3)
        
        # Rastrear cangadas e vencedor da primeira rodada
        primeira_cangada = False
        vencedor_primeira = None
        
        print("\n" + "="*50)
        print(f"NOVA MÃO! Vira: {vira} | Manilha: {manilha_valor}")
        print("="*50)

        primeiro_a_jogar = random.randint(0, 3)

        for rodada in range(1, 4):
            print(f"\n--- RODADA {rodada} ---")
            
            # Exibir a mão do usuário e os sinais recebidos do parceiro (Bot 2)
            sinais_parceiro = self.formatar_mao_sinais(maos[2], manilha_valor)
            print(f"Sua mão: {maos[0]}")
            print(f"Sinais do seu Parceiro (Bot 2): [{sinais_parceiro}]")
            
            mesa = []
            ordem_jogada = [(primeiro_a_jogar + i) % 4 for i in range(4)]

            for jog in ordem_jogada:
                if jog == 0:
                    # Jogada Humana
                    print("\nSua vez de jogar:")
                    for idx, c in enumerate(maos[0]):
                        print(f"  [{idx}] {c}")
                    
                    while True:
                        try:
                            escolha = int(input("Escolha o índice da carta: "))
                            if 0 <= escolha < len(maos[0]):
                                carta_jogada = maos[0].pop(escolha)
                                break
                        except ValueError:
                            pass
                        print("Escolha inválida, tente novamente.")
                    print(f"Você jogou: {carta_jogada}")
                else:
                    nome = f"Oponente {jog}" if jog in [1, 3] else "Parceiro Bot (2)"
                    carta_jogada = self.escolher_bot(
                        jog, maos[jog], mesa, manilha_valor, 
                        eh_parceiro=(jog == 2), mao_parceiro=maos[0]
                    )
                    maos[jog].remove(carta_jogada)
                    print(f"{nome} jogou: {carta_jogada}")

                mesa.append((carta_jogada, jog))

            # Determinar vencedor da vaza
            maior_forca = -1
            vencedores = []
            for carta, jog in mesa:
                f = self.forca_carta(carta, manilha_valor)
                if f > maior_forca:
                    maior_forca = f
                    vencedores = [jog]
                elif f == maior_forca:
                    vencedores.append(jog)

            if len(vencedores) > 1 and (vencedores[0] % 2 != vencedores[1] % 2):
                print(">> Rodada CANGADA (Empate)!")
                vencedor_vaza = None
                
                # Regra oficial: se primeira rodada cangada, marca para decisão na próxima
                if rodada == 1:
                    primeira_cangada = True
                # Regra oficial: se segunda/terceira cangada, quem ganhou a primeira ganha a mão
                elif vencedor_primeira is not None:
                    dupla_vencedora = vencedor_primeira % 2
                    vitorias_queda[dupla_vencedora] += 1
                    nome_vencedor = "Nós" if dupla_vencedora == 0 else "Eles"
                    print(f">> Pela regra de cangada, {nome_vencedor} ganham a mão!")
            else:
                vencedor_vaza = vencedores[0]
                dupla_vencedora = vencedor_vaza % 2
                
                # Se primeira cangada, quem ganha a próxima ganha a mão
                if primeira_cangada and rodada == 2:
                    vitorias_queda[dupla_vencedora] += 1
                    primeiro_a_jogar = vencedor_vaza
                    nome_vencedor = "Nós" if dupla_vencedora == 0 else "Eles"
                    print(f">> {nome_vencedor} ganham a mão (após cangada na primeira)!")
                else:
                    vitorias_queda[dupla_vencedora] += 1
                    primeiro_a_jogar = vencedor_vaza
                    nome_vencedor = "Nós" if dupla_vencedora == 0 else "Eles"
                    print(f">> Vencedor da rodada: {nome_vencedor} (Jogador {vencedor_vaza})")
                
                # Salva vencedor da primeira rodada para regra de cangada
                if rodada == 1:
                    vencedor_primeira = vencedor_vaza

            # Checar fim da queda
            if vitorias_queda[0] == 2:
                print("\n>>> NÓS ganhamos esta mão (2 pontos/vazas)! <<<")
                self.placar_nos += 1
                break
            elif vitorias_queda[1] == 2:
                print("\n>>> ELES ganharam esta mão (2 pontos/vazas)! <<<")
                self.placar_eles += 1
                break

    def iniciar(self):
        while self.placar_nos < 12 and self.placar_eles < 12:
            falta_nos = 12 - self.placar_nos
            falta_eles = 12 - self.placar_eles
            print(f"\n{'='*50}")
            print(f"PLACAR GERAL: Nós {self.placar_nos} x {self.placar_eles} Eles")
            print(f"Faltam: Nós {falta_nos} pontos | Eles {falta_eles} pontos")
            print(f"{'='*50}")
            self.jogar_rodada()
            input("\nPressione Enter para ir para a próxima mão...")
        
        print("\nFIM DE JOGO!")
        if self.placar_nos >= 12:
            print("Parabéns! Sua dupla venceu o jogo!")
        else:
            print("Os oponentes venceram o jogo.")

if __name__ == "__main__":
    jogo = JogoTruco()
    jogo.iniciar()