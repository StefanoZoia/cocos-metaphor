import json
import csv


def main():
    with open("metanet_classes.jsonl", encoding="utf-8") as scraped_data:
        with open("metanet_corpus.tsv", "w", encoding='utf-8', newline="") as  tsvfile:
            output_writer = csv.writer(tsvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            output_writer.writerow(["#ConceptualMetaphor", "#Source", "#Target"])

            # for each conceptual metaphor in MetaNet
            for line in scraped_data:
                scraped = json.loads(line.strip())
                
                metaphor = scraped["metaphor"]
                source_frame = scraped["source frame"]
                target_frame = scraped["target frame"]

                # check for subsumer in "source subcase of" relation
                # while the source frame is not in ConceptNet and there is a subsumer
                    # replace source frame with subsumer
                    # check for subsumer

                # check for subsumer in "target subcase of" relation
                # while the target frame is not in ConceptNet and there is a subsumer
                    # replace target frame with subsumer
                    # check for subsumer
                
                # if both source and target frame are represented in ConceptNet
                output_writer.writerow([metaphor, source_frame, target_frame])
                # else print a warning




if __name__ == '__main__': main()



