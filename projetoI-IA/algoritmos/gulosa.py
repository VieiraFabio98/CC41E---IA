import heapq
import time


def busca_gulosa(grid, inicio, destino):
    start_time = time.perf_counter()

    fila_prioridade = []
    pais = {}
    custo_ate_agora = {inicio: 0}
    expanded = 0
    nos_expandidos = []
    revisitas = 0
    nos_revisitados = []
    passos_animacao = []

    direcoes = [
        (-1, 0),  # cima
        (0, 1),   # direita
        (1, 0),   # baixo
        (0, -1)   # esquerda
    ]

    heuristica_inicial = abs(inicio[0] - destino[0]) + abs(inicio[1] - destino[1])
    heapq.heappush(fila_prioridade, (heuristica_inicial, 0, inicio))

    while fila_prioridade:
        _, custo_atual, posicao_atual = heapq.heappop(fila_prioridade)

        if custo_atual != custo_ate_agora.get(posicao_atual):
            revisitas += 1
            nos_revisitados.append(posicao_atual)
            passos_animacao.append(("revisit", posicao_atual))
            continue

        expanded += 1
        nos_expandidos.append(posicao_atual)
        passos_animacao.append(("expand", posicao_atual))

        if posicao_atual == destino:
            caminho = [destino]
            atual = destino

            while atual in pais:
                atual = pais[atual]
                caminho.append(atual)

            caminho.reverse()

            return {
                "found": True,
                "path": caminho,
                "cost": custo_atual,
                "expanded": expanded,
                "expanded_nodes": nos_expandidos,
                "revisitas": revisitas,
                "revisited_nodes": nos_revisitados,
                "passos_animacao": passos_animacao,
                "time_ms": (time.perf_counter() - start_time) * 1000.0,
                "guarantee": "nao_garante_melhor_caminho"
            }

        linha = posicao_atual[0]
        coluna = posicao_atual[1]

        for direcao in direcoes:
            nova_linha = linha + direcao[0]
            nova_coluna = coluna + direcao[1]

            if 0 <= nova_linha < len(grid) and 0 <= nova_coluna < len(grid[0]):
                if grid[nova_linha][nova_coluna] is not None:
                    nova_posicao = (nova_linha, nova_coluna)
                    novo_custo = custo_atual + grid[nova_linha][nova_coluna]

                    if novo_custo < custo_ate_agora.get(nova_posicao, float("inf")):
                        custo_ate_agora[nova_posicao] = novo_custo
                        pais[nova_posicao] = posicao_atual

                        heuristica = abs(nova_linha - destino[0]) + abs(nova_coluna - destino[1])
                        heapq.heappush(fila_prioridade, (heuristica, novo_custo, nova_posicao))
                    else:
                        revisitas += 1
                        nos_revisitados.append(nova_posicao)
                        passos_animacao.append(("revisit", nova_posicao))

    return {
        "found": False,
        "path": [],
        "cost": 0,
        "expanded": expanded,
        "expanded_nodes": nos_expandidos,
        "revisitas": revisitas,
        "revisited_nodes": nos_revisitados,
        "passos_animacao": passos_animacao,
        "time_ms": (time.perf_counter() - start_time) * 1000.0,
        "guarantee": "nao_garante_melhor_caminho"
    }
