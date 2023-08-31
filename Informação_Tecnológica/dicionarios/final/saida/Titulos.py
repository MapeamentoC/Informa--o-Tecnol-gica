import json
with open('./titulos.txt', 'w', encoding='utf8') as outfile:
    with open('./oasis.json', 'r', encoding='utf8') as infile:
        for linha in infile:
            documento = json.loads(linha)
            print(type(documento))
            outfile.write(documento['Título'])
            outfile.write('\n')
