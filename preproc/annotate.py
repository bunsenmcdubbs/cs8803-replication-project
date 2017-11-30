def mark_entities(sentences, ee):
    for eid, occurances in ee.occurances.items():
        for sent_idx, start_idx, end_idx in occurances:
            for token_idx in range(start_idx, end_idx):
                sentences[sent_idx]['tokens'][token_idx]['entity_id'] = eid

def mark_coref_mentions(sentences, all_chains):
    chains = []
    for chain in all_chains:
        entity_ids = set()
        for mention in chain:
            for token in sentences[mention['sentNum'] - 1]['tokens'][mention['startIndex'] - 1:mention['endIndex'] - 1]:
                if 'entity_id' in token:
                    entity_ids.add(token['entity_id'])
        if len(entity_ids) == 1:
            chains.append((list(entity_ids)[0], chain))

    for entity_id, chain in chains:
        for mention in chain:
            for token in sentences[mention['sentNum'] - 1]['tokens'][mention['startIndex'] - 1:mention['endIndex'] - 1]:
                token['entity_id'] = entity_id
