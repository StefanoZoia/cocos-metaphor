# Questo programma filtra le righe del tsv di Tsvetkov et al
# selezionando le righe per le quali tutti gli annotatori erano concordi

import csv

IN_FILE = 'TSV_AN_English.tsv'
OUT_FILE = 'tsv_an.tsv'
header = True

with open(OUT_FILE, 'w', newline='') as outputfile:
    with open(IN_FILE, newline='') as feed:
        writer = csv.writer(outputfile, delimiter='\t', quotechar='"')
        reader = csv.reader(feed, delimiter='\t', quotechar='"')
        for row in reader:
            if header == True:
                writer.writerow(row)
                header = False
            if row[0] == '1' and row[1] == '1' and row[2] == '1' and row[3] == '1' and row[4] == '1':
                writer.writerow([row[5], row[6], row[7]])