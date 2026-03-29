import random
from collections import deque

def gerarMatriz(n, m):
    # 75% de chance de criar um caminho - 25% de chance de criar uma parede
    caminhos = (1, 1, 1, -1)
    result = [[random.choice(caminhos) for _ in range(m)] for _ in range(n)]
    result[0][0] = 1
    return result

def gerarSaidaLabirinto(labirinto, inicio):
    n = len(labirinto)
    m = len(labirinto[0])

    while True:
        linha = random.randint(0, n-1)
        coluna = random.randint(0, m-1)

        if (linha, coluna) != inicio and labirinto[linha][coluna] == 1:
            return (linha, coluna)

def imprimirLabirinto(labirinto, inicio, saida):
    for i, linha in enumerate(labirinto):
        print(' '.join(
            'S' if (i, j) == saida
            else 'I' if (i, j) == inicio
            else '█' if c == -1
            else '*'
            for j, c in enumerate(linha)
        ))

def BFS(labirinto, inicio, saida):
    direcoes = [
        #L  C
        (0, 1), # direita
        (0, -1), # esquerda
        (1, 0), # cima
        (-1, 0) # baixo
    ]
    fila = deque()
    visitados = []

    fila.append(inicio)
    visitados.append(inicio)

    while fila:
        posicaoAtual = fila.popleft()

        for direcao in direcoes:
            novaLinha = posicaoAtual[0] + direcao[0]
            novaColuna = posicaoAtual[1] + direcao[1]

            if (0 <= novaLinha < len(labirinto)) and (0 <= novaColuna < len(labirinto[0])):
                if labirinto[novaLinha][novaColuna] != -1:
                    if (novaLinha, novaColuna) not in visitados:
                        if (novaLinha, novaColuna) == saida:
                            visitados.append((novaLinha, novaColuna))
                            return {
                                "solution": True,
                                "visitados": visitados
                            }
                        fila.append((novaLinha, novaColuna))
                        visitados.append((novaLinha, novaColuna))

    return {
        "solution": False,
        "visitados": visitados
    }


print("Informe o tamanho n do labirinto")
n = int(input())
print("Informe o tamanho m do labirinto")
m = int(input())

inicio = (0, 0)

labirinto = gerarMatriz(n, m)
saida = gerarSaidaLabirinto(labirinto, inicio)

imprimirLabirinto(labirinto, inicio, saida)

resultado = BFS(labirinto, inicio, saida)
print(resultado["solution"])
print(resultado["visitados"])
