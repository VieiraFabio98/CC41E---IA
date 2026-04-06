from utils import criar_mapa, imprimir_mapa, dentro, pode_andar
from visualizacao import desenhar_tres_mapas, desenhar_comparacao_profundidade
from algoritmos.largura import busca_largura
from algoritmos.profundidade import busca_profundidade
from algoritmos.gulosa import busca_gulosa
from algoritmos.a_estrela import busca_a_estrela


def ler_posicao(nome, n):
    texto = input(f"{nome} (linha,coluna) de 0 a {n-1}: ").strip()

    try:
        l, c = map(int, texto.split(","))
        return (l, c)
    except ValueError:
        return None


def escolher_algoritmo():
    print("=== MENU DE BUSCAS ===")
    print("1 - Busca em Largura")
    print("2 - Busca em Profundidade")
    print("3 - Busca Gulosa")
    print("4 - Busca A*")
    return input("Escolha uma opcao: ").strip()


def mostrar_resultado(nome, resultado):
    garantias = {
        "menor_numero_de_passos": "garante o menor numero de passos, mas nao o menor custo",
        "primeiro_caminho_encontrado": "mostra o primeiro caminho encontrado pela DFS simples",
        "melhor_custo_por_backtracking": "busca o melhor custo usando backtracking",
        "nao_garante_melhor_caminho": "usa heuristica, mas nao garante o melhor caminho",
        "melhor_caminho_com_heuristica": "usa custo + heuristica para buscar o melhor caminho"
    }

    print(f"\n=== Resultado: {nome} ===")

    if resultado["found"]:
        print("Caminho encontrado:")
        print(resultado["path"])
        print("Custo total:", resultado["cost"])
    else:
        print("Nenhum caminho encontrado.")

    print("Nos expandidos:", resultado["expanded"])

    if "revisitas" in resultado:
        print("Revisitas:", resultado["revisitas"])

    if "guarantee" in resultado:
        garantia = garantias.get(resultado["guarantee"], resultado["guarantee"])
        print("Garantia teorica:", garantia)

    print(f"Tempo (ms): {resultado['time_ms']:.3f}")


def main():
    opcao = escolher_algoritmo()
    print()

    try:
        n = int(input("Tamanho do mapa n x n: "))
        if n < 2:
            print("Valor muito pequeno, ajustando para 2.")
            n = 2
    except ValueError:
        print("Valor invalido, usando 10.")
        n = 10

    try:
        paredes = int(input("Quantidade de paredes: "))
        if paredes < 0:
            print("Quantidade invalida, usando 0.")
            paredes = 0
    except ValueError:
        print("Valor invalido, usando 0 paredes.")
        paredes = 0

    grid = criar_mapa(n, paredes)

    print()
    print("Deseja informar inicio e destino manualmente?")
    print("1 - Sim")
    print("2 - Nao (usar inicio=(0,0) e destino=(n-1,n-1))")
    escolha_pos = input("Opcao: ").strip()

    if escolha_pos == "1":
        inicio = ler_posicao("Inicio", n)
        destino = ler_posicao("Destino", n)

        if inicio is None or destino is None:
            print("Coordenadas invalidas.")
            return
    else:
        inicio = (0, 0)
        destino = (n - 1, n - 1)

    if not dentro(grid, inicio) or not dentro(grid, destino):
        print("Inicio ou destino fora do mapa.")
        return

    if not pode_andar(grid, inicio):
        print("O inicio caiu em uma parede.")
        return

    if not pode_andar(grid, destino):
        print("O destino caiu em uma parede.")
        return

    print("\nMapa inicial:")
    imprimir_mapa(grid, inicio, destino)

    if opcao == "1":
        nome = "Busca em Largura"
        resultado = busca_largura(grid, inicio, destino)
        mostrar_resultado(nome, resultado)

        if resultado["found"]:
            print("\nMapa com caminho:")
            imprimir_mapa(grid, inicio, destino, resultado["path"])
            desenhar_tres_mapas(grid, inicio, destino, resultado["path"], nome_algoritmo=nome)
        else:
            desenhar_tres_mapas(grid, inicio, destino, None, nome_algoritmo=nome)

    elif opcao == "2":
        resultados = busca_profundidade(grid, inicio, destino)
        simples = resultados["simples"]
        melhor = resultados["melhor"]

        mostrar_resultado("Busca em Profundidade - DFS Simples", simples)
        if simples["found"]:
            print("\nMapa DFS Simples:")
            imprimir_mapa(grid, inicio, destino, simples["path"])

        mostrar_resultado("Busca em Profundidade - DFS com Backtracking", melhor)
        if melhor["found"]:
            print("\nMapa DFS com Backtracking:")
            imprimir_mapa(grid, inicio, destino, melhor["path"])

        desenhar_comparacao_profundidade(
            grid,
            inicio,
            destino,
            simples["path"] if simples["found"] else None,
            melhor["path"] if melhor["found"] else None
        )

    elif opcao == "3":
        nome = "Busca Gulosa"
        resultado = busca_gulosa(grid, inicio, destino)
        mostrar_resultado(nome, resultado)

        if resultado["found"]:
            print("\nMapa com caminho:")
            imprimir_mapa(grid, inicio, destino, resultado["path"])
            desenhar_tres_mapas(grid, inicio, destino, resultado["path"], nome_algoritmo=nome)
        else:
            desenhar_tres_mapas(grid, inicio, destino, None, nome_algoritmo=nome)

    elif opcao == "4":
        nome = "Busca A*"
        resultado = busca_a_estrela(grid, inicio, destino)
        mostrar_resultado(nome, resultado)

        if resultado["found"]:
            print("\nMapa com caminho:")
            imprimir_mapa(grid, inicio, destino, resultado["path"])
            desenhar_tres_mapas(grid, inicio, destino, resultado["path"], nome_algoritmo=nome)
        else:
            desenhar_tres_mapas(grid, inicio, destino, None, nome_algoritmo=nome)

    else:
        print("Opcao invalida.")


if __name__ == "__main__":
    main()
