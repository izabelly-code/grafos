from Grafo import Grafo

if __name__ == "__main__":
    
    file_path = "netflix_amazon_disney_titles.csv"

    # Criar grafos direcionado e não-direcionado
    grafo_direcionado = Grafo.from_csv(file_path, directed=True)
    grafo_nao_direcionado = Grafo.from_csv(file_path, directed=False)

    # Analisar componentes
    # componentes_direcionado = grafo_direcionado.componentes_fortemente_conectadas()
    # componentes_nao_direcionado = grafo_nao_direcionado.componentes_conectadas()

    # Calcular centralidades
    # centralidade_grau_direcionado = grafo_direcionado.centralidade_grau()
    centralidade_intermediacao_direcionado = grafo_direcionado.centralidade_intermediacao()
    # centralidade_proximidade_direcionado = grafo_direcionado.centralidade_proximidade()

    # print(centralidade_grau_direcionado)
    # print(centralidade_intermediacao_direcionado)
    # print(centralidade_proximidade_direcionado)

    # centralidade_grau_nao_direcionado = grafo_nao_direcionado.centralidade_grau()
    # centralidade_intermediacao_nao_direcionado = grafo_nao_direcionado.centralidade_intermediacao()
    # centralidade_proximidade_nao_direcionado = grafo_nao_direcionado.centralidade_proximidade()

    # # Exibir resultados
    # grafo_direcionado.imprime_lista_adjacencias()
    # grafo_nao_direcionado.imprime_lista_adjacencias()

    # # Plotar gráficos
    # grafo_direcionado.plota_histograma_grau()
    # grafo_direcionado.plota_top10_centralidade_grau()
    # grafo_direcionado.plota_top10_centralidade_intermediacao()
    # grafo_direcionado.plota_top10_centralidade_proximidade()

    # grafo_nao_direcionado.plota_histograma_grau()
    grafo_nao_direcionado.plota_top10_centralidade_grau()
    # grafo_nao_direcionado.plota_top10_centralidade_intermediacao()
    # grafo_nao_direcionado.plota_top10_centralidade_proximidade()