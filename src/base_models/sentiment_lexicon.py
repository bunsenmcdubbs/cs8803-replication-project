from collections import Counter
from enum import Enum

import pygtrie

class POS(Enum):
    ANY_POS = 'anypos'
    ADJ = 'adj'
    ADVERB = 'adverb'
    NOUN = 'noun'
    VERB = 'verb'

class Sentiment(Enum):
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    NEUTRAL = 'neutral'

    def is_valid(text):
        return text in set([Sentiment.POSITIVE.value, Sentiment.NEGATIVE.value])

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class SentimentLexicon:
    def __init__(self):
        self.trie = pygtrie.CharTrie()

    def add_entry(self, text, pos, is_stem, sentiment):
        if text not in self.trie:
            self.trie[text] = dict()
        assert (pos, is_stem) not in self.trie[text], '{} already exists'.format((text, pos, is_stem))
        self.trie[text][pos, is_stem] = sentiment

    def get_sentiment(self, text, pos):
        if self.trie.has_key(text):
            if (pos, False) in self.trie[text]:
                return self.trie[text][pos, False]
            elif (pos, True) in self.trie[text]:
                return self.trie[text][pos, True]
        else:
            for _, entries in reversed(list(self.trie.prefixes(text))):
                if (pos, True) in entries:
                    return entries[pos, True]
        return None

    def get_sentiment_label(self, tokens):
        s_count = Counter()
        no_match = 0
        for token in tokens:
            pos = _ptb2ezpos(token['pos'])
            token_sentiment = self.get_sentiment(token['originalText'], pos) or \
                              self.get_sentiment(token['lemma'], pos) if 'lemma' in token else None
            if token_sentiment is not None:
                s_count[token_sentiment] += 1
            else:
                no_match += 1

        sentiment = None
        if len(s_count) == 1:
            sentiment = s_count.most_common()[0][0]
        elif len(s_count) > 1:
            top2 = s_count.most_common(2)
            if top2[0][1] == top2[1][1]:
                sentiment = Sentiment.NEUTRAL

        if no_match > 0:
            s_count[None] = no_match

        return sentiment, s_count

    @staticmethod
    def from_mpqa_file(filename):
        sentiment_count = Counter()
        pos_count = Counter()
        sl = SentimentLexicon()
        with open(filename, 'r') as f:
            for raw_entry in f:
                try:
                    entry = dict((pair.split('=')) for pair in raw_entry.strip().split(' '))
                except ValueError as e:
                    continue
                if Sentiment.is_valid(entry['priorpolarity']):
                    try:
                        sl.add_entry(
                            entry['word1'],
                            POS(entry['pos1']),
                            entry['stemmed1']=='y',
                            Sentiment(entry['priorpolarity']))
                    except AssertionError as e:
                        continue
                    sentiment_count[Sentiment(entry['priorpolarity'])] += 1
                    pos_count[POS(entry['pos1'])] += 1
        return sl, sentiment_count, pos_count

def _ptb2ezpos(ptb_tag):
    tag = ptb_tag.lower()[:1]
    if tag == 'nn': # NN, NNS, NNP, NNPS
        return POS.NOUN
    elif tag == 'vb': # VB, VBD, VBG, VBN, VBP, VBZ
        return POS.VERB
    elif tag == 'rb': # RB, RBR, RBS
        return POS.ADVERB
    elif tag == 'jj': # JJ, JJR, JJS
        return POS.ADJ
    return POS.ANY_POS
