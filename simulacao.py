import random
from game import Carta, Baralho, ORDEM_BASE, FORCA_NAIPES

class JogoTrucoSimulacao:
    def __init__(self):
        self.placar_nos = 0
        self.placar_eles = 0
        self.historico_maos = []
        self.mao_atual = None
        
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
    
    def escolher_bot(self, jogador_id, maos, mesa, manilha_valor):
        cartas_ordenadas = sorted(maos[jogador_id], 
                                 key=lambda c: self.forca_carta(c, manilha_valor))
        
        if not mesa:
            carta = cartas_ordenadas[0]
        else:
            melhor_carta_mesa, dono_melhor = max(mesa, 
                                                key=lambda item: self.forca_carta(item[0], manilha_valor))
            forca_melhor_mesa = self.forca_carta(melhor_carta_mesa, manilha_valor)
            
            dupla_parceira = (jogador_id % 2 == dono_melhor % 2)
            if dupla_parceira:
                carta = cartas_ordenadas[0]
            else:
                for c in cartas_ordenadas:
                    if self.forca_carta(c, manilha_valor) > forca_melhor_mesa:
                        carta = c
                        break
                else:
                    carta = cartas_ordenadas[0]
        
        return carta
    
    def simular_mao(self):
        baralho = Baralho()
        vira, manilha_valor = self.obter_manilha_e_vira(baralho)
        maos = {i: baralho.comprar(3) for i in range(4)}
        
        historico_mao = {
            'vira': vira,
            'manilha': manilha_valor,
            'rodadas': [],
            'vencedor': None
        }
        
        vitorias_queda = {0: 0, 1: 0}
        rodada_atual = 1
        primeiro_a_jogar = 0
        jogador_atual = 0
        primeira_cangada = False
        vencedor_primeira = None
        
        while rodada_atual <= 3:
            mesa = []
            cartas_rodada = []
            
            for _ in range(4):
                carta = self.escolher_bot(jogador_atual, maos, mesa, manilha_valor)
                maos[jogador_atual].remove(carta)
                mesa.append((carta, jogador_atual))
                cartas_rodada.append((carta, jogador_atual))
                jogador_atual = (jogador_atual + 1) % 4
            
            # Determina vencedor da vaza
            maior_forca = -1
            vencedores = []
            for carta, jog in mesa:
                f = self.forca_carta(carta, manilha_valor)
                if f > maior_forca:
                    maior_forca = f
                    vencedores = [jog]
                elif f == maior_forca:
                    vencedores.append(jog)
            
            historico_mao['rodadas'].append({
                'numero': rodada_atual,
                'cartas': [(c, j) for c, j in cartas_rodada],
                'vencedor_vaza': vencedores[0] if len(vencedores) == 1 else None,
                'cangada': len(vencedores) > 1 and (vencedores[0] % 2 != vencedores[1] % 2)
            })
            
            if len(vencedores) > 1 and (vencedores[0] % 2 != vencedores[1] % 2):
                if rodada_atual == 1:
                    primeira_cangada = True
                elif vencedor_primeira is not None:
                    dupla_vencedora = vencedor_primeira % 2
                    vitorias_queda[dupla_vencedora] += 1
                    break
            else:
                vencedor_vaza = vencedores[0]
                dupla_vencedora = vencedor_vaza % 2
                
                if primeira_cangada and rodada_atual == 2:
                    vitorias_queda[dupla_vencedora] += 1
                    primeiro_a_jogar = vencedor_vaza
                    break
                else:
                    vitorias_queda[dupla_vencedora] += 1
                    primeiro_a_jogar = vencedor_vaza
                    
                    if rodada_atual == 1:
                        vencedor_primeira = vencedor_vaza
            
            rodada_atual += 1
            jogador_atual = primeiro_a_jogar
        
        # Empate na terceira
        if rodada_atual > 3 and vitorias_queda[0] < 2 and vitorias_queda[1] < 2:
            if vencedor_primeira is not None:
                dupla_vencedora = vencedor_primeira % 2
                vitorias_queda[dupla_vencedora] += 1
        
        if vitorias_queda[0] == 2:
            self.placar_nos += 1
            historico_mao['vencedor'] = 'Nós'
        else:
            self.placar_eles += 1
            historico_mao['vencedor'] = 'Eles'
        
        self.historico_maos.append(historico_mao)
        return historico_mao
    
    def simular_jogo_completo(self):
        self.historico_maos = []
        self.placar_nos = 0
        self.placar_eles = 0
        
        while self.placar_nos < 12 and self.placar_eles < 12:
            self.simular_mao()
        
        return self.historico_maos
    
    def imprimir_tabela(self):
        print("\n" + "=" * 120)
        print("SIMULAÇÃO DE JOGO DE TRUCO PAULISTA")
        print("=" * 120)
        print(f"\nPlacar Final: Nós {self.placar_nos} x {self.placar_eles} Eles")
        print(f"Vencedor: {'NÓS' if self.placar_nos >= 12 else 'ELES'}")
        print("\n" + "=" * 120)
        
        for idx, mao in enumerate(self.historico_maos, 1):
            print(f"\nMÃO {idx} - Vira: {mao['vira']} | Manilha: {mao['manilha']}")
            print("-" * 120)
            print(f"{'Rodada':<8} {'J0 (Nós)':<20} {'J1 (Eles)':<20} {'J2 (Nós)':<20} {'J3 (Eles)':<20} {'Vencedor':<15} {'Cangada?':<10}")
            print("-" * 120)
            
            for rodada in mao['rodadas']:
                cartas_por_jogador = {0: '-', 1: '-', 2: '-', 3: '-'}
                for carta, jogador in rodada['cartas']:
                    cartas_por_jogador[jogador] = str(carta)
                
                vencedor_str = f"J{rodada['vencedor_vaza']}" if rodada['vencedor_vaza'] is not None else "-"
                cangada_str = "SIM" if rodada['cangada'] else "NÃO"
                
                print(f"{rodada['numero']:<8} {cartas_por_jogador[0]:<20} {cartas_por_jogador[1]:<20} {cartas_por_jogador[2]:<20} {cartas_por_jogador[3]:<20} {vencedor_str:<15} {cangada_str:<10}")
            
            print("-" * 120)
            print(f"Vencedor da mão: {mao['vencedor']}")
            print(f"Placar após esta mão: Nós {self.placar_nos} x {self.placar_eles} Eles")
        
        print("\n" + "=" * 120)
        print("EVOLUÇÃO DO PLACAR")
        print("=" * 120)
        print(f"{'Mão':<6} {'Placar Nós':<15} {'Placar Eles':<15} {'Vencedor':<15}")
        print("-" * 120)
        
        placar_nos_acumulado = 0
        placar_eles_acumulado = 0
        for idx, mao in enumerate(self.historico_maos, 1):
            if mao['vencedor'] == 'Nós':
                placar_nos_acumulado += 1
            else:
                placar_eles_acumulado += 1
            
            print(f"{idx:<6} {placar_nos_acumulado:<15} {placar_eles_acumulado:<15} {mao['vencedor']:<15}")
        
        print("=" * 120 + "\n")


if __name__ == "__main__":
    jogo = JogoTrucoSimulacao()
    jogo.simular_jogo_completo()
    jogo.imprimir_tabela()
