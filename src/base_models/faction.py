from itertools import product

from ..preproc.entity_extractor import occurs_by_sentence
from ..util import find_dep_path

def get_factions(sentences, ee):
    factions = set()
    eid_sents = lambda eid: set(sent_idx for sent_idx, _, _ in ee.occurances[eid])
    obs = occurs_by_sentence(ee)

    for sent_idx, sentence in enumerate(sentences):
        for ((_, s_idx, _), s_eid), ((_, d_idx, _), d_eid) in product(obs[sent_idx], obs[sent_idx]):
            if s_idx == d_idx or s_eid == d_eid:
                continue
            if (s_eid, d_eid) in factions:
                continue
            dep_path = find_dep_path(sentence['tokens'], s_idx, d_idx)
            deps = [dep_type for (_, dep_type), _ in dep_path][1:]

            if (
                    (len(deps) == 1 and deps[0] in ['nmod', 'nmod:poss', 'amod', 'nn', 'compound']) or
                    (len(deps) < 3 and ('poss' in deps or 'appos' in deps))
            ):
                factions.add((s_eid, d_eid))
                factions.add((d_eid, s_eid))
    return factions
