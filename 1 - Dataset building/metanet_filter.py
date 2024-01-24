import json
import csv
import requests
import time

REQ_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
'Accept': 'application/json'}

# save locally concepts already looked for in ConceptNet to reduce API calls
conceptnet_cache = dict()

def is_in_conceptnet(concept):
    if concept is None:
        return False
    if concept not in conceptnet_cache.keys():
        #print(f"Looking for {concept} in ConceptNet...")
        query = f"https://api.conceptnet.io/c/en/{concept.strip().lower().replace(" ", "_").replace("-", "_")}"

        json = None
        limit = 10  #max n of retries
        delay = 1   #n of seconds to wait between retries
        retried = 0
        got_it = False

        # if the response is not a json or is a json with error != 404, waits and retries
        while not got_it and retried < limit:
            try:
                json = requests.get(query, REQ_HEADERS).json()
                if "error" in json.keys() and json["error"]["status"] != 404:
                    got_it = False
                    retried += 1
                    print(f'>>>>WARNING: failed attempt {retried}/{limit}')
                    time.sleep(delay)
                else:
                    got_it = True
            except:
                got_it = False
                retried += 1
                print(f'>>>>WARNING: failed attempt {retried}/{limit}')
                time.sleep(delay)
        
        if "error" in json.keys():
            conceptnet_cache[concept] = False
        else:
            conceptnet_cache[concept] = True
    
    return conceptnet_cache[concept]
    

def relation_breadth_first_exploration(rel_dict):
    # for each key
    for key in rel_dict.keys():
        # build a FIFO queue
        # add each metaphor in the main value list to the queue
        queue = list(rel_dict[key])

        # while the queue is not void
        while len(queue) > 0:
            # m = first metaphor in the queue
            # remove m from the queue
            m = queue.pop(0)

            # ignore metaphors not present in MetaNet
            if m in rel_dict.keys():
                # if m is not in the main value list, add it to the value list
                if m not in (rel_dict[key]):
                    rel_dict[key].append(m)

                # for each metaphor in the value list of m
                for other_met in rel_dict[m]:
                    # add it to the queue
                    queue.append(other_met)



def main():

    # save source and target of each metaphor in a dictionary
    metaphors_dict = dict()
    # save "source subcase of" and "target subcase of" relations in two dictionaries
    tgt_subsumers_of = dict()
    src_subsumers_of = dict()

    with open("metanet_classes.jsonl", encoding="utf-8") as scraped_data:
        for line in scraped_data:
            scraped = json.loads(line.strip())
            
            metaphor = scraped["metaphor"]
            src = scraped["source frame"]
            tgt = scraped["target frame"]

            metaphors_dict[metaphor] = {"source": src, "target": tgt}

            super_st = scraped["both s and t subcase of"]

            super_source = scraped["source subcase of"]
            src_subsumers_of[metaphor] = super_st + super_source

            super_target = scraped["target subcase of"]
            tgt_subsumers_of[metaphor] = super_st + super_target

    # extend the value lists of the subcase dictionaries with a breadth-first search of the relation
    relation_breadth_first_exploration(src_subsumers_of)
    relation_breadth_first_exploration(tgt_subsumers_of)
            
    # use the three dictionaries to build MetaNet corpus
    with open("metanet_corpus.tsv", "w", encoding='utf-8', newline="") as  tsvfile:
        output_writer = csv.writer(tsvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(["#Source", "#Target", "#ConceptualMetaphor"])

        lost_count = 0

        # for each conceptual metaphor in MetaNet
        for met in metaphors_dict.keys():
            
            source_frame = metaphors_dict[met]["source"]
            target_frame = metaphors_dict[met]["target"]

            # check for subsumer in "source subcase of" relation
            subsumers_list = list(src_subsumers_of[met])
            
            # while the source frame is not in ConceptNet and there is a subsumer
            while not is_in_conceptnet(source_frame) \
                        and len(subsumers_list) > 0:
                # retrieve subsumer
                subsumer_met = subsumers_list.pop(0)
                # replace source frame with the subsumer's source frame (if exists)
                if subsumer_met in metaphors_dict.keys():
                    source_frame = metaphors_dict[subsumer_met]["source"]

            # Note: at this point, either source_frame was found in conceptnet, or there is no subsumer to look for

            

            # check for subsumer in "target subcase of" relation
            subsumers_list = list(tgt_subsumers_of[met])
            
            # while the target frame is not in ConceptNet and there is a subsumer
            while not is_in_conceptnet(target_frame) \
                        and len(subsumers_list) > 0:
                # retrieve subsumer
                subsumer_met = subsumers_list.pop(0)
                # replace target frame with the subsumer's target frame (if exists)
                if subsumer_met in metaphors_dict.keys():
                    target_frame = metaphors_dict[subsumer_met]["target"]
                
            # Note: at this point, either target_frame was found in conceptnet, or there is no subsumer to look for
            
            # if both source and target frame are represented in ConceptNet
            if is_in_conceptnet(source_frame) and is_in_conceptnet(target_frame):
                output_writer.writerow([source_frame, target_frame, met])
            # else print a warning
            else:
                lost_count += 1
                print(f"Conceptual Metaphor {met} cannot be represented")
                if not is_in_conceptnet(source_frame):
                    print(f"\t> source frame \"{source_frame}\" not in ConceptNet")
                if not is_in_conceptnet(target_frame):
                    print(f"\t> source frame \"{target_frame}\" not in ConceptNet")
                print()

        print(lost_count, "conceptual metaphors not representable")




if __name__ == '__main__': main()



