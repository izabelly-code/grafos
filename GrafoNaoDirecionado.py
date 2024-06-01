from collections import defaultdict

class GrafoNaoDirecionado:
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
            self.lista_adjacencias[v].append((u, 1))
            self.num_arestas += 1
                
        else:
            for to in self.lista_adjacencias[u]:                
                if to[0] == v:
                    segundo_valor = to[1]
                    novo_segundo_valor = segundo_valor + 1  
                    nova_tupla = (to[0], novo_segundo_valor)
                    indice = self.lista_adjacencias[u].index(to)
                    self.lista_adjacencias[u][indice] = nova_tupla

            for to in self.lista_adjacencias[v]:
                if to[0] == u:
                    peso = to[1]
                    novo_peso =peso + 1  
                    vertice_peso_atualizado = (to[0], novo_peso)
                    indice = self.lista_adjacencias[v].index(to)
                    self.lista_adjacencias[v][indice] = vertice_peso_atualizado
                    
    def print_grafo(self):
        for vertice in self.lista_adjacencias:
            print(f"Vertice {vertice}:")
            for aresta in self.lista_adjacencias[vertice]:
                print(f"  -> {aresta[0]} (Peso: {aresta[1]})")