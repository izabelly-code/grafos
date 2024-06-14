from Grafo import Grafo

# Requisito 1: Construção do grafo
grafo = Grafo(direcionado=True, ponderado=True)

grafo.adiciona_aresta('A', 'B', 2)
grafo.adiciona_aresta('A', 'C', 3)
grafo.adiciona_aresta('B', 'C', 4)
grafo.adiciona_aresta('C', 'A', 5)
grafo.adiciona_aresta('C', 'D', 6)

grafo.imprime_lista_adjacencias()

# Requisito 2: Identificação de componentes

# Componentes fortemente conectadas usando Kosaraju
componentes_fortemente_conectadas = grafo.componentes_fortemente_conectadas_kosaraju()
print("Componentes Fortemente Conectadas (Kosaraju):", componentes_fortemente_conectadas)

# Componentes conectadas em um grafo não direcionado
grafo_nao_direcionado = Grafo(direcionado=False, ponderado=True)
grafo_nao_direcionado.adiciona_aresta('A', 'B', 2)
grafo_nao_direcionado.adiciona_aresta('A', 'C', 3)
grafo_nao_direcionado.adiciona_aresta('B', 'C', 4)
grafo_nao_direcionado.adiciona_aresta('C', 'D', 6)
componentes_conectadas = grafo_nao_direcionado.componentes_conectadas()
print("Componentes Conectadas:", componentes_conectadas)

# Requisito 3: Árvore geradora mínima (algoritmo de Prim)
mst, custo_total = grafo.arvore_geradora_minima_prim('A')
print("Árvore Geradora Mínima (Prim):")
mst.imprime_lista_adjacencias()
print("Custo Total da MST:", custo_total)

# Requisito 4: Centralidade de Grau
centralidade_grau = grafo.centralidade_grau()
print("Centralidade de Grau:", centralidade_grau)
grafo.plota_histograma_grau()
grafo.plota_top10_centralidade_grau()

# Requisito 6: Centralidade de Intermediação
centralidade_intermediacao = grafo.centralidade_intermediacao()
print("Centralidade de Intermediação:", centralidade_intermediacao)
grafo.plota_top10_centralidade_intermediacao()

# Requisito 7: Centralidade de Proximidade
centralidade_proximidade = grafo.centralidade_proximidade()
print("Centralidade de Proximidade:", centralidade_proximidade)
grafo.plota_top10_centralidade_proximidade()
