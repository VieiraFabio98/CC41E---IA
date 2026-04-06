import random
import ast
import matplotlib.pyplot as plt
import numpy as np

def _coerce_grid(grid):
    if isinstance(grid, str):
        text = grid.strip()
        if "=" in text:
            text = text.split("=", 1)[1].strip()
        return ast.literal_eval(text)
    return grid


def draw_three_maps(grid, start, goal, path):
    grid = _coerce_grid(grid)
    N = len(grid)

    def create_visual(show_start=False, show_goal=False, show_path=False):
        visual = np.zeros((N, N))

        for i in range(N):
            for j in range(N):
                if grid[i][j] is None:
                    visual[i][j] = 2  # parede
                elif grid[i][j] == 5:
                    visual[i][j] = 1  # lama
                else:
                    visual[i][j] = 0  # livre

        if show_start:
            visual[start[0]][start[1]] = 3

        if show_goal:
            visual[goal[0]][goal[1]] = 4

        if show_path and path:
            for x, y in path:
                if (x, y) != start and (x, y) != goal:
                    visual[x][y] = 5

        return visual

    # cria os 3 cenários
    map1 = create_visual()
    map2 = create_visual(show_start=True, show_goal=True)
    map3 = create_visual(show_start=True, show_goal=True, show_path=True)

    # mapa de cores
    cmap = plt.cm.colors.ListedColormap([
        "limegreen",   # livre
        "sienna",   # lama
        "black",   # parede
        "royalblue",    # start
        "red",     # goal
        "yellow"    # caminho
    ])

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    titles = ["Mapa Inicial", "Mapa com Inicio e Fim", "Caminho A*"]
    maps = [map1, map2, map3]

    for ax, m, title in zip(axes, maps, titles):
      ax.imshow(m, cmap=cmap, vmin=0, vmax=5)
      ax.set_title(title)
      ax.set_xticks(range(N))
      ax.set_yticks(range(N))
      ax.grid(True)

    plt.show()


def creatMapGrid(N, par, *, print_grid=True):
    grid = [random.choices([1, 5], weights=[3, 1], k=N) for _ in range(N)]

    par = max(0, min(par, N * N))
    walls = set()
    while len(walls) < par:
        walls.add((random.randrange(N), random.randrange(N)))
    for x, y in walls:
        grid[x][y] = None

    if print_grid:
        for row in grid:
            print(
                " ".join(
                    "X" if cell is None else ("L" if cell == 5 else ".") for cell in row
                )
            )

    return grid

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
