"""
Módulo de Busca em Profundidade
UTFPR-PG
Autores: Fabio, Jhenyfer, Monique
"""

import random
import time

# -- configs do terreno --
C_GRAMA = 1
C_LAMA = 5
PAREDE = -1

# símbolos pra mostrar
SIMB = {
    C_GRAMA: ".",
    C_LAMA: "~",
    PAREDE: "#"
}

def monta_mapa(tam):
    """cria mapa com grama e lama"""
    mapa = []
    for i in range(tam):
        linha = []
        for j in range(tam):
            # escolhe aleatório entre grama e lama
            terreno = random.choice([C_GRAMA, C_LAMA])
            linha.append(terreno)
        mapa.append(linha)
    return mapa

def poe_paredes(mapa, qtd, inicio, destino):
    n = len(mapa)
    coloc = 0
    # evita loop infinito se qtd for grande
    max_tent = qtd * 20 + 100
    tent = 0
    while coloc < qtd and tent < max_tent:
        l = random.randint(0, n-1)
        c = random.randint(0, n-1)
        # não coloca parede no início nem no destino
        if (l, c) == inicio or (l, c) == destino:
            tent += 1
            continue
        if mapa[l][c] != PAREDE:
            mapa[l][c] = PAREDE
            coloc += 1
        tent += 1
    # se não conseguiu colocar todas, avisa mas continua seguindo
    if coloc < qtd:
        print(f"  (só consegui colocar {coloc} paredes de {qtd})")

def exibe_mapa(mapa, inicio, destino, caminho=None):
    n = len(mapa)
    conj_caminho = set(caminho) if caminho else set()
    print()
    for i in range(n):
        linha_txt = []
        for j in range(n):
            p = (i, j)
            if p == inicio:
                linha_txt.append("A")
            elif p == destino:
                linha_txt.append("B")
            elif p in conj_caminho:
                linha_txt.append("*")
            else:
                linha_txt.append(SIMB[mapa[i][j]])
        print(" ".join(linha_txt))
    print()

def dentro(l, c, n):
    return 0 <= l < n and 0 <= c < n

def pode(mapa, l, c):
    return mapa[l][c] != PAREDE

def vizinhos(l, c):
    # ordem mais padrão: cima, direita, baixo, esquerda
    # (deixei assim porque funcionou nos testes)
    return [(l-1, c), (l, c+1), (l+1, c), (l, c-1)]

def calcula_custo(mapa, caminho):
    tot = 0
    # começa do 1 porque a origem não tem custo
    for i in range(1, len(caminho)):
        l, c = caminho[i]
        tot += mapa[l][c]
    return tot

def busca_dfs(mapa, inicio, destino):
    n = len(mapa)
    visitado = [[False]*n for _ in range(n)]
    
    melhor_caminho = []
    melhor_custo = float('inf')
    nos_expandidos = 0
    revisitas = 0
    caminho_atual = []
    
    def recursao(l, c, custo_ate_aqui):
        nonlocal melhor_custo, melhor_caminho, nos_expandidos, revisitas
        
        if not dentro(l, c, n) or not pode(mapa, l, c):
            return
        if visitado[l][c]:
            revisitas += 1
            return
        
        visitado[l][c] = True
        caminho_atual.append((l, c))
        nos_expandidos += 1
        
        # poda: se já tá pior que o melhor, desiste
        if custo_ate_aqui >= melhor_custo:
            caminho_atual.pop()
            visitado[l][c] = False
            return
        
        if (l, c) == destino:
            # chegou, e é melhor porque passou pela poda
            melhor_custo = custo_ate_aqui
            melhor_caminho = caminho_atual.copy()
        else:
            for pl, pc in vizinhos(l, c):
                if dentro(pl, pc, n) and pode(mapa, pl, pc):
                    prox_custo = custo_ate_aqui
                    if not visitado[pl][pc]:
                        prox_custo += mapa[pl][pc]
                    recursao(pl, pc, prox_custo)
        
        # backtrack
        caminho_atual.pop()
        visitado[l][c] = False
    
    t0 = time.perf_counter()
    recursao(inicio[0], inicio[1], 0)
    t1 = time.perf_counter()
    tempo_ms = (t1 - t0) * 1000
    
    return {
        "ok": len(melhor_caminho) > 0,
        "caminho": melhor_caminho,
        "custo": melhor_custo if melhor_caminho else 0,
        "expandidos": nos_expandidos,
        "revisitas": revisitas,
        "tempo": tempo_ms
    }

def main():
    print("=== BUSCA EM PROFUNDIDADE (DFS com poda) ===")
    print()
    
    # entrada com validação simples
    try:
        n = int(input("Tamanho do mapa n x n: "))
        if n < 2:
            print("Muito pequeno, vou usar 2")
            n = 2
    except:
        print("Valor inválido, usando 10")
        n = 10
    
    try:
        paredes = int(input("Quantidade de paredes: "))
        if paredes < 0:
            paredes = 0
    except:
        print("Inválido, sem paredes")
        paredes = 0
    
    max_paredes = n*n - 2
    if paredes > max_paredes:
        print(f"Muitas paredes, vou limitar pra {max_paredes}")
        paredes = max_paredes
    
    inicio = (0, 0)
    destino = (n-1, n-1)
    
    mapa = monta_mapa(n)
    poe_paredes(mapa, paredes, inicio, destino)
    
    print("\nMapa inicial:")
    exibe_mapa(mapa, inicio, destino)
    
    resultado = busca_dfs(mapa, inicio, destino)
    
    if resultado["ok"]:
        print("Caminho encontrado (coordenadas):")
        print(resultado["caminho"])
        print("\nMapa com o melhor caminho:")
        exibe_mapa(mapa, inicio, destino, resultado["caminho"])
        print(f"Custo total: {resultado['custo']}")
        print(f"Nós expandidos: {resultado['expandidos']}")
        print(f"Revisitas: {resultado['revisitas']}")
        print(f"Tempo: {resultado['tempo']:.3f} ms")
    else:
        print("Nenhum caminho encontrado :(")
        print(f"Nós expandidos: {resultado['expandidos']}")
        print(f"Revisitas: {resultado['revisitas']}")
        print(f"Tempo: {resultado['tempo']:.3f} ms")
    
    print("\nLegenda:")
    print("A = início, B = destino, * = caminho")
    print(". = grama (custo 1), ~ = lama (custo 5), # = parede")

if __name__ == "__main__":
    main()
