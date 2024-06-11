from collections import defaultdict
import heapq
import csv
import matplotlib.pyplot as plt

class Grafo:
    # Requisito 1: construção dos grafos
    def __init__(self):
        self.lista_adjacencias = defaultdict(list)
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

    # @staticmethod
    def load_data(file_path):
        data = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data
    
    # @staticmethod
    def from_csv(file_path, directed=True):
        grafo = Grafo()
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                diretor = row['director'].strip().upper()
                elenco = [actor.strip().upper() for actor in row['cast'].split(',')]
                if diretor:
                    for ator in elenco:
                        if directed:
                            grafo.adiciona_aresta(ator, diretor)
                        else:
                            for outro_ator in elenco:
                                if ator != outro_ator:
                                    grafo.adiciona_aresta(ator, outro_ator)
        return grafo
    
    # Requisito 2: identificação de componentes
    # componentes fortemente conectadas - grafo direcionado
    def componentes_fortemente_conectadas(self):
        index = 0
        stack = []
        indices = {}
        lowlink = {}
        on_stack = defaultdict(bool)
        scc = []

        def strongconnect(v):
            nonlocal index
            indices[v] = index
            lowlink[v] = index
            index += 1
            stack.append(v)
            on_stack[v] = True

            for (w, _) in self.lista_adjacencias[v]:
                if w not in indices:
                    strongconnect(w)
                    lowlink[v] = min(lowlink[v], lowlink[w])
                elif on_stack[w]:
                    lowlink[v] = min(lowlink[v], indices[w])

            if lowlink[v] == indices[v]:
                component = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    component.append(w)
                    if w == v:
                        break
                scc.append(component)

        for v in self.lista_adjacencias:
            if v not in indices:
                strongconnect(v)

        return scc
    
    # componentes conectadas - grafo nao-direcionado
    def componentes_conectadas(self):
        visited = defaultdict(bool)
        components = []

        def dfs(v, component):
            stack = [v]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    component.append(node)
                    for (neighbour, _) in self.lista_adjacencias[node]:
                        if not visited[neighbour]:
                            stack.append(neighbour)

        for v in self.lista_adjacencias:
            if not visited[v]:
                component = []
                dfs(v, component)
                components.append(component)

        return components
    
    # Requisito 3: árvore geradora mínima
    # algoritmo de Prim  
    def arvore_geradora_minima(self, vertice):
        mst = Grafo()
        visited = set()
        edges = [(0, vertice, vertice)]

        while edges:
            weight, u, v = heapq.heappop(edges)
            if v not in visited:
                visited.add(v)
                mst.adiciona_aresta(u, v, weight)
                for (neighbour, weight) in self.lista_adjacencias[v]:
                    if neighbour not in visited:
                        heapq.heappush(edges, (weight, v, neighbour))

        return mst
    
    # Requisito 4: centralidade de grau  
    def centralidade_grau(self):
        centralidade = {v: self.grau_saida(v) for v in self.lista_adjacencias}
        return centralidade
    
    def plota_histograma_grau(self):
        centralidade = self.centralidade_grau()
        plt.figure(figsize=(10, 5))
        plt.hist(centralidade.values(), bins=10)
        plt.title('Distribuição de Graus')
        plt.xlabel('Grau')
        plt.ylabel('Frequência')
        plt.show()

    # Requisito 5: top-10 vértices com maior centralidade de grau 
    def plota_top10_centralidade_grau(self):
        centralidade = self.centralidade_grau()
        top10 = dict(sorted(centralidade.items(), key=lambda item: item[1], reverse=True)[:10])
        plt.figure(figsize=(10, 5))
        plt.bar(top10.keys(), top10.values())
        plt.title('Top-10 Vértices com Maior Centralidade de Grau')
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

        return C
    
    # Função para plotar os top-10 vértices com maior centralidade de intermediação
    def plota_top10_centralidade_intermediacao(self):
        centralidade = self.centralidade_intermediacao()
        top10 = dict(sorted(centralidade.items(), key=lambda item: item[1], reverse=True)[:10])
        plt.figure(figsize=(10, 5))
        plt.bar(top10.keys(), top10.values())
        plt.title('Top-10 Vértices com Maior Centralidade de Intermediação')
        plt.xlabel('Vértices')
        plt.ylabel('Centralidade de Intermediação')
        plt.show()

    # Requisito 7: centralidade de proximidade
    def centralidade_proximidade(self):
        def bfs_shortest_path(start):
            visited = {start: 0}
            queue = [start]
            while queue:
                node = queue.pop(0)
                for neighbour, _ in self.lista_adjacencias[node]:
                    if neighbour not in visited:
                        visited[neighbour] = visited[node] + 1
                        queue.append(neighbour)
            return visited

        closeness = {}
        for v in self.lista_adjacencias:
            shortest_paths = bfs_shortest_path(v)
            total_distance = sum(shortest_paths.values())
            if total_distance > 0 and len(self.lista_adjacencias) > 1:
                closeness[v] = (len(shortest_paths) - 1) / total_distance
            else:
                closeness[v] = 0.0

        return closeness

    # Função para plotar os top-10 vértices com maior centralidade de proximidade
    def plota_top10_centralidade_proximidade(self):
        centralidade = self.centralidade_proximidade()
        top10 = dict(sorted(centralidade.items(), key=lambda item: item[1], reverse=True)[:10])
        plt.figure(figsize=(10, 5))
        plt.bar(top10.keys(), top10.values())
        plt.title('Top-10 Vértices com Maior Centralidade de Proximidade')
        plt.xlabel('Vértices')
        plt.ylabel('Centralidade de Proximidade')
        plt.show()