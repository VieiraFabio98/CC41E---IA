import time

from utils import vizinhos, custo_entrada


def busca_profundidade_simples(grid, inicio, destino):
    n = len(grid)
    visitado = [[False] * n for _ in range(n)]
    caminho_atual = []
    caminho_encontrado = []
    nos_expandidos = 0
    revisitas = 0
    encontrou = False

    def recursao(pos, custo_ate_aqui):
        nonlocal caminho_encontrado, nos_expandidos, revisitas, encontrou

        if encontrou:
            return None

        l, c = pos
        if visitado[l][c]:
            revisitas += 1
            return None

        visitado[l][c] = True
        caminho_atual.append(pos)
        nos_expandidos += 1

        if pos == destino:
            caminho_encontrado = caminho_atual.copy()
            encontrou = True
            caminho_atual.pop()
            visitado[l][c] = False
            return custo_ate_aqui

        for prox in vizinhos(grid, pos):
            pl, pc = prox
            if not visitado[pl][pc]:
                resultado = recursao(prox, custo_ate_aqui + custo_entrada(grid, prox))
                if resultado is not None:
                    caminho_atual.pop()
                    visitado[l][c] = False
                    return resultado
            else:
                revisitas += 1

        caminho_atual.pop()
        visitado[l][c] = False
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
    n = len(grid)
    visitado = [[False] * n for _ in range(n)]

    melhor_caminho = []
    melhor_custo = float("inf")
    nos_expandidos = 0
    revisitas = 0
    caminho_atual = []

    def recursao(pos, custo_ate_aqui):
        nonlocal melhor_custo, melhor_caminho, nos_expandidos, revisitas

        l, c = pos

        if visitado[l][c]:
            revisitas += 1
            return

        visitado[l][c] = True
        caminho_atual.append(pos)
        nos_expandidos += 1

        if custo_ate_aqui >= melhor_custo:
            caminho_atual.pop()
            visitado[l][c] = False
            return

        if pos == destino:
            melhor_custo = custo_ate_aqui
            melhor_caminho = caminho_atual.copy()
        else:
            for prox in vizinhos(grid, pos):
                pl, pc = prox

                if not visitado[pl][pc]:
                    prox_custo = custo_ate_aqui + custo_entrada(grid, prox)
                    recursao(prox, prox_custo)
                else:
                    revisitas += 1

        caminho_atual.pop()
        visitado[l][c] = False

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
