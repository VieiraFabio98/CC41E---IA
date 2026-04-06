import time
from collections import deque


def busca_largura(grid, inicio, destino):
    start_time = time.perf_counter()

    direcoes = [
        (0, 1),   # direita
        (0, -1),  # esquerda
        (1, 0),   # baixo
        (-1, 0)   # cima
    ]

    fila = deque()
    visitados = []
    pais = {}
    expanded = 0

    fila.append(inicio)
    visitados.append(inicio)

    while fila:
        posicao_atual = fila.popleft()
        expanded += 1

        if posicao_atual == destino:
            caminho = [destino]
            atual = destino

            while atual in pais:
                atual = pais[atual]
                caminho.append(atual)

            caminho.reverse()

            custo_total = 0
            for posicao in caminho[1:]:
                linha, coluna = posicao
                custo_total += grid[linha][coluna]

            return {
                "found": True,
                "path": caminho,
                "cost": custo_total,
                "expanded": expanded,
                "time_ms": (time.perf_counter() - start_time) * 1000.0,
                "guarantee": "menor_numero_de_passos"
            }

        for direcao in direcoes:
            nova_linha = posicao_atual[0] + direcao[0]
            nova_coluna = posicao_atual[1] + direcao[1]

            if 0 <= nova_linha < len(grid) and 0 <= nova_coluna < len(grid[0]):
                if grid[nova_linha][nova_coluna] is not None:
                    nova_posicao = (nova_linha, nova_coluna)

                    if nova_posicao not in visitados:
                        fila.append(nova_posicao)
                        visitados.append(nova_posicao)
                        pais[nova_posicao] = posicao_atual

    return {
        "found": False,
        "path": [],
        "cost": 0,
        "expanded": expanded,
        "time_ms": (time.perf_counter() - start_time) * 1000.0,
        "guarantee": "menor_numero_de_passos"
    }
