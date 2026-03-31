import heapq
import time
import random

def creatMapGrid(N, par):
    grid = [random.choices([1, 5], weights=[3, 1], k=N) for _ in range(N)]

    par = max(0, min(par, N * N))
    walls = set()
    while len(walls) < par:
        walls.add((random.randrange(N), random.randrange(N)))
    for x, y in walls:
        grid[x][y] = None

    for row in grid:
        print(
            " ".join("X" if cell is None else ("L" if cell == 5 else ".") for cell in row)
        )
    return grid

def mapGridInitial(grid, init, fim, path=None):
    path_set = set(path or ())

    for i in range(len(grid)):
        row = []
        for j in range(len(grid[i])):
            pos = (i, j)
            cell = grid[i][j]
            if pos == init:
                row.append("I")
            elif pos == fim:
                row.append("F")
            elif pos in path_set:
                row.append("*")
            elif cell is None:
                row.append("X")
            elif cell == 5:
                row.append("L")
            else:
                row.append(".")
        print(" ".join(row))

def manhattanDistance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def createCost(grid):
    return lambda _a, b: grid[b[0]][b[1]]

def neighbors(pos, grid):
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] is not None:
            yield (nx, ny)

def reconstructPath(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def searchAStar(init, fim, grid):
    start_time = time.perf_counter()
    expanded = 0

    h = lambda node: manhattanDistance(node, fim)
    cost = createCost(grid)

    came_from = {}
    g_score = {init: 0}
    open_heap = [(h(init), 0, init)]  # (f, g, node)

    while open_heap:
        _, g_current, current = heapq.heappop(open_heap)
        if g_current != g_score.get(current):
            continue

        expanded += 1
        if current == fim:
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
                heapq.heappush(open_heap, (tentative_g + h(neighbor), tentative_g, neighbor))

    return None

def main():
    n = int(input("Tamanho do mapa: "))
    par = int(input("Quantidade de paredes: "))

    grid = creatMapGrid(n, par)

    init = tuple(map(int, input("Quais os valores iniciais (linha,coluna): ").split(",")))
    if(init[0] < 0 or init[0] >= n or init[1] < 0 or init[1] >= n):
        print(f"Valores iniciais fora do mapa! Use valores entre 0 e {n-1}")
        return
    fim = tuple(map(int, input("Quais os valores finais (linha,coluna): ").split(",")))
    if(fim[0] < 0 or fim[0] >= n or fim[1] < 0 or fim[1] >= n):
        print(f"Valores finais fora do mapa! Use valores entre 0 e {n-1}")
        return

    if grid[init[0]][init[1]] is None:
        print("O início está em uma parede!")
        return

    if grid[fim[0]][fim[1]] is None:
        print("O final está em uma parede!")
        return

    print("\nMapa inicial:")
    mapGridInitial(grid, init, fim)

    result = searchAStar(init, fim, grid)
    if not result:
        print("\nNenhum caminho encontrado")
        return

    print("\nCaminho:", result["path"])
    print("Custo total:", result["cost"])
    print("Nós expandidos:", result["expanded"])
    print(f"Tempo (ms): {result['time_ms']:.3f}")

    print("\nMapa com caminho encontrado:")
    mapGridInitial(grid, init, fim, result["path"])


if __name__ == "__main__":
    main()

"""
I: init (início)
F: fim (fimetivo)
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
