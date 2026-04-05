import time
from collections import deque

from utils import vizinhos, reconstruct_path, calcular_custo_caminho


def busca_largura(grid, inicio, destino):
    start_time = time.perf_counter()

    fila = deque()
    visitados = set()
    came_from = {}
    expanded = 0

    fila.append(inicio)
    visitados.add(inicio)

    while fila:
        atual = fila.popleft()
        expanded += 1

        if atual == destino:
            caminho = reconstruct_path(came_from, atual)
            return {
                "found": True,
                "path": caminho,
                "cost": calcular_custo_caminho(grid, caminho),
                "expanded": expanded,
                "time_ms": (time.perf_counter() - start_time) * 1000.0,
                "guarantee": "menor_numero_de_passos"
            }

        for prox in vizinhos(grid, atual):
            if prox not in visitados:
                visitados.add(prox)
                came_from[prox] = atual
                fila.append(prox)

    return {
        "found": False,
        "path": [],
        "cost": 0,
        "expanded": expanded,
        "time_ms": (time.perf_counter() - start_time) * 1000.0,
        "guarantee": "menor_numero_de_passos"
    }