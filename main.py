import csv
import sys
from GrafoDirecionado import GrafoDirecionado;
from GrafoNaoDirecionado import GrafoNaoDirecionado;


sys.setrecursionlimit(20000)

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


grafoDirecionado = GrafoDirecionado()
grafoNaoDirecionado = GrafoNaoDirecionado()
file_path = "netflix_amazon_disney_titles.csv"

def contrucao_grafo_direcionado(linha):
    if linha[3] != "" and linha[4] != "":
        #deixando em maisculo e removendo espaços
        diretor=linha[3].upper().strip()
        cast=linha[4].split(",")
        for ator in list(cast):
            removido=ator
            ator=ator.upper().strip()
            grafoDirecionado.adiciona_aresta(diretor, ator)           
            ator=ator.upper().strip()
            for ator2 in cast:               
                ator2=ator2.upper().strip()
                if ator != ator2:                                 
                    grafoNaoDirecionado.adiciona_aresta(ator, ator2)
            #para não repetir pares iguais e assim dar erro no peso dos vertices
            cast.remove(removido)  

            
   
try:
    with open(file_path, 'r', encoding='utf-8',errors='ignore') as f:
        reader = csv.reader(f)
        next(reader)
        # CONSTRUÇÃO DO GRAFO DIRECIONADO ENTRE DIRETOR E ATORES
        for linha in reader:
            contrucao_grafo_direcionado(linha)            
  
    print("Questão 1: Construção do Grafo Direcionado e Não Direcionado")
    print("Grafo Direcionado construído com sucesso")
    print(f"Arestas:  {grafoDirecionado.num_arestas}")
    print(f"Vertices: {grafoDirecionado.num_vertices}")
    #grafoDirecionado.print_grafo()
    print("Grafo Não Direcionado construído com sucesso")
    print(f"Arestas:  {grafoNaoDirecionado.num_arestas}")
    print(f"Vertices: {grafoNaoDirecionado.num_vertices}") 
    print("Questão 2: Componentes Conexas")
    quantidade_componentes = grafoNaoDirecionado.calcula_componentes_conexas()
    print(f"Componentes Conexas do Grafo Não Direcionado {quantidade_componentes}")
    #grafoNaoDirecionado.print_grafo()
               
except Exception as e:
    print(f"An error occurred: {e}")