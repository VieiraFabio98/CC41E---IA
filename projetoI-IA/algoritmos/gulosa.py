import heapq
import time

from utils import (
    manhattan,
    create_cost,
    vizinhos,
    reconstruct_path
)


def busca_gulosa(grid, inicio, destino):
    start_time = time.perf_counter()
    expanded = 0

    h = lambda node: manhattan(node, destino)
    cost = create_cost(grid)

    came_from = {}
    g_score = {inicio: 0}
    open_heap = [(h(inicio), 0, inicio)]  # (h, g, node)

    while open_heap:
        _, g_current, current = heapq.heappop(open_heap)

        if g_current != g_score.get(current):
            continue

        expanded += 1

        if current == destino:
            return {
                "found": True,
                "path": reconstruct_path(came_from, current),
                "cost": g_current,
                "expanded": expanded,
                "time_ms": (time.perf_counter() - start_time) * 1000.0,
                "guarantee": "nao_garante_melhor_caminho"
            }

        for neighbor in vizinhos(grid, current):
            tentative_g = g_current + cost(current, neighbor)

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                heapq.heappush(open_heap, (h(neighbor), tentative_g, neighbor))

    return {
        "found": False,
        "path": [],
        "cost": 0,
        "expanded": expanded,
        "time_ms": (time.perf_counter() - start_time) * 1000.0,
        "guarantee": "nao_garante_melhor_caminho"
    }
