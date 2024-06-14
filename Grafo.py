from collections import defaultdict, deque
import heapq
import csv
import matplotlib.pyplot as plt

class Grafo:
    # Requisito 1: construção dos grafos
    def __init__(self, direcionado=False, ponderado=True):
        self.lista_adjacencias = defaultdict(list)
        self.direcionado = direcionado
        self.ponderado = ponderado
        self.num_vertices = 0
        self.num_arestas = 0

    def adiciona_vertice(self, u):
        if u not in self.lista_adjacencias:
            self.lista_adjacencias[u] = []
            self.num_vertices += 1

    def adiciona_aresta(self, u, v, peso=1):
        if v not in self.lista_adjacencias:
            self.adiciona_vertice(v)
        if u not in self.lista_adjacencias:
            self.adiciona_vertice(u)

        for to in self.lista_adjacencias[u]:
            if to[0] == v:
                self.lista_adjacencias[u].remove(to)
                self.lista_adjacencias[u].append((v, to[1] + 1))
                return
        self.lista_adjacencias[u].append((v, peso))
        self.num_arestas += 1

    def tem_aresta(self, u, v):
        return any(aresta for aresta in self.lista_adjacencias[u] if aresta[0] == v)

    def grau_entrada(self, u):
        return sum(1 for vertice in self.lista_adjacencias for aresta in self.lista_adjacencias[vertice] if aresta[0] == u)

    def grau_saida(self, u):
        return len(self.lista_adjacencias[u])

    def grau(self, u):
        return self.grau_entrada(u) + self.grau_saida(u)

    def get_peso(self, u, v):
        for aresta in self.lista_adjacencias[u]:
            if aresta[0] == v:
                return aresta[1]
        return None
    
    def retorna_adjacentes(self, u):
        return [aresta[0] for aresta in self.lista_adjacencias[u]]

    def imprime_lista_adjacencias(self):
        for vertice, arestas in self.lista_adjacencias.items():
            print(f'{vertice}:', ' -> '.join(f"('{aresta[0]}', {aresta[1]})" for aresta in arestas), '->')
        print(f"Ordem do grafo: {self.num_vertices}")
        print(f"Tamanho do grafo: {self.num_arestas}")

    @staticmethod
    def load_data(file_path):
        data = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data
    
    @staticmethod
    def from_csv(file_path, direcionado=True):
        grafo = Grafo(direcionado=direcionado, ponderado=True)
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                diretor = row['director'].strip().upper() if row['director'] else ''
                elenco = [actor.strip().upper() for actor in row['cast'].split(',')] if row['cast'] else []
                if direcionado:
                    if diretor:
                        for ator in elenco:
                            grafo.adiciona_aresta(ator, diretor)
                else:
                    for ator in elenco:
                        for outro_ator in elenco:
                            if ator != outro_ator:
                                grafo.adiciona_aresta(ator, outro_ator)
        return grafo
    
    def salvar_lista_adjacencias(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for vertice, arestas in self.lista_adjacencias.items():
                arestas_str = ' -> '.join(f"('{vizinho}', {peso})" for vizinho, peso in arestas)
                file.write(f'{vertice}: {arestas_str}\n')
    
    # Requisito 2: identificação de componentes
    # componentes fortemente conectadas - grafo direcionado - algoritmo de Kosaraju
    def inverte_grafo(self):
        inverso = Grafo(direcionado=self.direcionado)

        for u in self.lista_adjacencias:
            for v, peso in self.lista_adjacencias[u]:
                inverso.adiciona_aresta(v, u, peso)
        return inverso
    
    def dfs(self, v, visitado, stack=None):
        visitado[v] = True

        for i, _ in self.lista_adjacencias[v]:
            if not visitado[i]:
                self.dfs(i, visitado, stack)

        if stack is not None:
            stack.append(v)
    
    def componentes_fortemente_conectadas_kosaraju(self):
        stack = []
        visitado = defaultdict(bool)
        vertices = list(self.lista_adjacencias.keys())

        for i in vertices:
            if not visitado[i]:
                self.dfs(i, visitado, stack)
        
        inverso = self.inverte_grafo()
        
        visitado = defaultdict(bool)
        scc = []

        while stack:
            i = stack.pop()
            if not visitado[i]:
                componente = []
                inverso.dfs(i, visitado, componente)
                scc.append(componente)
        
        return scc
    
    # componentes conectadas - grafo nao-direcionado
    def bfs(self, v, visitado):
        
        componente = []
        queue = deque([v])

        while queue:
            node = queue.popleft()
            if not visitado[node]:
                visitado[node] = True
                componente.append(node)
                for vizinho, _ in self.lista_adjacencias[node]:
                    if not visitado[vizinho]:
                        queue.append(vizinho)

        return componente

    def componentes_conectadas(self):
        visitado = defaultdict(bool)
        componentes = []
        vertices = list(self.lista_adjacencias.keys())

        for v in vertices:
            if not visitado[v]:
                componente = self.bfs(v, visitado)
                componentes.append(componente)

        return componentes
    
    # Requisito 3: árvore geradora mínima
    # algoritmo de Prim  
    def arvore_geradora_minima_prim(self, vertice):
        mst = Grafo(direcionado=self.direcionado, ponderado=self.ponderado)
        visitado = set()
        arestas = [(0, vertice, vertice)]
        custo_total = 0
        
        while arestas:
            peso, u, v = heapq.heappop(arestas)
            if v not in visitado:
                visitado.add(v)
                if u != v:
                    mst.adiciona_aresta(u, v, peso)
                    custo_total += peso
                for vizinho, peso_vizinho in self.lista_adjacencias[v]:
                    if vizinho not in visitado:
                        heapq.heappush(arestas, (peso_vizinho, v, vizinho))
        
        return mst, custo_total
    
    # Requisito 4: centralidade de grau  
    def centralidade_grau(self):
        num_vertices = len(self.lista_adjacencias)
        if num_vertices <= 1:
            return {v: 0 for v in self.lista_adjacencias}
        centralidade = {v: self.grau(v) / (2 * (num_vertices - 1)) for v in self.lista_adjacencias}
        return centralidade
    
    def plota_histograma_grau(self):
        centralidade = self.centralidade_grau()
        plt.figure(figsize=(10, 5))
        plt.hist(centralidade.values(), bins=10)
        plt.title('Distribuição de Graus')
        plt.xlabel('Grau')
        plt.ylabel('Frequência')
        plt.show()

    # Requisito 5: top 10 vértices com maior centralidade de grau 
    def plota_top10_centralidade_grau(self):
        centralidade = self.centralidade_grau()
        top10 = dict(sorted(centralidade.items(), key=lambda item: item[1], reverse=True)[:10])
        plt.figure(figsize=(10, 5))
        plt.bar(top10.keys(), top10.values())
        plt.title('Top 10 Vértices com Maior Centralidade de Grau')
        plt.xlabel('Vértices')
        plt.ylabel('Centralidade de Grau')
        plt.show()

    
    # Requisito 6: centralidade de intermediação
    # algoritmo de Brandes
    def centralidade_intermediacao(self):
        C = {v: 0 for v in self.lista_adjacencias}
        for s in self.lista_adjacencias:
            S = []
            P = {w: [] for w in self.lista_adjacencias}
            sigma = dict.fromkeys(self.lista_adjacencias, 0)
            sigma[s] = 1
            d = dict.fromkeys(self.lista_adjacencias, -1)
            d[s] = 0
            Q = [s]

            while Q:
                v = Q.pop(0)
                S.append(v)
                for w, _ in self.lista_adjacencias[v]:
                    if d[w] < 0:
                        Q.append(w)
                        d[w] = d[v] + 1
                    if d[w] == d[v] + 1:
                        sigma[w] += sigma[v]
                        P[w].append(v)

            delta = dict.fromkeys(self.lista_adjacencias, 0)
            while S:
                w = S.pop()
                for v in P[w]:
                    delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
                if w != s:
                    C[w] += delta[w]
        
        # Normalização da centralidade de intermediação
        num_vertices = len(self.lista_adjacencias)
        if self.direcionado:
            normalizador = (num_vertices - 1) * (num_vertices - 2)
        else:
            normalizador = (num_vertices - 1) * (num_vertices - 2) / 2
        
        for v in C:
            C[v] /= normalizador
        
        return C

    # Função para plotar os top-10 vértices com maior centralidade de intermediação
    def plota_top10_centralidade_intermediacao(self):
        centralidade = self.centralidade_intermediacao()
        top10 = dict(sorted(centralidade.items(), key=lambda item: item[1], reverse=True)[:10])
        plt.figure(figsize=(10, 5))
        plt.bar(top10.keys(), top10.values())
        plt.title('Top 10 Vértices com Maior Centralidade de Intermediação')
        plt.xlabel('Vértices')
        plt.ylabel('Centralidade de Intermediação')
        plt.show()

    # Requisito 7: centralidade de proximidade
    def centralidade_proximidade(self):
        def bfs_caminho_mais_curto(inicio):
            visitados = {inicio: 0}
            fila = [inicio]
            while fila:
                node = fila.pop(0)
                for vizinho, _ in self.lista_adjacencias[node]:
                    if vizinho not in visitados:
                        visitados[vizinho] = visitados[node] + 1
                        fila.append(vizinho)
            return visitados

        proximidade = {}
        num_vertices = len(self.lista_adjacencias)

        for v in self.lista_adjacencias:
            
            caminhos_mais_curtos = bfs_caminho_mais_curto(v)

            distancia_total = sum(caminhos_mais_curtos.values())
            if distancia_total > 0:
                proximidade[v] = (num_vertices - 1) / distancia_total
            else:
                proximidade[v] = 0.0

        return proximidade


    # Função para plotar os top-10 vértices com maior centralidade de proximidade
    def plota_top10_centralidade_proximidade(self):
        centralidade = self.centralidade_proximidade()
        top10 = dict(sorted(centralidade.items(), key=lambda item: item[1], reverse=True)[:10])
        plt.figure(figsize=(10, 5))
        plt.bar(top10.keys(), top10.values())
        plt.title('Top 10 vértices com maior centralidade de proximidade')
        plt.xlabel('Vértices')
        plt.ylabel('Centralidade de proximidade')
        plt.show()
