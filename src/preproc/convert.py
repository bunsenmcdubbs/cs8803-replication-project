"""
Functions to convert data format provided by authors into standard format
based on StanfordCoreNLP API JSON format
"""

def insert_pos(sentences, pos):
    for sent_idx in range(len(sentences)):
        for token_idx in range(len(sentences[sent_idx]['tokens'])):
            sentences[sent_idx]['tokens'][token_idx]['pos'] = pos[sent_idx][token_idx]

def insert_dependencies(sentences, depparse):
    for sent_idx, sentence in enumerate(sentences):
        sentence['enhancedPlusPlusDependencies'] = [
            {
                'governor': governor,
                'dependent': dependent,
                'dep': dep_type
            } for governor, dependent, dep_type in depparse[str(sent_idx + 1)]
        ]
