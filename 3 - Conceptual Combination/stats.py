import os
import cocos_config as cfg
import json
import csv

def main():
    n_files = 0
    n_results = 0
    classified = list()
    for filename in os.listdir(cfg.COCOS_DIR):
        file_path = os.path.join(cfg.COCOS_DIR, filename)
        with open(file_path) as f:
            input_lines = f.readlines()
            # remove comments and void lines
            input_lines = [x.strip() for x in input_lines 
                            if x.strip() != '' and x.strip()[0] != '#']
            
            n_files += 1
            file_has_result = False
            
            for line in input_lines:
                line = [k.strip() for k in line.split(':', maxsplit=1)]
                if line[0] == 'Result':
                    file_has_result = True
            
            if file_has_result:
                n_results += 1
                classified.append(filename[:-4])
    
    print(f'total combination files: {n_files}')
    print(f'total successful combinations: {n_results}')
    with open("mn_examples_classified.json", "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps(classified))


def classified_sentences():
    with open("mn_examples_classified.json", "r", encoding="utf-8") as jsonfile:
        classified_pairs = json.load(jsonfile)
        classified_sents = dict()

        with open("metanet_examples.tsv", newline='', encoding='utf-8') as corpus:
            reader = csv.reader(corpus, delimiter='\t', quotechar='"')
            for row in reader:
                source = row[0].lower().replace(" ", "_").replace("-", "_")
                target = row[1].lower().replace(" ", "_").replace("-", "_")
                sentence = row[2]
                pair_name = f"{target}_{source}"
                if pair_name in classified_pairs:
                    classified_sents[sentence] = target.upper() + " IS " + source.upper()

        with open("mn_examples_classified_dict.json", "w", encoding="utf-8") as json_file:
            json_file.write(json.dumps(classified_sents))
        print(len(classified_sents))


if __name__ == '__main__' : classified_sentences()