import random

def imprimir_tabuleiro(tab):
    print("\n")
    print(f" {tab[0]} | {tab[1]} | {tab[2]} ")
    print("---+---+---")
    print(f" {tab[3]} | {tab[4]} | {tab[5]} ")
    print("---+---+---")
    print(f" {tab[6]} | {tab[7]} | {tab[8]} ")
    print("\n")

def vencedor(tab, simbolo):
    linhas = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    return any(tab[a] == tab[b] == tab[c] == simbolo for a, b, c in linhas)

def empate(tab):
    return all(c in ("X", "O") for c in tab)

def posicao_valida(tab, pos):
    return 1 <= pos <= 9 and tab[pos - 1] not in ("X", "O")

def jogada_jogador(tab):
    while True:
        try:
            pos = int(input("Sua vez! Escolha uma posição (1-9): "))
            if posicao_valida(tab, pos):
                return pos - 1
            else:
                print("Posição inválida ou ocupada.")
        except ValueError:
            print("Digite um número válido.")

def jogada_computador(tab, dificuldade):
    if dificuldade == "fácil":
        return random.choice([i for i, v in enumerate(tab) if v not in ("X", "O")])
    elif dificuldade == "médio":
        # Tenta vencer ou bloquear
        for simbolo in ["O", "X"]:
            for i in range(9):
                if tab[i] not in ("X", "O"):
                    original = tab[i]
                    tab[i] = simbolo
                    if vencedor(tab, simbolo):
                        tab[i] = original
                        return i
                    tab[i] = original
        return random.choice([i for i, v in enumerate(tab) if v not in ("X", "O")])
    else:  # difícil
        return minimax(tab, "O")

def minimax(tab, jogador):
    if vencedor(tab, "O"):
        return 1
    elif vencedor(tab, "X"):
        return -1
    elif empate(tab):
        return 0

    simbolo = "O" if jogador == "O" else "X"
    melhor_valor = -float("inf") if jogador == "O" else float("inf")
    melhor_jogada = None

    for i in range(9):
        if tab[i] not in ("X", "O"):
            original = tab[i]
            tab[i] = jogador
            valor = minimax(tab, "X" if jogador == "O" else "O")
            tab[i] = original

            if jogador == "O":
                if valor > melhor_valor:
                    melhor_valor = valor
                    melhor_jogada = i
            else:
                if valor < melhor_valor:
                    melhor_valor = valor
                    melhor_jogada = i

    return melhor_jogada if melhor_jogada is not None else 0

def jogar(placar, dificuldade):
    tabuleiro = [str(i) for i in range(1, 10)]
    print(f"Você é X, o Python é O. Dificuldade: {dificuldade.capitalize()}")
    imprimir_tabuleiro(tabuleiro)

    while True:
        idx = jogada_jogador(tabuleiro)
        tabuleiro[idx] = "X"
        imprimir_tabuleiro(tabuleiro)
        if vencedor(tabuleiro, "X"):
            print("Parabéns, você venceu! 🎉")
            placar["Você"] += 1
            break
        if empate(tabuleiro):
            print("Empate! 🤝")
            placar["Empates"] += 1
            break

        print("Vez do Python...")
        idx = jogada_computador(tabuleiro, dificuldade)
        tabuleiro[idx] = "O"
        imprimir_tabuleiro(tabuleiro)
        if vencedor(tabuleiro, "O"):
            print("Python venceu! 🤖")
            placar["Python"] += 1
            break
        if empate(tabuleiro):
            print("Empate! 🤝")
            placar["Empates"] += 1
            break

def mostrar_placar(placar):
    print("\n📊 Placar:")
    print(f"Você: {placar['Você']} | Python: {placar['Python']} | Empates: {placar['Empates']}\n")

if __name__ == "__main__":
    placar = {"Você": 0, "Python": 0, "Empates": 0}

    while True:
        dificuldade = input("Escolha a dificuldade (fácil, médio, difícil): ").strip().lower()
        if dificuldade not in ("fácil", "medio", "médio", "difícil", "dificil"):
            print("Dificuldade inválida. Tente novamente.")
            continue
        if dificuldade == "medio":
            dificuldade = "médio"
        elif dificuldade == "dificil":
            dificuldade = "difícil"

        jogar(placar, dificuldade)
        mostrar_placar(placar)
        resp = input("Quer jogar novamente? (S/N): ").strip().lower()
        if resp not in ("s", "sim"):
            print("Obrigado por jogar! 👋")
            break
