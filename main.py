import numpy as np
import random
import time, sys
import os
import psutil


def get_process_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def abrir_arquivo(arquivo, modo_abertura):
    return open(arquivo, modo_abertura)


def lista(arq):
    arq = abrir_arquivo(arq, 'r')
    memoryStart = get_process_memory()
    arq.seek(0)
    FirstLine = arq.readline().rstrip()
    FirstLine = FirstLine.split()
    Vertices = int(FirstLine[0])
    Arestas = int(FirstLine[1])

    Lista = [[] for x in range(Vertices)]

    for i in range(0, Arestas):
        Aresta = arq.readline()
        Aresta = Aresta.split(" ")
        x = int(Aresta[0])
        y = int(Aresta[1])
        z = float(Aresta[2])
        Lista[x].append((y, z))
        Lista[y].append((x, z))

    memoryEnd = get_process_memory()
    Memoria = (memoryEnd - memoryStart) / (1024 * 1024)
    print(Memoria, "MB")
    return Lista


def matriz(arq):
    arq = abrir_arquivo(arq, 'r')
    #memoryStart = get_process_memory()
    arq.seek(0)
    FirstLine = arq.readline().rstrip()
    FirstLine = FirstLine.split()
    Vertices = int(FirstLine[0])
    Arestas = int(FirstLine[1])
    Matriz = [[0 for _ in range(Vertices)] for _ in range(Vertices)]

    for i in range(0, Arestas):
        Aresta = arq.readline()
        Aresta = Aresta.split(" ")
        x = int(Aresta[0])
        y = int(Aresta[1])
        z = float(Aresta[2])
        Matriz[x][y] = z
        Matriz[y][x] = z

    #memoryEnd = get_process_memory()
    #Memoria = (memoryEnd - memoryStart) / (1024 * 1024)
    #print(Memoria, "MB")
    print()
    return Matriz


# cria o grafo completo
def grafo_completo(V, wMin, wMax):
    G = [[0 for i in range(V)] for i in range(V)]
    i = 0
    A = (V * (V - 1))
    A = A / 2
    # 'A' recebe o numero de arestas que o grafo possui
    while i < A:
        # sorteando vertices
        u = random.randint(0, V - 1)
        v = random.randint(0, V - 1)
        # sorteando pesos
        w = random.randint(wMin, wMax)
        if u != v and G[u][v] == 0:
            # atribuindo peso nas arestas
            G[u][v] = w
            G[v][u] = w
            i += 1
    return G  #retorna grafo em matriz


# converte de matriz para lista
def converter(a):
    ListaAdj = []
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] != 0:
                w = a[i][j]
                ListaAdj.append(
                    (i, j,
                     w))  # cria uma lista com os dados dos vertices e peso
    return ListaAdj


# imprime matriz
def imprime_matriz(matriz):
    print("~ MATRIZ ~")
    for i in range(len(matriz)):
        print(matriz[i])


# encontrar o peso entre dois vertices
def peso_aresta(u, v, listaAdj):
    for x, y, w in listaAdj:
        if u == x and v == y:
            return w
    print("Erro! Peso não definido.")


# algoritmo vizinho mais próximo
def vizinhoMaisProximo(grafo):
    #print(grafo)
    vertice = 0  # vértice atual
    caminho = []
    restantes = []
    listaAdj = converter(grafo)
    origem = 0  # vértice caso precise alterar a origem
    custo = 0

    inicio = time.time()
    # cria lista de restantes
    for i in range(len(grafo)):
        restantes.append(i)

    # remove a origem dos restantes
    del (restantes[0])

    # laço principal
    while restantes:
        menor = None
        #for u, v, w in grafo:
        for u, v, w in listaAdj:

            if u == vertice and v in restantes:  # analisa os vertices adj do vertice que estão em restantes
                if menor == None:  # menor recebe o primeiro adj para analisar o resto
                    menor = v
                    peso = w
                elif peso > w:
                    menor = v
                    peso = w

        caminho.append(vertice)
        custo = custo + peso
        # trocando o vértice analisado para o menor
        vertice = menor
        # removendo o vertice dos restantes
        restantes.remove(vertice)

    caminho.append(vertice)

    custo += grafo[caminho[-1]][caminho[0]]
    custo = round(custo, 2)
    caminho.append(origem)
    fim = time.time()
    tempo = (fim - inicio)
    tempo = round(tempo, 4)
    print("Rota: ", caminho)
    print("Custo: ", custo)
    print("Tempo: ", tempo, "s")

    return custo, caminho, tempo

# https://stackoverflow.com/questions/53275314/2-opt-algorithm-to-solve-the-travelling-salesman-problem-in-python
# algoritmo que retorna o custo da rota
def cost(custo_matriz, rota):
    return custo_matriz[np.roll(rota, 1), rota].sum()

# algoritmo de troca das arestas
def two_opt(rota, matriz):
    melhor = rota
    melhorada = True
    while melhorada:
        melhorada = False
        for i in range(1, len(rota) - 2):
            for j in range(i + 1, len(rota)):
                if j - i == 1: continue  # não muda nada, então passa
                nova_rota = rota[:]
                nova_rota[i:j] = rota[j - 1:i -
                                      1:-1]  # é aqui onde ocorre a troca
                matriz = np.array(matriz)
                nova_r = np.array(nova_rota)
                melhor_r = np.array(melhor)
                custo_nova = cost(matriz, nova_r)
                custo_melhor = cost(matriz, melhor_r)
                if custo_nova < custo_melhor:  # compara os custos das rotas
                    melhor = nova_rota
                    melhorada = True
                    custo_nova = cost(matriz, nova_r)
                    custo_melhor = cost(matriz, melhor_r)

        custo_final = custo_melhor
        custo_final = round(custo_final, 2)
        rota = melhor

    #fim = time.time()
    #tempo = (fim-inicio)
    #print("Tempo: %.5fs" %tempo)

    return melhor, custo_final


# função para limpar tela
def screen_clear():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


# função do menu
def menu():
    print(" ")
    print("Escolha uma opção:")
    #time.sleep(1)
    print("1 - Vizinho mais próximo (guloso)")
    #time.sleep(1)
    #print("2 - Força bruta")
    #time.sleep(1)
    print("2 - Sair")
    opcao = int(input('> '))
    screen_clear()
    return opcao


def entradas():
    v = int(input('Digite o numero de vertices: '))
    wMin = int(input('Digite o peso mínimo: '))
    wMax = int(input('Digite o peso máximo: '))
    print()
    return v, wMin, wMax


# menu
opcao = 0
print("~~~~ GRAFO MASTER ~~~~")
while opcao != 2:
    opcao = menu()
    if opcao == 1:
        #v, min, max = entradas()
        print("~~~~ VIZINHO MAIS PRÓXIMO ~~~~\n")
        print("Escolha um arquivo texto ou crie seu grafo:")
        print("1 - a280.txt")
        print("2 - ali535.txt")
        print("3 - ch130.txt")
        print("4 - fl1577.txt")
        print("5 - gr666.txt")
        print("6 - teste.txt")
        print("7 - criar grafo")
        opcao = int(input('> '))
        screen_clear()

        def default():
            print("Value default")

        def switch(opcao):
            if opcao == 1:
                print("~~~~ a280 ~~~~")
                grafo = matriz('a280.txt')
                return grafo
            elif opcao == 2:
                print("~~~~ ali535 ~~~~")
                grafo = matriz('ali535.txt')
                return grafo
            elif opcao == 3:
                print("~~~~ ch130 ~~~~")
                grafo = matriz('ch130.txt')
                return grafo
            elif opcao == 4:
                print("~~~~ fl1577 ~~~~")
                grafo = matriz('fl1577.txt')
                return grafo
            elif opcao == 5:
                print("~~~~ gr666 ~~~~")
                grafo = matriz('gr666.txt')
                return grafo
            elif opcao == 6:
                print("~~~~ teste ~~~~")
                grafo = matriz('teste.txt')
                return grafo
            elif opcao == 7:
                print("~~~~ criando seu grafo ~~~~\n")
                v, min, max = entradas()
                grafo = grafo_completo(v, min, max)
                return grafo
            else:
                return default()

        print("Obtendo rota", end="")
        for i in range(0, 3):
            sys.stdout.write(".")
            time.sleep(1)
            sys.stdout.flush()

        screen_clear()
        grafo = switch(opcao)

        custo, caminho, tempo_original = vizinhoMaisProximo(grafo)

        print()
        print("Deseja tentar otimizar a rota? (2-opt)")
        print("1 - Sim")
        print("2 - Não")
        opcao_2 = int(input('> '))
        screen_clear()
        if (opcao_2 == 1):
            print("~~~~ OTIMIZADO ~~~~ \n")
            #TO DO TEMPO
            inicio = time.time()
            tempo_2 = time.time()
            tempo_usuario = 60
            tempo_final = tempo_2 + tempo_usuario
            caminho_otimizado, custo_otimizado = two_opt(caminho, grafo)
            fim = time.time()
            tempo = (fim - inicio)
            if (tempo_2 > tempo_final):
                if (custo_otimizado < custo):
                    print("Rota original: ", caminho)
                    print("Custo original: ", custo)
                    print("Tempo original: ", tempo_original, "s")
                    print("\nRota otimizada: ", caminho_otimizado)
                    print("Custo otimizado: ", custo_otimizado)
                    tempo = (fim - inicio)
                    print("Tempo da otimização: %.4f" % tempo, "s")
                    string_custo = str(custo_otimizado)
                    string_caminho = str(caminho_otimizado)

                    arquivo = open('saida.txt', 'w')
                    arquivo.write(string_custo)
                    arquivo.write(string_caminho)
                    arquivo.close
                    print()
                    print(tempo_final)
                    print(tempo_2)
                    print("\nArquivo salvado!")
                else:
                    print("Tempo excedido!")
            else:
                print("Não existe otimização para essa rota!")
        elif (opcao_2 == 2):
            print("Saindo...")
        #matriz = imprime_matriz(grafo)

#    elif opcao == 2:
#        v, min, max = entradas()
#        print(" ")
#        print("FORÇA BRUTA")
#        inicio = time.time()
#        grafo = grafo_completo(v, min, max)
#        forca_bruta(grafo)
#        fim = time.time()
#        tempo = (fim - inicio)
#        matriz = imprime_matriz(grafo)
#        print("Tempo: %.3f" %tempo)

    elif opcao == 2:
        print("Finalizando", end="")

        for i in range(0, 3):
            sys.stdout.write(".")
            time.sleep(1)
            sys.stdout.flush()

    else:
        print("Digite uma opção válida.")
    print()
    print('~ ' * 10)
