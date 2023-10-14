# Questo programma filtra le righe del csv di Gordon et al
# selezionando le metafore NN (oppure AN)

import csv
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

IN_FILE = 'metaphor-corpus.csv'
OUT_FILE = 'gordon_na.tsv'
header = True

SENTENCE = 0
TARGET_LM = 6
SOURCE_LM = 8


with open(OUT_FILE, 'w', newline='', encoding='utf-8') as outputfile:
    with open(IN_FILE, newline='', encoding='utf-8') as feed:
        writer = csv.writer(outputfile, delimiter='\t', quotechar='"')
        reader = csv.reader(feed, delimiter=',', quotechar='"')
        for row in reader:
            if header == True:
                #writer.writerow(row)
                header = False
            else:
                tok_sentence = word_tokenize(row[SENTENCE])

                # filtering out phraseological sources and targets
                if row[SOURCE_LM] in tok_sentence and row[TARGET_LM] in tok_sentence:
                    source_index = tok_sentence.index(row[SOURCE_LM])
                    target_index = tok_sentence.index(row[TARGET_LM])

                    # pos tag row[SENTENCE]
                    pos = pos_tag(tok_sentence, tagset='universal')
                    
                    # if source and target are of the specified pos
                    if pos[source_index][1] == 'NOUN' and pos[target_index][1] == 'ADJ':
                        # write the filtered row
                        writer.writerow([row[SOURCE_LM], row[TARGET_LM], row[SENTENCE]])
