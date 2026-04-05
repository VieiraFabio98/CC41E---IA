import random


GRAMA = 1
LAMA = 5
PAREDE = None

SIMBOLOS = {
    GRAMA: ".",
    LAMA: "~",
    PAREDE: "#"
}


def criar_mapa(n, qtd_paredes, *, print_grid=False):
    """Cria um mapa n x n com grama, lama e paredes."""
    grid = [random.choices([GRAMA, LAMA], weights=[3, 1], k=n) for _ in range(n)]

    qtd_paredes = max(0, min(qtd_paredes, n * n - 2))
    paredes = set()

    while len(paredes) < qtd_paredes:
        pos = (random.randrange(n), random.randrange(n))

        if pos == (0, 0) or pos == (n - 1, n - 1):
            continue

        paredes.add(pos)

    for l, c in paredes:
        grid[l][c] = PAREDE

    if print_grid:
        for row in grid:
            print(
                " ".join(
                    "X" if cell is None else ("L" if cell == 5 else ".")
                    for cell in row
                )
            )

    return grid


def dentro(grid, pos):
    l, c = pos
    return 0 <= l < len(grid) and 0 <= c < len(grid[0])


def pode_andar(grid, pos):
    l, c = pos
    return grid[l][c] is not PAREDE


def vizinhos(grid, pos):
    """Retorna os vizinhos validos na ordem cima, direita, baixo e esquerda."""
    l, c = pos
    candidatos = [
        (l - 1, c),
        (l, c + 1),
        (l + 1, c),
        (l, c - 1)
    ]

    validos = []
    for p in candidatos:
        if dentro(grid, p) and pode_andar(grid, p):
            validos.append(p)

    return validos


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def custo_entrada(grid, pos):
    l, c = pos
    return grid[l][c]


def create_cost(grid):
    """Retorna uma funcao para consultar o custo de entrada em cada celula."""
    return lambda _a, b: grid[b[0]][b[1]]


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def calcular_custo_caminho(grid, caminho):
    if not caminho:
        return 0

    total = 0
    for pos in caminho[1:]:
        total += custo_entrada(grid, pos)
    return total


def imprimir_mapa(grid, inicio, destino, caminho=None):
    """Mostra o mapa no terminal."""
    caminho_set = set(caminho) if caminho else set()

    print()
    for i in range(len(grid)):
        linha_saida = []

        for j in range(len(grid[0])):
            pos = (i, j)

            if pos == inicio:
                linha_saida.append("A")
            elif pos == destino:
                linha_saida.append("B")
            elif pos in caminho_set:
                linha_saida.append("*")
            else:
                linha_saida.append(SIMBOLOS[grid[i][j]])

        print(" ".join(linha_saida))
    print()
