import heapq
import itertools
import time


def busca_a_estrela(grid, inicio, destino):
    start_time = time.perf_counter()

    fila_prioridade = []
    pais = {}
    custo_ate_agora = {inicio: 0}
    fechados = []
    ordem_insercao = itertools.count()
    expanded = 0

    direcoes = [
        (-1, 0),  # cima
        (0, 1),   # direita
        (1, 0),   # baixo
        (0, -1)   # esquerda
    ]

    heuristica_inicial = abs(inicio[0] - destino[0]) + abs(inicio[1] - destino[1])
    heapq.heappush(
        fila_prioridade,
        (heuristica_inicial, heuristica_inicial, next(ordem_insercao), 0, inicio)
    )

    while fila_prioridade:
        _, _, _, custo_atual, posicao_atual = heapq.heappop(fila_prioridade)

        if custo_atual != custo_ate_agora.get(posicao_atual):
            continue

        if posicao_atual in fechados:
            continue

        fechados.append(posicao_atual)
        expanded += 1

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
                "time_ms": (time.perf_counter() - start_time) * 1000.0,
                "guarantee": "melhor_caminho_com_heuristica"
            }

        linha = posicao_atual[0]
        coluna = posicao_atual[1]

        for direcao in direcoes:
            nova_linha = linha + direcao[0]
            nova_coluna = coluna + direcao[1]

            if 0 <= nova_linha < len(grid) and 0 <= nova_coluna < len(grid[0]):
                if grid[nova_linha][nova_coluna] is not None:
                    nova_posicao = (nova_linha, nova_coluna)

                    if nova_posicao in fechados:
                        continue

                    novo_custo = custo_atual + grid[nova_linha][nova_coluna]

                    if novo_custo < custo_ate_agora.get(nova_posicao, float("inf")):
                        custo_ate_agora[nova_posicao] = novo_custo
                        pais[nova_posicao] = posicao_atual

                        heuristica = abs(nova_linha - destino[0]) + abs(nova_coluna - destino[1])
                        prioridade = novo_custo + heuristica

                        heapq.heappush(
                            fila_prioridade,
                            (prioridade, heuristica, next(ordem_insercao), novo_custo, nova_posicao)
                        )

    return {
        "found": False,
        "path": [],
        "cost": 0,
        "expanded": expanded,
        "time_ms": (time.perf_counter() - start_time) * 1000.0,
        "guarantee": "melhor_caminho_com_heuristica"
    }
