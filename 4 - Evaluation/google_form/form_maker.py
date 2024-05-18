import os
import csv
import json
import random
import eval_config as cfg

def main():
    # store the list of examples for each source-target pair
    source_target = dict()

    with open(cfg.CORPUS_FILE, encoding='utf-8', newline='') as corpusfile:
        reader = csv.reader(corpusfile, delimiter='\t')

        for row in reader:
            key = f'{row[0]}_{row[1]}'.lower()
            if key not in source_target:
                # new source-target pair
                source_target[key] = [row[2]]
            else:
                if row not in source_target[key]:
                    # new example
                    source_target[key].append(row[2])

    # save the questions on a new file
    tmpfile = 'form.tsv'
    with open(tmpfile, 'w', encoding='utf-8', newline='') as tmp:
        writer = csv.writer(tmp, delimiter='\t')

        # for each source-target pair (in random order)
        random.seed(10)
        for couple in sorted(source_target, key = lambda couple : random.random()):
            source, target = couple.split('_')

            # read the combination result
            combination_result = None
            file_path = os.path.join(cfg.COCOS_DIR, f'{target}_{source}.txt')
            with open(file_path) as f:
                input_lines = f.readlines()
                # remove comments and void lines
                input_lines = [x.strip() for x in input_lines 
                                if x.strip() != '' and x.strip()[0] != '#']
                
                for line in input_lines:
                    line = [k.strip() for k in line.split(':', maxsplit=1)]
                    if line[0] == 'Result':
                        combination_result = json.loads(line[1])
    

            # build the question
            question = 'Please consider the following metaphorical sentence/s\\n'
            for example in source_target[couple]:
                question += f'\\n"{example}"'

            question += f'\\n\\nIn order to understand the metaphor, it is necessary somehow to creatively combine the meaning of the concepts \
{target.upper()} and {source.upper()}, creating a new metaphorical concept {target.upper()}-{source.upper()}.\
\\nPlease rate on a scale between 0 (worst) and 9 (best) if, overall, the features associated \
to the new metaphorical concept make sense to understand its metaphorical meaning.\\n\\n'
            
            for feature in sorted(combination_result, key = lambda feature : combination_result[feature], reverse=True):
                if feature[0] != '@':   # list all features but not the scenario probability
                    feature_value = combination_result[feature]
                    if feature[0] == '-':
                        feature = f'not {feature[1:]}'
                    question += f'{feature.replace("_", " ")}: {feature_value}\\n'

            # write the question on the output file
            writer.writerow([question])



if __name__ == '__main__' : main()