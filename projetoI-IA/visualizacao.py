import matplotlib.pyplot as plt
import numpy as np


def _create_visual(grid, inicio, destino, caminho=None):
    n = len(grid)
    visual = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if grid[i][j] is None:
                visual[i][j] = 2  # parede
            elif grid[i][j] == 5:
                visual[i][j] = 1  # lama
            else:
                visual[i][j] = 0  # grama

    visual[inicio[0]][inicio[1]] = 3
    visual[destino[0]][destino[1]] = 4

    if caminho:
        for l, c in caminho:
            if (l, c) != inicio and (l, c) != destino:
                visual[l][c] = 5

    return visual


def _create_cmap():
    return plt.cm.colors.ListedColormap([
        "limegreen",  # grama
        "sienna",     # lama
        "black",      # parede
        "royalblue",  # inicio
        "red",        # destino
        "yellow"      # caminho
    ])


def desenhar_um_mapa(grid, inicio, destino, caminho=None, titulo="Mapa"):
    n = len(grid)
    visual = _create_visual(grid, inicio, destino, caminho)

    plt.figure(figsize=(6, 6))
    plt.imshow(visual, cmap=_create_cmap(), vmin=0, vmax=5)
    plt.title(titulo)
    plt.xticks(range(n))
    plt.yticks(range(n))
    plt.grid(True)
    plt.show()


def desenhar_tres_mapas(grid, inicio, destino, caminho=None, nome_algoritmo="Busca"):
    n = len(grid)

    map1 = _create_visual(grid, inicio, destino, None)
    map1[inicio[0]][inicio[1]] = 0
    map1[destino[0]][destino[1]] = 0

    map2 = _create_visual(grid, inicio, destino, None)
    map3 = _create_visual(grid, inicio, destino, caminho)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    titles = [
        "Mapa Inicial",
        "Mapa com Inicio e Fim",
        f"Caminho - {nome_algoritmo}"
    ]
    maps = [map1, map2, map3]

    for ax, mapa, title in zip(axes, maps, titles):
        ax.imshow(mapa, cmap=_create_cmap(), vmin=0, vmax=5)
        ax.set_title(title)
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.grid(True)

    plt.show()


def desenhar_comparacao_profundidade(grid, inicio, destino, caminho_simples=None, caminho_melhor=None):
    n = len(grid)

    map1 = _create_visual(grid, inicio, destino, None)
    map1[inicio[0]][inicio[1]] = 0
    map1[destino[0]][destino[1]] = 0

    map2 = _create_visual(grid, inicio, destino, None)
    map3 = _create_visual(grid, inicio, destino, caminho_simples)
    map4 = _create_visual(grid, inicio, destino, caminho_melhor)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    titles = [
        "Mapa Inicial",
        "Mapa com Inicio e Fim",
        "DFS Simples",
        "DFS com Backtracking"
    ]
    maps = [map1, map2, map3, map4]

    for ax, mapa, title in zip(axes, maps, titles):
        ax.imshow(mapa, cmap=_create_cmap(), vmin=0, vmax=5)
        ax.set_title(title)
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.grid(True)

    plt.tight_layout()
    plt.show()
