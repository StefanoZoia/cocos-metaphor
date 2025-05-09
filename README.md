CoCoS system applied to Metaphors

Part of the METCL project. Please see the updated repository https://github.com/StefanoZoia/METCL

A Python tool for dynamic generation of knowledge in Description Logics of 
Typicality tested in the contexts of RaiPlay, WikiArt Emotions, and ArsMeteo
here applied to metaphor interpretation.

The tool is still under development, so no guarantee is provided on its functioning.

This work includes data from ConceptNet 5, which was compiled by the Commonsense Computing Initiative. ConceptNet 5 is freely available under the Creative Commons Attribution-ShareAlike license (CC BY SA 4.0) from https://conceptnet.io. The included data was created by contributors to Commonsense Computing projects, contributors to Wikimedia projects, Games with a Purpose, Princeton University's WordNet, DBPedia, OpenCyc, and Umbel.

------------------------------------------------------------------------------------------

# Module 1 - Dataset building

### Description

This module features different datasets containing occurrences of metaphors presented as tsv triples (target, source, sentence).
The abbreviation nn stands for noun-noun metaphor type, an for adjective-noun (the adjective being the source), na for noun-adjective (the noun being the source)

- vuamc_[nn/an].tsv contains manually extracted metaphors from the VUAMC corpus, excluding the occurrences where either the source or the target is a phrase and manually annotating the target and source.
- simple_corpus_[nn/an/na].tsv contains manually extracted metaphors from the Metaphor Detection Dataset developed by Mensa et al.
- tsv_an.tv contains adjective - noun pairs from the Tsvetkov dataset, filtering only the occurrences that every annotator indicated as metaphorical (by using the filter.py script).
- gordon_[nn/an/na].tsv contains metaphors from the "Corpus of Rich Metaphor Annotation" by Gordon et al., automatically excluding the occurrences where either the source or the target is a phrase and filtering for the different pos (by using the corpus_filter.py script).
- all_[nn/an/na].tsv contains the union of all the above metaphors, for a total of 115 an, 18 na, 534 nn metaphors

The script in remove_duplicates.py was used to remove duplicated examples if present

#### MetaNet extension

Our current work is dedicated to the conceptual metaphors in the [MetaNet Wiki](https://metaphor.icsi.berkeley.edu/pub/en/index.php/MetaNet_Metaphor_Wiki).
- metanet_classes.jsonl contains web-scraped informations about the MetaNet conceptual metaphor classes.
- metanet_frames.jsonl contains web-scraped informations about the underlying frames and theie relations with Framenet frames.
- metanet_annotations.csv contains manual annotations of the metaphorical expressions provided by MetaNet as lexicalization examples for the conceptual metaphors outlined in the wiki.
- metanet_filter.py generates the metanet_corpus.tsv file, containing the representations of the conceptual metaphors as triples, where the source and target are represented by the source and target frames (or the first subsuming frame that can be found in ConceptNet).

### Libraries 

nltk library is used for tokenization and POS tagging

------------------------------------------------------------------------------------------

# Module 2 - Prototype generation

### Description

Generation of the prototypes involved in metaphors.
1. A first step involves the retrieval of relations from ConceptNet
2. The second step builds the prototypes based on the extracted relations

### Input

The tsv representation of the metaphor corpus, represented as triples (target, source, sentence).

### Output

Prototypes of each concept involved in some metaphor

### How to run

To run the retrieval of relation from ConceptNet: python3 cn_rel_getter.py

- please, note that the execution may require some time, needed to query the ConceptNet Knowledge Base

To run the generation of prototypes of concepts: python3 prototyper.py

### Configuration

The configuration for both steps is specified in prototyper_config.py.
In particular, the configuration for prototyper.py specifies how to filter ConceptNet relations

### Libraries 

nltk is used for lemmatization

------------------------------------------------------------------------------------------

# Module 3 - Conceptual combination

### Description

Generation of the prototypes of metaphorical concepts by conceptual combination.
1. A first step preprocesses the input
2. The second step performs the conceptual combination

### Input

1. The representation of rigid and typical properties of the concepts involved in the combination.
2. The tsv representation of the metaphors

### Output

Prototypes of the combined metaphorical concepts.

### How to run

To run the generation of the input file for CoCoS: python3 cocos_preprocessing.py
- the preprocessing step writes the prototypes of each couple of concepts involved in a metaphor into a suitable file

To run the conceptual combination with CoCoS: python3 cocos.py
- This runs the combination on all the files in a specified folder.
- To run on a single file, simply call the cocos() function. The function takes the file name as the first parameter and the maximum number of properties in the resulting concept as a second (optional) parameter.

### Configuration

The configuration for both steps is specified in cocos_config.py.
In particular, the configuration specifies where to search for the input

------------------------------------------------------------------------------------------

# Module 4 - Evaluation


### Description

This module was used to conduct a human evaluation of the generated metaphorical concepts. The evaluation was conducted in 3 rounds, using different technical supports and applied to different sets of concepts:

1. the "google_form" folder contains results of the first round; we used a single Google Form survey to collect evaluations for the combined concepts representing lexicalized metaphors (from the "all-nn.tsv" file generated by Module 1).
2. the "webapp_form" folder contains results of the evaluation of combined concepts representing MetaNet's conceptual metaphors. We used a webapp to generate random samples of conceptual metaphors to evaluate.
3. the "lab_session" folder contains results fo the same evaluation of the "webapp_form", but we used 10 different Google Forms, each containing a different random sample of conceptual metaphors to evaluate.
