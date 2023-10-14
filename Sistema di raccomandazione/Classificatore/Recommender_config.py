# Config file for DEGARI's recommender module
# Here are specified the features of a dataset in order to generate its recommendations


# configuration for WikiArt dataset

# name of json description file for input
jsonDescrFile = "descr_wikiart.json"

# artwork identifier attribute in json description file, corresponding to a prototype file name in protPath
instanceID = "ID"

# instance title attributes in json description file
# the first attribute is the artwork instance's title, followed by other main features
instanceTitle = ["Title"]

# list of instance description attributes in json description file
instanceDescr = ["Description"]

# prototypes folder path
protPath = "wikiart_for_cocos/"


"""
# configuration for ArsMeteo dataset

# name of json description file for input
jsonDescrFile = "descr_arsmeteo.json"

# artwork identifier attribute in json description file, corresponding to a prototype file name in protPath
instanceID = "titolo"

# instance title attributes in json description file
# the first attribute is the artwork instance's title, followed by other main features
instanceTitle = ["titolo"]

# list of instance description attributes in json description file
instanceDescr = ["descrizione", "testo", "titolo"]

# prototypes folder path
protPath = "arsmeteo_for_cocos/"
"""

"""
# configuration for SPICE dataset

# name of json description file for input
jsonDescrFile = "descr_spice.json"

# artwork identifier attribute in json description file, corresponding to a prototype file name in protPath
instanceID = "opera"

# instance title attributes in json description file
# the first attribute is the artwork instance's title, followed by other main features
instanceTitle = ["titolo"]

# list of instance description attributes in json description file
instanceDescr = ["evento", "storia", "titolo", "sensazione"]

# prototypes folder path
protPath = "spice_for_cocos/"
"""

"""
# configuration for RaiPlay dataset

# name of json description file for input
jsonDescrFile = "descr_raiplay.json"

# artwork identifier attribute in json description file, corresponding to a prototype file name in protPath
instanceID = "programma"

# instance title attributes in json description file
# the first attribute is the artwork instance's title (used to identify it), followed by other main features
instanceTitle = ["name", "descrProgramma"]

# list of instance description attributes in json description file
instanceDescr = ["description", "name", "descrProgramma", "programma"]

# prototypes folder path
protPath = "raiplay_for_cocos/"
"""