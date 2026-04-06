import heapq
import time

from search_utils import (
    creatMapGrid,
    createCost,
    manhattanDistance,
    neighbors,
    reconstructPath,
    draw_three_maps
)

def greedySearch(grid, init, last):
    start_time = time.perf_counter()
    expanded = 0
    h = lambda node: manhattanDistance(node, last)
    cost = createCost(grid)

    came_from = {}
    g_score = {init: 0}
    open_heap = [(h(init), 0, init)]  # (h, g, node)

    while open_heap:
        _, g_current, current = heapq.heappop(open_heap)
        if g_current != g_score.get(current):
            continue

        expanded += 1
        if current == last:
            return {
                "path": reconstructPath(came_from, current),
                "cost": g_current,
                "expanded": expanded,
                "time_ms": (time.perf_counter() - start_time) * 1000.0,
            }

        for neighbor in neighbors(current, grid):
            tentative_g = g_current + cost(current, neighbor)
            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                heapq.heappush(open_heap, (h(neighbor), tentative_g, neighbor))

    return None

def main():
    n = int(input("Tamanho do mapa: "))
    par = int(input("Quantidade de paredes: "))

    grid = creatMapGrid(n, par)

    init = tuple(map(int, input("Quais os valores iniciais (linha,coluna): ").split(",")))
    if(init[0] < 0 or init[0] >= n or init[1] < 0 or init[1] >= n):
        print(f"Valores iniciais fora do mapa! Use valores entre 0 e {n-1}")
        return
    last = tuple(map(int, input("Quais os valores finais (linha,coluna): ").split(",")))
    if(last[0] < 0 or last[0] >= n or last[1] < 0 or last[1] >= n):
        print(f"Valores finais fora do mapa! Use valores entre 0 e {n-1}")
        return

    if grid[init[0]][init[1]] is None:
        print("O início está em uma parede!")
        return

    if grid[last[0]][last[1]] is None:
        print("O final está em uma parede!")
        return

    result = greedySearch(grid, init, last)
    if not result:
        print("\nNenhum caminho encontrado")
        return

    print("\nCaminho:", result["path"])
    print("Custo total:", result["cost"])
    print("Nós expandidos:", result["expanded"])
    print(f"Tempo (ms): {result['time_ms']:.3f}")

    draw_three_maps(grid, init, last, result["path"])


if __name__ == "__main__":
    main()

"""
I: init (início)
F: last (fim)
*: Caminho encontrado pelo A*
.: Terreno normal (custo = 1)
L: Lama (custo = 5)
X: Parede (intransponível) 
-----------------------------
Custos:
Terreno normal (grama): 1
Lama: 5
Parede: intransponível (None)
"""
