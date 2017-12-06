from collections import defaultdict
import itertools

from ..preproc.entity_extractor import EntityExtractor, occurs_by_sentence
from ..util import DepDirection, dep_path_to_token_slice, find_dep_path

def feat_sentiment_dobj_nsubjrev(sl, sentence, dep_path):
    if len(dep_path) > 3:
        return None
    deps = [dep for dep, _ in dep_path]
    if (DepDirection.DEP, 'dobj') not in deps or (DepDirection.GOV, 'nsubj') not in deps:
        return None
    return sl.get_sentiment_label(dep_path_to_token_slice(sentence, dep_path))[0]

def feat_sentiment_nsubj_ccomp_nsubj(sl, sentence, dep_path):
    target = [
        (DepDirection.GOV, 'nsubj'),
        (DepDirection.DEP, 'ccomp'),
        (DepDirection.DEP, 'nsubj')
    ]
    deps = [dep for dep, _ in dep_path if dep in target]
    if len(deps) < 3:
        return None
    if not all([dep in deps for dep in target]):
        return None
    start_idx = deps.index(target[0]) # first occurance of target[0]
    end_idx = len(deps) - list(reversed(deps)).index(target[2]) # last occurance of target[2]
    if target[1] not in deps[start_idx:end_idx]: # is target[1] between target[0] and target[2]
        return None
    return sl.get_sentiment_label(dep_path_to_token_slice(sentence, dep_path))[0]

def feat_sentiment_no_named_entity(sl, sentence, dep_path):
    t_slice = dep_path_to_token_slice(sentence, dep_path)[1:-1] # exclude first and last tokens
    num_entity_mentions = sum(1 for token in t_slice if 'entity_id' in token)
    if num_entity_mentions != 0:
        return None
    return sl.get_sentiment_label(t_slice)[0]

def feat_indicator_nmod_against(sl, sentence, dep_path):
    deps = [dep_type for (_, dep_type), _ in dep_path]
    return 'nmod:against' in deps

feat_map = {
    'sentiment_dobj_nsubjrev': feat_sentiment_dobj_nsubjrev,
    'sentiment_nsubj_ccomp_nsubj': feat_sentiment_nsubj_ccomp_nsubj,
    'sentiment_no_named_entity': feat_sentiment_no_named_entity,
    'indicator_nmod_against': feat_indicator_nmod_against
}

def dep_path_features(sl, sentence, dep_path):
    return [
        (key, feat_val)
        for key, feat_val in (
            (key, feat_func(sl, sentence, dep_path))
            for key, feat_func in feat_map.items())
        if feat_val
    ]

def dependency_features(sl, sentences, ee):
    features = defaultdict(list)
    obs = occurs_by_sentence(ee)
    for sent_idx, sentence in enumerate(sentences):
        for ((_, s_idx, _), s_eid), ((_, d_idx, _), d_eid) in itertools.product(obs[sent_idx], obs[sent_idx]):
            if s_idx == d_idx or s_eid == d_eid:
                continue
            dep_path = find_dep_path(sentence['tokens'], s_idx, d_idx)
            # TODO bug?
            # if dep_path is None:
            #     print(len(sentence['tokens']), sent_idx, sentence['tokens'][s_idx], sentence['tokens'][d_idx])
            # assert dep_path is not None, 'dependency path was not found!'
            if dep_path is None:
                dep_path = find_dep_path(sentence['tokens'], d_idx, s_idx)
                if dep_path is not None:
                    dep_path = [
                        (
                            (
                                DepDirection.DEP if dep_dir == DepDirection.GOV else DepDirection.GOV,
                                dep_type
                            ),
                            dep_idx
                        ) for (dep_dir, dep_type), dep_idx in dep_path
                    ]
            if dep_path is None:
                continue
            features[s_eid, d_eid].extend(dep_path_features(sl, sentence['tokens'], dep_path))
    return features

def document_features(sl, sentences, ee):
    num_occur = lambda eid: len(ee.occurances[eid])

    most_common2 = set([eid for eid, _ in ee.most_common(2)])
    doc_slice = (token for sentence in sentences for token in sentence['tokens'])
    doc_sent, _ = sl.get_sentiment_label(doc_slice)

    eid_by_num_occurs = sorted(ee.occurances.keys(),
                               key=num_occur,
                               reverse=True)
    eid_sents = lambda eid: set(sent_idx for sent_idx, _, _ in ee.occurances[eid])
    occur_rank = lambda eid: eid_by_num_occurs.index(eid)

    all_doc_features = dict()
    for eid1, eid2 in itertools.product(ee.occurances.keys(), ee.occurances.keys()):
        # TODO add headline feature

        if eid1 == eid2:
            continue
        features = dict()
        if num_occur(eid1) == 1 and num_occur(eid2) == 1:
            features['indicator_occurs_once'] = True

        if set([eid1, eid2]) == most_common2:
            features['sentiment_most_common_doc_sentiment'] = doc_sent

        if len(eid_sents(eid1) & eid_sents(eid2)) == 0:
            features['rank_no_cooccur_holder'] = occur_rank(eid1)
            features['rank_no_cooccur_target'] = occur_rank(eid2)

        all_doc_features[eid1, eid2] = list(features.items())
    return all_doc_features

def get_features(sl, sentences, ee):
    features = defaultdict(list)

    for pair, feats in dependency_features(sl, sentences, ee).items():
        features[pair].extend(feats)

    for pair, feats in document_features(sl, sentences, ee).items():
        features[pair].extend(feats)

    return features
