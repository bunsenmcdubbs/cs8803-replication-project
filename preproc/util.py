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
