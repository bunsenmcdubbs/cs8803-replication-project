from collections import defaultdict, Counter
import itertools

from .sentiment_lexicon import Sentiment
from ..preproc.entity_extractor import EntityExtractor, occurs_by_sentence

def classify(sl, sentences, ee):
    features = defaultdict(list)

    doc_slice = [token for sentence in sentences for token in sentence['tokens']]
    doc_sent = sl.get_sentiment_label(doc_slice)

    obs = occurs_by_sentence(ee)
    for sent_idx, sentence in enumerate(sentences):
        # sentence sentiment
        sent_sent, _ = sl.get_sentiment_label(sentence['tokens'])
        if sent_sent is not None:
            continue
        for ((_, s_idx, _), s_eid), ((_, d_idx, _), d_eid) in itertools.product(obs[sent_idx], obs[sent_idx]):
            if s_eid == d_eid:
                continue
            features[s_eid, d_eid] = sent_sent
    feat_counts = [(len(feats) if feats is not None else None, key) for key, feats in features.items()]

    results = {}
    # drop the bottom third of "weakest" signals
    for _, pair in feat_counts[int(len(feat_counts) / 3):]:
        counts = Counter(features[pair])
        sentiment = Sentiment.NEUTRAL
        if len(counts) == 1:
            sentiment = counts.most_common(1)[0][0]
        if len(counts) > 1:
            top1, top2 = counts.most_common(2)
            if top1[1] == top2[1]:
                sentiment = Sentiment.NEUTRAL
            else:
                sentiment = top1[0]
        results[pair] = sentiment

    return results
