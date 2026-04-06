import time


def busca_profundidade_simples(grid, inicio, destino):
    visitado = []
    caminho_atual = []
    caminho_encontrado = []
    nos_expandidos = 0
    revisitas = 0

    direcoes = [
        (-1, 0),  # cima
        (0, 1),   # direita
        (1, 0),   # baixo
        (0, -1)   # esquerda
    ]

    def recursao(posicao_atual, custo_ate_aqui):
        nonlocal caminho_encontrado, nos_expandidos, revisitas

        linha = posicao_atual[0]
        coluna = posicao_atual[1]

        if posicao_atual in visitado:
            revisitas += 1
            return None

        visitado.append(posicao_atual)
        caminho_atual.append(posicao_atual)
        nos_expandidos += 1

        if posicao_atual == destino:
            caminho_encontrado = caminho_atual.copy()
            caminho_atual.pop()
            visitado.pop()
            return custo_ate_aqui

        for direcao in direcoes:
            nova_linha = linha + direcao[0]
            nova_coluna = coluna + direcao[1]

            if 0 <= nova_linha < len(grid) and 0 <= nova_coluna < len(grid[0]):
                if grid[nova_linha][nova_coluna] is not None:
                    nova_posicao = (nova_linha, nova_coluna)

                    if nova_posicao not in visitado:
                        novo_custo = custo_ate_aqui + grid[nova_linha][nova_coluna]
                        resultado = recursao(nova_posicao, novo_custo)
                        if resultado is not None:
                            caminho_atual.pop()
                            visitado.pop()
                            return resultado
                    else:
                        revisitas += 1

        caminho_atual.pop()
        visitado.pop()
        return None

    t0 = time.perf_counter()
    custo = recursao(inicio, 0)
    t1 = time.perf_counter()

    return {
        "found": len(caminho_encontrado) > 0,
        "path": caminho_encontrado,
        "cost": custo if custo is not None else 0,
        "expanded": nos_expandidos,
        "revisitas": revisitas,
        "time_ms": (t1 - t0) * 1000,
        "guarantee": "primeiro_caminho_encontrado"
    }


def busca_profundidade_melhor(grid, inicio, destino):
    visitado = []
    caminho_atual = []
    melhor_caminho = []
    melhor_custo = float("inf")
    nos_expandidos = 0
    revisitas = 0

    direcoes = [
        (-1, 0),  # cima
        (0, 1),   # direita
        (1, 0),   # baixo
        (0, -1)   # esquerda
    ]

    def recursao(posicao_atual, custo_ate_aqui):
        nonlocal melhor_caminho, melhor_custo, nos_expandidos, revisitas

        linha = posicao_atual[0]
        coluna = posicao_atual[1]

        if posicao_atual in visitado:
            revisitas += 1
            return

        visitado.append(posicao_atual)
        caminho_atual.append(posicao_atual)
        nos_expandidos += 1

        if custo_ate_aqui >= melhor_custo:
            caminho_atual.pop()
            visitado.pop()
            return

        if posicao_atual == destino:
            melhor_custo = custo_ate_aqui
            melhor_caminho = caminho_atual.copy()
            caminho_atual.pop()
            visitado.pop()
            return

        for direcao in direcoes:
            nova_linha = linha + direcao[0]
            nova_coluna = coluna + direcao[1]

            if 0 <= nova_linha < len(grid) and 0 <= nova_coluna < len(grid[0]):
                if grid[nova_linha][nova_coluna] is not None:
                    nova_posicao = (nova_linha, nova_coluna)

                    if nova_posicao not in visitado:
                        novo_custo = custo_ate_aqui + grid[nova_linha][nova_coluna]
                        recursao(nova_posicao, novo_custo)
                    else:
                        revisitas += 1

        caminho_atual.pop()
        visitado.pop()

    t0 = time.perf_counter()
    recursao(inicio, 0)
    t1 = time.perf_counter()

    return {
        "found": len(melhor_caminho) > 0,
        "path": melhor_caminho,
        "cost": melhor_custo if melhor_caminho else 0,
        "expanded": nos_expandidos,
        "revisitas": revisitas,
        "time_ms": (t1 - t0) * 1000,
        "guarantee": "melhor_custo_por_backtracking"
    }


def busca_profundidade(grid, inicio, destino):
    return {
        "simples": busca_profundidade_simples(grid, inicio, destino),
        "melhor": busca_profundidade_melhor(grid, inicio, destino)
    }
