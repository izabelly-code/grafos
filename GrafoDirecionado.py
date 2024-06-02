from collections import defaultdict

class GrafoDirecionado:
    def __init__(self):
        self.lista_adjacencias = defaultdict(list)
        self.num_vertices = 0
        self.num_arestas = 0


    def adiciona_vertice(self, u):
        if u not in self.lista_adjacencias:
            self.lista_adjacencias[u] = []
            self.num_vertices += 1

    def adiciona_aresta(self, u, v):
        if v not in self.lista_adjacencias:
            self.adiciona_vertice(v)
        if u not in self.lista_adjacencias:
            self.adiciona_vertice(u)
        if not any(aresta for aresta in self.lista_adjacencias[u] if aresta[0] == v):
            self.lista_adjacencias[u].append((v, 1))
            self.num_arestas += 1
                
        else:
            for to in self.lista_adjacencias[u]:
                if to[0] == v:
                    segundo_valor = to[1]
                    novo_segundo_valor = segundo_valor + 1  
                    nova_tupla = (to[0], novo_segundo_valor)
                    indice = self.lista_adjacencias[u].index(to)
                    self.lista_adjacencias[u][indice] = nova_tupla

    def print_grafo(self):
        for vertice in self.lista_adjacencias:
            print(f"Vertice {vertice}:")
            for aresta in self.lista_adjacencias[vertice]:
                print(f"  -> {aresta[0]} (Peso: {aresta[1]})")

    def kosaraju(self):
        self.visitados = {}
      #prioridade, eu preciso saber a ordem de visita dos vertices, assim o ultimo sera o primeiro
        self.pilha = []
        self.componentes_conexas = []
        for v in self.lista_adjacencias.keys():
            self.visitados[v] = False
        for v in self.lista_adjacencias.keys():
            if not self.visitados[v]:
               self.pdfs(v,self.pilha,self.visitados)

        self.lista_adjacencias = self.transpor_grafo()
        for v in self.lista_adjacencias.keys():
            self.visitados[v] = False
        while self.pilha:
            v = self.pilha.pop()
            if not self.visitados[v]:
                self.componentes_conexas.append([])
                self.dfs_rcon_comps(self.lista_adjacencias.keys(),v)
        return self.componentes_conexas
    
    def pdfs(self,v,pilha,visitados):
        visitados[v] = True
        for u in self.lista_adjacencias[v]:
            if not visitados[u]:
                self.pdfs(u,pilha,visitados)
        pilha.append(v)

    def transpor_grafo(self):
        transposto = defaultdict(list)
        for v in self.lista_adjacencias.keys():
            for u in self.lista_adjacencias[v]:
                transposto[u].append

        return transposto