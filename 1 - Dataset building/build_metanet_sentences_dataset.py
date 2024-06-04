import csv

def main():
    # obiettivo:
    # fare un file tsv con triple (source, target, sentence) per ogni frase annotata manualmente di metanet
    input_file = 'metanet_annotation.csv'
    with open(input_file, "r", encoding='utf8') as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)
        source_index = header.index('Source')
        target_index = header.index('Target')
        sentence_index = header.index('Sentence')
        with open('metanet_sentences.tsv', 'w', encoding='utf8') as out:
            writer = csv.writer(out, delimiter='\t', lineterminator='')
            writer.writerow(['#Target', '#Source', '#Sentence'])
            for row in reader:
                if(row[source_index] and row[target_index]):
                    writer.writerow([row[target_index], row[source_index], row[sentence_index]])

if __name__ == "__main__":
    main()