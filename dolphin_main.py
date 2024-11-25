#######################################################################################################
#
#  Informações e instruções para o Projeto 1:
#
# O projeto consiste em escrever um programa em (python, C ou C++) que lê o arquivo 
# (soc-dolphins.mtx, ou o txt), monta com esses dados um grafo não direcionado, sem pesos, 
# usando listas de adjacências, e então calcula e imprime como saída (tela) o seguinte:
#
# 1) o vértice, e seu respectivo grau (para todos os vértices);
# 2) todos os cliques maximais (indicando o número de vértices e quais);
# 3) O Coeficiente de Aglomeração de cada vértice;
# 4) O Coeficiente médio de Aglomeração do Grafo.
# 5) Gera uma visualização do grafo completo, colocando cores diferentes em todos os cliques
# maximais
#
########################################################################################################

import networkx as nx
import matplotlib.pyplot as plt
import random


def ConstroiListaEncadeada(arquivo):

    # A lista Encadeada será um dicionario que armazenará os vértices
    listaAdjacencia = {}

    # Leitura do txt desconsiderando a primeira linha que contém a quantidade de vértices e de adjacencias
    with open(arquivo, 'r') as arquivo:
        arquivo = arquivo.readlines()
        
        for linha in arquivo[1:]:

            vertice1, vertice2 = map(int, linha.split())
            
            # Inseriremos cada vértice da linha de forma separada, porque o grafo é não direcionado
            if vertice1 not in listaAdjacencia:
                listaAdjacencia[vertice1] = []
            listaAdjacencia[vertice1].append(vertice2)
            
            if vertice2 not in listaAdjacencia:
                listaAdjacencia[vertice2] = []
            listaAdjacencia[vertice2].append(vertice1)
    
        # Print da lista de adjacencias
        print(f"\nLista de Adjacencias do Grafo dos golfinhos:")
        for vertice, adjacencia in listaAdjacencia.items():
            print(f"{vertice}: {adjacencia}")

            
    return(listaAdjacencia)

# -----------------------------------------------------------------------------------------------------------

# Função responsável por printar todos os vértices do grafo e seus respectvos graus
def PrintGrauVertices(listaEncadeada):

    print(f"\nPrint dos vértices e seus respectivos graus")
    
    for i in sorted(listaEncadeada, key = listaEncadeada.get):
        print(f"Vértice: {i} -> Grau: {len(listaEncadeada[i])}")

    return

# -----------------------------------------------------------------------------------------------------------

# ====================================================================================================================
# Para encontrar os cliques, implementaremos um algoritmo de Bron Kerbosch, que é basicamente um
# algoritmo de enumeração para encontrar todos os cliques maximais em um grafo não direcionado.
# Seu código base consiste em três conjuntos: 
#  - Conjunto R: vértices que seriam parte do clique (ps. inicia vazio).
#  - Conjunto P: vértices que têm ligação com todos os vértices de R (candidatos).
#  - Conjunto X: vértices já analisados e que não levam a uma extensão do conjunto R. 
#    Usado para evitar comparação excessiva (ps. inicia vazio).
#
# Referência: Bron, Coen; Kerbosch, Joep (1973), "Algorithm 457: finding all cliques  of  an  undirected  graph",  
# Commun.  ACM,  ACM,  16 (9):575–577, doi:10.1145/362342.362367.
# ======================================================================================================================

# Função responsável por encontrar todos os cliques maximais do grafo
def BronKerbosch(R, P, X, listaAdjacencia, cliques):
 
    if not P and not X:
        # Se P e X estão vazios, um clique maximal foi encontrado
        cliques.append(R)
        return

    for v in list(P):
        # Para cada vértice v escolhido, faz-se uma chamada recursiva adicionando v em R.
        BronKerbosch(
            # Usa as funções união e insterseção nativas
            R.union({v}),
            P.intersection(listaAdjacencia[v]),
            X.intersection(listaAdjacencia[v]),
            listaAdjacencia,
            cliques
        )
        
        # Quando todas as extensões de R que contém v forem analisadas, v é movido de P para X.
        P.remove(v)
        X.add(v)


def Cliques(listaAdjacencia):

    # Foi escolhido sets, porque irei utilizar união (.union) e interseção (.intersection) exclusivos de sets
    R = set() 
    P = set(listaAdjacencia.keys())  
    X = set()  
    cliques = [] 

    # Executa o algoritmo de Bron Kerbosch
    BronKerbosch(R, P, X, listaAdjacencia, cliques)

    # Print dos cliques maximais
    print("\nCliques Maximais:")
    for clique in cliques:
        print(f"{len(clique)} vértices: {sorted(clique)}")

    return cliques

# -----------------------------------------------------------------------------------------------------------
# Função para encontrar os coeficientes de aglomeração:
# Existia dois meios para encontrar o coeficiente de aglomeração: 
# - Usando a fórmula do coeficiente de aglomeração:  2ti / ni (ni - 1) e implementar o código na mão
# - Usar uma biblioteca que já tenha implementada o coeficiente
# 
# Por ser mais simples, optei por implementar a biblioteca já pronta

def CoeficienteAglomeracao(listaEncadeada):
    # Cria um grafo usando a biblioteca networkx e a de lista de adjacencias, e usa a função da networkx para encontrar os coeficientes
    Grafo = nx.Graph(listaEncadeada)
    coeficienteAglomeracao = nx.clustering(Grafo)
    
    print("\nCoeficiente de Aglomeração de cada vértice:")
    for vertice, coeficiente in coeficienteAglomeracao.items():
        print(f"Vértice {vertice}: Coeficiente de Aglomeração = {coeficiente}")
    
    # Retorna o coeficiente de aglomeração para todos os vértices
    return coeficienteAglomeracao

#------------------------------------------------------------------------------------------------------------
# Função para encontrar o coeficiente médio de aglomeração do grafo
def CoeficienteMédioAglomeração(coeficienteAglomeracao):
    
    # Média simples 
    soma = sum(coeficienteAglomeracao.values())
    quantidadeVertices = len(coeficienteAglomeracao)
    media = soma / quantidadeVertices
    print(f"\nCoeficiente médio de Aglomeração do Grafo é: {media}")
    
    return ()

#------------------------------------------------------------------------------------------------------------

# Para a plotagem do grafo foi necessário o uso de três biblioteca: Matplotlib para plotar o grafico,
# a NetworkX para criar e manipular grafos (nesse caso usado para criar um grafo considerando a lista de
# adjcencias) e desenhar o grafo na Matplot e a biblioteca Random, para gerar cores aleatórias para os vértice.
# Para a criação desse algoritmo, me baseei no algoritmo do The igraph development team, que pode ser conferido:
# https://python.igraph.org/en/latest/tutorials/visualize_cliques.html, alem da documentação das duas bibliotecas:
# https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.clique.find_cliques.html
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
#


# Função para gerar a visualização do grafo com cliques e arestas coloridas
def visualizacaoGrafo(listaEncadeada, cliques):
    
    # Cria o grafo a partir da lista de adjacência. Criei um dicionário para mapear as cores
    grafo = nx.Graph(listaEncadeada)
    cores = {}
    
    # Gera uma cor aleatória para cada clique. A cor está em RGB
    for clique in cliques:
        cor = (random.random(), random.random(), random.random())
        for vertice in clique:
            cores[vertice] = cor

    # Lista de cores para os vértices do grafo
    coresVertices = [cores.get(i, (1, 1, 1)) for i in grafo.nodes()] 

    # Desenha o grafo com o matplotlib
    plt.figure(figsize=(8, 5))
    coordenadas = nx.spring_layout(grafo)
    
    # Parametros necessários para plotar o grafo
    nx.draw(
            grafo, 
            coordenadas, 
            with_labels = True,
            node_size = 500,
            node_color = coresVertices,
            font_size = 10,
            font_weight = 'bold', # Fonte em negrito
            edge_color = 'black'
            )

    # Plota o grafo
    plt.show()
    return ()

# -----------------------------------------------------------------------------------------------------------
# Função principal: leitura do arquivo txt e chamada das respectivas funções
def main():
    arquivo = 'soc-dolphins.txt'
    
    # Chama função para construir a lista encadeada de vértices 
    listaEncadeada = ConstroiListaEncadeada(arquivo)

    # Função para printar os vértices e seus respectivos graus
    PrintGrauVertices(listaEncadeada)

    # Função para idintificar todos os cliques maximais e printá-los
    cliques = Cliques(listaEncadeada) 

    # Função para identificar o coeficiente de aglomeração de cada um dos vértices
    coeficienteAglomeracao = CoeficienteAglomeracao(listaEncadeada)

    # Função para identificar o coeficiente médio de aglomeração do grafo
    CoeficienteMédioAglomeração(coeficienteAglomeracao)
    
    # Função para visualização dos vertices e adjacencias do grafo e seus respectivos cliques maximais
    visualizacaoGrafo(listaEncadeada, cliques)


if __name__ == "__main__":
    main()
