import pandas as pd
import json
from fuzzywuzzy import fuzz


def calcular_similaridade(texto1, texto2):
    similaridade = fuzz.ratio(texto1, texto2)
    return similaridade


doc_list = []
with open('./lista_final.json', 'r', encoding='utf8') as infile:
    for linha in infile:
        documento = json.loads(linha)
        doc_list.append(documento)

my_list = pd.DataFrame(doc_list)
other_list = pd.read_excel('./Artigos_Rayyan_Aux.xlsx')

duplicados = []
unicos = []


for o_titulo in other_list['Nome']:
    if type(o_titulo) is str:
        for titulo in my_list['titulo']:
            valid = 0
            similaridade = fuzz.ratio(o_titulo.lower(), titulo.lower())
            if similaridade > 95:
                duplicados.append(o_titulo)
                break
            else:
                valid = 1

        if valid == 1:
            unicos.append(o_titulo)
