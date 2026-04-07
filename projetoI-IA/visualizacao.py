import matplotlib.pyplot as plt
import numpy as np


VELOCIDADE_ANIMACAO = 0.04

GRAMA_VISUAL = 0
LAMA_VISUAL = 1
PAREDE_VISUAL = 2
INICIO_VISUAL = 3
DESTINO_VISUAL = 4
EXPANDIDO_VISUAL = 5
REVISITADO_VISUAL = 6
ATUAL_VISUAL = 7
CAMINHO_VISUAL = 8


def _criar_mapa_cores():
    return plt.cm.colors.ListedColormap([
        "limegreen",   # grama
        "sienna",      # lama
        "black",       # parede
        "royalblue",   # inicio
        "red",         # destino
        "khaki",       # expandido ja visto
        "orange",      # revisitado ja visto
        "darkgoldenrod",  # passo atual
        "deepskyblue"  # caminho final
    ])


def _criar_visual_terreno(grid):
    n = len(grid)
    visual = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if grid[i][j] is None:
                visual[i][j] = PAREDE_VISUAL
            elif grid[i][j] == 5:
                visual[i][j] = LAMA_VISUAL
            else:
                visual[i][j] = GRAMA_VISUAL

    return visual


def _aplicar_inicio_destino(visual, inicio, destino):
    visual_com_pontos = visual.copy()
    visual_com_pontos[inicio[0]][inicio[1]] = INICIO_VISUAL
    visual_com_pontos[destino[0]][destino[1]] = DESTINO_VISUAL
    return visual_com_pontos


def _aplicar_caminho(visual, caminho, inicio, destino):
    visual_com_caminho = visual.copy()

    if caminho:
        for linha, coluna in caminho:
            if (linha, coluna) != inicio and (linha, coluna) != destino:
                visual_com_caminho[linha][coluna] = CAMINHO_VISUAL

    return visual_com_caminho


def _desenhar_painel(ax, visual, titulo, n):
    ax.clear()
    ax.imshow(visual, cmap=_criar_mapa_cores(), vmin=0, vmax=8)
    ax.set_title(titulo)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.grid(True)


def _montar_frame_animacao(base, inicio, destino, passos, frame):
    visual = base.copy()
    expandidos = set()
    revisitados = set()
    atual = None
    tipo_atual = ""

    for indice in range(min(frame + 1, len(passos))):
        tipo, posicao = passos[indice]
        atual = posicao
        tipo_atual = tipo

        if tipo == "expand":
            expandidos.add(posicao)
        else:
            revisitados.add(posicao)

    for linha, coluna in expandidos:
        if (linha, coluna) != inicio and (linha, coluna) != destino:
            visual[linha][coluna] = EXPANDIDO_VISUAL

    for linha, coluna in revisitados:
        if (linha, coluna) != inicio and (linha, coluna) != destino:
            visual[linha][coluna] = REVISITADO_VISUAL

    if atual and atual != inicio and atual != destino:
        visual[atual[0]][atual[1]] = ATUAL_VISUAL

    visual[inicio[0]][inicio[1]] = INICIO_VISUAL
    visual[destino[0]][destino[1]] = DESTINO_VISUAL
    return visual, len(expandidos), len(revisitados)


def _texto_legenda_animacao():
    return (
        "Legenda: verde=grama | marrom=lama | preto=parede | "
        "azul=inicio | vermelho=destino | amarelo=expandido | "
        "laranja=revisitado | dourado escuro=passo atual | azul claro=caminho final"
    )


def _animar_paineis(fig, axes, paineis, n, titulo_base):
    total_frames = max(1, max(len(painel["passos"]) for painel in paineis if painel["tipo"] == "animado"))
    plt.ion()
    plt.show(block=False)

    for frame in range(total_frames):
        for ax, painel in zip(axes, paineis):
            if painel["tipo"] == "fixo":
                visual = painel["visual"]
                expandidos = 0
                revisitados = 0
            else:
                visual, expandidos, revisitados = _montar_frame_animacao(
                    painel["base"],
                    painel["inicio"],
                    painel["destino"],
                    painel["passos"],
                    frame
                )
                painel["ultimo_expandido"] = expandidos
                painel["ultimo_revisitado"] = revisitados

            _desenhar_painel(ax, visual, painel["titulo"], n)

        resumo = []
        for painel in paineis:
            if painel["tipo"] == "animado":
                expandidos = painel.get("ultimo_expandido", 0)
                revisitados = painel.get("ultimo_revisitado", 0)
                resumo.append(f"{painel['titulo']}: E={expandidos} R={revisitados}")

        fig.suptitle(
            f"{titulo_base} - passo {frame + 1}/{total_frames}\n" + " | ".join(resumo),
            fontsize=11
        )
        fig.text(0.5, 0.02, _texto_legenda_animacao(), ha="center", fontsize=9)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()
        plt.pause(VELOCIDADE_ANIMACAO)

    plt.ioff()
    plt.close(fig)


def desenhar_um_mapa(grid, inicio, destino, caminho=None, titulo="Mapa"):
    n = len(grid)
    visual = _create_visual(grid, inicio, destino, caminho)

    fig, ax = plt.subplots(figsize=(6, 6))
    _desenhar_painel(ax, visual, titulo, n)
    plt.tight_layout()
    plt.show()


def desenhar_tres_mapas(grid, inicio, destino, caminho=None, nome_algoritmo="Busca"):
    n = len(grid)
    mapa_terreno = _criar_visual_terreno(grid)
    mapa_inicio_fim = _aplicar_inicio_destino(mapa_terreno, inicio, destino)
    mapa_resultado = _aplicar_caminho(mapa_inicio_fim, caminho, inicio, destino)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    paineis = [
        ("Mapa do Terreno", mapa_terreno),
        ("Mapa com Inicio e Fim", mapa_inicio_fim),
        (f"Caminho Final - {nome_algoritmo}", mapa_resultado)
    ]

    for ax, (titulo, visual) in zip(axes, paineis):
        _desenhar_painel(ax, visual, titulo, n)

    plt.tight_layout()
    plt.show()


def desenhar_comparacao_profundidade(grid, inicio, destino, caminho_simples=None, caminho_melhor=None):
    n = len(grid)
    mapa_terreno = _criar_visual_terreno(grid)
    mapa_inicio_fim = _aplicar_inicio_destino(mapa_terreno, inicio, destino)
    mapa_simples = _aplicar_caminho(mapa_inicio_fim, caminho_simples, inicio, destino)
    mapa_melhor = _aplicar_caminho(mapa_inicio_fim, caminho_melhor, inicio, destino)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    paineis = [
        ("Mapa do Terreno", mapa_terreno),
        ("Mapa com Inicio e Fim", mapa_inicio_fim),
        ("DFS Simples", mapa_simples),
        ("DFS com Backtracking", mapa_melhor)
    ]

    for ax, (titulo, visual) in zip(axes, paineis):
        _desenhar_painel(ax, visual, titulo, n)

    plt.tight_layout()
    plt.show()


def desenhar_comparacao_todos(
    grid,
    inicio,
    destino,
    caminho_largura=None,
    caminho_dfs_simples=None,
    caminho_dfs_melhor=None,
    caminho_gulosa=None,
    caminho_a_estrela=None
):
    n = len(grid)
    mapa_inicio_fim = _aplicar_inicio_destino(_criar_visual_terreno(grid), inicio, destino)

    paineis = [
        ("Mapa com Inicio e Fim", mapa_inicio_fim),
        ("Busca em Largura", _aplicar_caminho(mapa_inicio_fim, caminho_largura, inicio, destino)),
        ("DFS Simples", _aplicar_caminho(mapa_inicio_fim, caminho_dfs_simples, inicio, destino)),
        ("DFS com Backtracking", _aplicar_caminho(mapa_inicio_fim, caminho_dfs_melhor, inicio, destino)),
        ("Busca Gulosa", _aplicar_caminho(mapa_inicio_fim, caminho_gulosa, inicio, destino)),
        ("Busca A*", _aplicar_caminho(mapa_inicio_fim, caminho_a_estrela, inicio, destino))
    ]

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()

    for ax, (titulo, visual) in zip(axes, paineis):
        _desenhar_painel(ax, visual, titulo, n)

    plt.tight_layout()
    plt.show()


def animar_resultado_individual(grid, inicio, destino, resultado, nome_algoritmo="Busca"):
    n = len(grid)
    base = _aplicar_inicio_destino(_criar_visual_terreno(grid), inicio, destino)
    passos = resultado.get("passos_animacao", [])

    fig, ax = plt.subplots(1, 1, figsize=(7, 7))
    paineis = [
        {
            "tipo": "animado",
            "titulo": f"Percurso Percorrido - {nome_algoritmo}",
            "base": base,
            "passos": passos,
            "inicio": inicio,
            "destino": destino
        }
    ]

    _animar_paineis(fig, [ax], paineis, n, nome_algoritmo)


def animar_comparacao_profundidade(grid, inicio, destino, resultado_simples, resultado_melhor):
    n = len(grid)
    base = _aplicar_inicio_destino(_criar_visual_terreno(grid), inicio, destino)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    paineis = [
        {
            "tipo": "animado",
            "titulo": "DFS Simples",
            "base": base,
            "passos": resultado_simples.get("passos_animacao", []),
            "inicio": inicio,
            "destino": destino
        },
        {
            "tipo": "animado",
            "titulo": "DFS com Backtracking",
            "base": base,
            "passos": resultado_melhor.get("passos_animacao", []),
            "inicio": inicio,
            "destino": destino
        }
    ]

    _animar_paineis(fig, axes, paineis, n, "Comparacao da Profundidade")


def animar_comparacao_todos(
    grid,
    inicio,
    destino,
    resultado_largura,
    resultado_dfs_simples,
    resultado_dfs_melhor,
    resultado_gulosa,
    resultado_a_estrela
):
    n = len(grid)
    base = _aplicar_inicio_destino(_criar_visual_terreno(grid), inicio, destino)

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    paineis = [
        {
            "tipo": "fixo",
            "titulo": "Mapa com Inicio e Fim",
            "visual": base
        },
        {
            "tipo": "animado",
            "titulo": "Busca em Largura",
            "base": base,
            "passos": resultado_largura.get("passos_animacao", []),
            "inicio": inicio,
            "destino": destino
        },
        {
            "tipo": "animado",
            "titulo": "DFS Simples",
            "base": base,
            "passos": resultado_dfs_simples.get("passos_animacao", []),
            "inicio": inicio,
            "destino": destino
        },
        {
            "tipo": "animado",
            "titulo": "DFS com Backtracking",
            "base": base,
            "passos": resultado_dfs_melhor.get("passos_animacao", []),
            "inicio": inicio,
            "destino": destino
        },
        {
            "tipo": "animado",
            "titulo": "Busca Gulosa",
            "base": base,
            "passos": resultado_gulosa.get("passos_animacao", []),
            "inicio": inicio,
            "destino": destino
        },
        {
            "tipo": "animado",
            "titulo": "Busca A*",
            "base": base,
            "passos": resultado_a_estrela.get("passos_animacao", []),
            "inicio": inicio,
            "destino": destino
        }
    ]

    paineis[0]["passos"] = [("expand", inicio)]
    _animar_paineis(fig, axes, paineis, n, "Comparacao Geral")
