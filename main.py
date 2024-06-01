import csv
import sys
from GrafoDirecionado import GrafoDirecionado;

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


grafoDirecionado = GrafoDirecionado()
file_path = "netflix_amazon_disney_titles.csv"
try:
    with open(file_path, 'r', encoding='utf-8',errors='ignore') as f:
        reader = csv.reader(f)
        next(reader)
        for linha in reader:
            # CONSTRUÇÃO DO GRAFO DIRECIONADO ENTRE DIRETOR E ATORES
            if linha[3] != "" and linha[4] != "":
                diretor=linha[3]
                cast=linha[4].split(",")
                for ator in cast:
                    grafoDirecionado.adiciona_aresta(diretor, ator)

except Exception as e:
    print(f"An error occurred: {e}")