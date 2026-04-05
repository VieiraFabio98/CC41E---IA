import heapq
import itertools
import time

from utils import (
    manhattan,
    create_cost,
    vizinhos,
    reconstruct_path
)


def busca_a_estrela(grid, inicio, destino):
    start_time = time.perf_counter()
    expanded = 0

    h = lambda node: manhattan(node, destino)
    cost = create_cost(grid)

    came_from = {}
    g_score = {inicio: 0}
    closed = set()
    push_count = itertools.count()

    open_heap = [
        (h(inicio), h(inicio), next(push_count), 0, inicio)
    ]  # (f, h, _, g, node)

    while open_heap:
        _, _, _, g_current, current = heapq.heappop(open_heap)

        if g_current != g_score.get(current):
            continue

        if current in closed:
            continue

        closed.add(current)
        expanded += 1

        if current == destino:
            return {
                "found": True,
                "path": reconstruct_path(came_from, current),
                "cost": g_current,
                "expanded": expanded,
                "time_ms": (time.perf_counter() - start_time) * 1000.0,
                "guarantee": "melhor_caminho_com_heuristica"
            }

        for neighbor in vizinhos(grid, current):
            if neighbor in closed:
                continue

            tentative_g = g_current + cost(current, neighbor)

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                h_neighbor = h(neighbor)

                heapq.heappush(
                    open_heap,
                    (
                        tentative_g + h_neighbor,
                        h_neighbor,
                        next(push_count),
                        tentative_g,
                        neighbor
                    ),
                )

    return {
        "found": False,
        "path": [],
        "cost": 0,
        "expanded": expanded,
        "time_ms": (time.perf_counter() - start_time) * 1000.0,
        "guarantee": "melhor_caminho_com_heuristica"
    }
