import json


with open('./Oasis.json', 'r', encoding="utf8") as infile:
    for linha in infile:
        documento = json.loads(linha)
        titulo = documento['Título'].replace(':', '_').replace('/', '_').replace(
            '.', '_').replace('|', '_').replace('?', '').replace('–', '').replace('"', '_')
        with open('./txts\\'+titulo[0:45]+'.txt', 'w', encoding='utf8') as outfile:
            outfile.write(documento['Texto'])
