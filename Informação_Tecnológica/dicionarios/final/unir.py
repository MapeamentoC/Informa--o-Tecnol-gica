import glob
import json
import nltk
import ftfy
import fasttext


def reonhece_lingua(sentenca):
    model = fasttext.load_model('./lid.176.ftz')
    result = model.predict(sentenca, k=1)
    if result[0][0] == '__label__pt':
        validador = True
    else:
        validador = False

    return validador


nltk.download('punkt')


def tokenize_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return sentences


with open('./saida\\Oasis.json', 'w', encoding='utf8') as outfile:
    for item in glob.glob('./*.json'):
        print(item)
        print('\n')
        with open(item, 'r', encoding='utf8') as infile:
            json_data = [json.loads(linha) for linha in infile]
            for linha in json_data:
                if linha['Texto'] != '':
             
                    texto = linha['Texto']
                    texto = ftfy.ftfy(texto)
                    texto = tokenize_sentences(texto)
                    out_text = ''
                    for sent in texto:
                        if len(sent) > 30:
                            out_text += sent+'\n'
                    dikt = {'Título': linha['Título'], 'Texto': out_text}
                    json.dump(dikt, outfile)
                    outfile.write('\n')
