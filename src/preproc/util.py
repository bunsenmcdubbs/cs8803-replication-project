import json

from pycorenlp import StanfordCoreNLP

def get_text(tokens):
    raw_text = []
    for token in tokens:
        raw_text.append(token['originalText'])
        raw_text.append(token['after'])
    return ''.join(raw_text[:-1])

sentences_from_parsed = lambda sentences: [
    {
        'index': s_idx,
        'tokens': [
            {
                'index': t_idx + 1, # index starting at 1
                'originalText': token
            } for t_idx, token in enumerate(sentence)
        ]
    } for s_idx, sentence in enumerate(sentences)
]

chains_from_parsed = lambda chains: [
    [
        {
            'sentNum': m['sent_ind'],
            'startIndex': m['token_ind'],
            'endIndex': m['end_ind']
        } for m in chain
    ] for chain in chains
]

def load_from_parsed(f):
    parsed_data = json.load(f)
    sentences = sentences_from_parsed(parsed_data['text'])
    corefs = chains_from_parsed(parsed_data['cluster_json'])
    return parsed_data, sentences, corefs

def load_from_text(f):
    raw_text = f.read()
    nlp = StanfordCoreNLP('http://localhost:9000')
    output = nlp.annotate(raw_text, properties={
        'annotators': 'ner,coref',
        'outputFormat': 'json'
    })
    sentences = output['sentences']
    corefs = output['corefs'].values()
    return output, sentences, corefs
