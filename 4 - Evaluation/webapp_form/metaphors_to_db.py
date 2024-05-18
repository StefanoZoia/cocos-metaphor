import os
import csv
import json
import mysql.connector

# file containing the rows of the corpus for which a prototype has been realized
CORPUS_FILE = '../../3 - Conceptual Combination/prototyped.tsv'

# directory containing CoCoS results
COCOS_DIR = '../../3 - Conceptual Combination/cocos'

def select_metaphor(db_connection, src, tgt):
    cursor = db_connection.cursor()

    sql = f"SELECT * FROM metaphor WHERE source = '{src}' AND target = '{tgt}'"
    cursor.execute(sql)

    return cursor.fetchall()


def insert_metaphor(db_connection, src, tgt, ex, prot):
    cursor = db_connection.cursor()

    sql = f"INSERT INTO metaphor (source, target, examples, prototype) VALUES ('{src}', '{tgt}', '{ex}', '{prot}')"
    cursor.execute(sql)

    db_connection.commit()

    print(cursor.rowcount, "record inserted.")


def update_metaphor(db_connection, src, tgt, ex, prot):
    cursor = db_connection.cursor()

    sql = f"UPDATE metaphor SET examples = '{ex}', prototype = '{prot}' WHERE source = '{src}' AND target = '{tgt}'"
    cursor.execute(sql)

    db_connection.commit()

    print(cursor.rowcount, "record updated.")


def main():
    # DB connection
    db_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="survey"
    )

    # read the metaphors
    with open(cfg.CORPUS_FILE, encoding='utf-8', newline='') as corpusfile:
        reader = csv.reader(corpusfile, delimiter='\t')

        for row in reader:
            source = row[0].lower().replace(" ", "_").replace("-", "_")
            target = row[1].lower().replace(" ", "_").replace("-", "_")
            example = row[2]

            # read the combination result
            result = None
            file_path = os.path.join(cfg.COCOS_DIR, f'{target}_{source}.txt')
            with open(file_path) as f:
                input_lines = f.readlines()
                # remove comments and void lines
                input_lines = [x.strip() for x in input_lines 
                                if x.strip() != '' and x.strip()[0] != '#']
                
                for line in input_lines:
                    line = [k.strip() for k in line.split(':', maxsplit=1)]
                    if line[0] == 'Result':
                        result = json.loads(line[1])
            
            # make the prototype more human-readable
            prototype = dict()
            for k in result.keys():
                if k[0] == "@":
                    pass
                elif k[0] == "-":
                    prototype[k.replace("-", "not ", 1).replace("_", " ")] = result[k]
                else:
                    prototype[k.replace("_", " ")] = result[k]

            # if the metaphor is already present in the db
            curr_row = select_metaphor(db_conn, source, target)
            if curr_row:
                # update the row
                print(curr_row[0][1], curr_row[0][2], ":", curr_row[0][3])
                curr_examples = json.loads(curr_row[0][3])
                if example not in curr_examples:
                    curr_examples.append(example)
                update_metaphor(db_conn, source, target, json.dumps(curr_examples).replace("'", "''"), json.dumps(prototype).replace("'", "''"))
            # else insert the new metaphor
            else:
                insert_metaphor(db_conn, source, target, json.dumps([example]).replace("'", "''"), json.dumps(prototype).replace("'", "''"))




if __name__ == '__main__' : main()