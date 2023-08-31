import glob

tokens = 0

for file in glob.glob('./*.txt'):
    with open(file, 'r', encoding='utf8') as infile:
        for linha in infile:
            tokens += len(linha.split(' '))

print(tokens)
