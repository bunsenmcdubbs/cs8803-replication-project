# CS 8803 Computational Social Science Replication Project

A project for CS8803-CSS at Georgia Tech by Andrew Dai and Taha Merghani
replicating
[_Document-level Sentiment Inference with Social, Faction, and Discourse Context_
by Choi, Eunsol and Rashkin, Hannah and Zettlemoyer, Luke and Choi, Yejin](https://homes.cs.washington.edu/~yejin/Papers/acl16_sfd.pdf).

`bibtex`
```
@InProceedings{Choi:2016:ACL,
  author    = {Choi, Eunsol and Rashkin, Hannah and Zettlemoyer, Luke and Choi, Yejin},
  title     = {Document-level Sentiment Inference with Social, Faction, and Discourse Context},
  booktitle = {Proceedings of the ACL},
  year      = {2016},
  publisher = {Association for Computational Linguistics}
}
```

## Tools and Datasets
 - Stanford CoreNLP
 - Scipy
 - CPLEX4 (Community edition)
 - MPQA
 - Data from authors (publically available and privately shared)

## "A Document-level Sentiment Model" (Section 2)
The paper introduces a:
> document-level ILP that includes base models and soft social constraints

**TODO**
- overall formula (social + faction + all pairwise)
- faction inference (soft constraint) (Section 2.1)
  - input: entity pairwise faction extracted with base model described in 3.2
- sentiment relations (Section 2.2)
  - input: entity pairwise sentiments extracted with base model described in 3.1
  - balance theory constraints
  - reciprocity contraints

## "Pairwise Base Models" (Section 3)

> The global model in Sec. 2 uses two base models,
> one for pairwise sentiment classification and the
> other for detecting faction relationships.

### Sentiment Classifier (section 3.1)

> The input is plain text and no gold labels are assumed; entity detection,
> dependency parse and co-reference resolution are automatic, and include
> common nouns and pronoun mentions.

It predicts sentiment between entity-pairs:
`sent(e_i→e_j)∈{positive, unbiased, negative}`.

The authors "trained separate classifiers for pairs that co-occur in a sentence
and those that do not, using a linear class-weighted SVM classifier with
crowd-sourced data...".

> define the _sentiment label_ for the text to be positive if it contains more
> words that appear in the positive sentiment lexicon than that appear in the
> negative one (and similarly for the negative label). We used the MPQA
> sentiment lexicon

#### Dependency features
- Sentiment labels for:
  - Paths containing `dobj` and `nsubj_rev`, length <= 3 if path contains
  sentiment lexicon words
  - Paths `e_i ↑ nsubj ↓ ccomp ↓ nsubj ↓ e_j` (if exists)
  - Paths without any named entity
- Indicator for `nmod:against`

#### Document features
- NER (Named Entity Recognizer) types
- Percentage of sentences with entity co-occurance
- Mentioned in the headline
- Appear only once in the document
- Add document sentiment when both entities are most frequent entities
- Rank of number of mentions of holder and target
(`e_i` and `e_j` respectively), when they never co-occur in any sentences

#### Quotation Features
- Direct quotations
  - Extracted with regular expressions.
  - Sentiment label of quote applied to (speaker, entities in quote),
  excluding entities with less than 3 occurances
  - Sentiment label also added to (speaker, most frequent entity)
- Indirect quotations
  - Connect speaker and quotation using
  "list of 20 verbs indicating speech events"
  - "Sentiment label of words connected to `e_j` via dependency path of
  length up to two that also includes the subject of the quotation verb to `e_j`"
- Indicator for whether `e_i` is the subject of the quotation verb

### Faction Detector "simple pattern-based detector"

Entity is marked as a faction if the dependency path between them
- "contains only one link of modifier or compound label (`nmod`, `nmod:poss`, `amod`, `nn`, or `compound`)"
- "contains less than three links and has a possessive or appositive label (`poss` or `appos`)"

This is an "important area for future work"
