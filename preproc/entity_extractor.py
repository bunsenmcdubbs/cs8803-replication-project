from collections import Counter

import util
import wikidata

PERSON_TYPE = 'PERSON'
LOCATION_TYPE = 'LOCATION'
ORGANIZATION_TYPE = 'ORGANIZATION'
MISC_TYPE = 'MISC'
NAMED_TYPES = set([PERSON_TYPE, LOCATION_TYPE, ORGANIZATION_TYPE, MISC_TYPE])

class EntityExtractor:
    # TODO add option to turn off wikidata merging
    def __init__(self):
        self._entity_to_id = {} # many entity to one id
        self._occurances = {} # one id to many occurances
        self._next_id = 0

    @property
    def ids(self):
        return self._entity_to_id.items()

    @property
    def occurances(self):
        return self._occurances

    def create_entity(self, entity):
        assert entity not in self._entity_to_id
        _, text = entity

        wikidata_id = wikidata.get_id(text)
        if wikidata_id:
            entity_id = ('wikidata', wikidata_id)
        else:
            entity_id = ('manual', self._next_id)
            self._next_id += 1
        self._entity_to_id[entity] = entity_id

        if entity_id not in self._occurances:
            self._occurances[entity_id] = set()

    def add_occurance(self, entity, sent_idx, start_idx, end_idx):
        self.add_occurances(entity, {(sent_idx, start_idx, end_idx)})

    def add_occurances(self, entity, occurs_iter):
        if entity not in self._entity_to_id:
            self.create_entity(entity)
        self._occurances[self._entity_to_id[entity]].update(set(occurs_iter))

    def merge_entities(self, eid_dest, eid_additional):
        self._occurances[eid_dest] |= self._occurances[eid_additional]

        keys_to_change = [entity_key for entity_key, eid in self.ids if eid == eid_additional]
        for key in keys_to_change:
            self._entity_to_id[key] = eid_dest
            del self.occurances[eid_additional]

    @staticmethod
    def from_sentences(sentences):
        ee = EntityExtractor()
        for sentence in sentences:
            start_idx = curr_type = None
            for token in sentence['tokens']:
                if token['ner'] != curr_type and curr_type is not None:
                    end_idx = token['index'] - 1
                    raw_text = util.get_text(sentence['tokens'][start_idx:end_idx])
                    ee.add_occurance((curr_type, raw_text), sentence['index'], start_idx, end_idx)
                    start_idx = curr_type = None
                if token['ner'] in NAMED_TYPES and curr_type is None:
                    start_idx = token['index'] - 1
                    curr_type = token['ner']
            if curr_type is not None:
                end_idx = token['index']
                raw_text = util.get_text(sentence['tokens'][start_idx:end_idx])
                ee.add_occurance((curr_type, raw_text), sentence['index'], start_idx, end_idx)
        return ee

    @staticmethod
    def from_parsed_data(entity_occurances):
        """
        For use with parsed named entity data provided by authors
        """
        ee = EntityExtractor()
        for entity, occurances in entity_occurances.items():
            for sent_idx, e_type, start_idx, end_idx in occurances:
                if e_type in NAMED_TYPES:
                    ee.add_occurance((e_type, entity), sent_idx - 1, start_idx - 1, end_idx) # convert to index from 0 and exclusive end
        return ee

def merge_people_by_last_name(ee):
    people = list(filter(lambda pair: pair[0][0] == PERSON_TYPE, ee.ids))
    people.sort(key=lambda pair: (pair[0][1].split(' ')[-1], len(pair[0][1])))
    potential_merges = set()
    curr_last_name = None
    curr_last_name_eid = None

    for (_, name), eid in people:
        if len(name.split(' ')) == 1:
            curr_last_name = name
            curr_last_name_eid = eid
        elif curr_last_name is not None:
            if curr_last_name == name.split(' ')[-1]:
                potential_merges.add((curr_last_name_eid, eid))

    count = Counter(eid for pair in potential_merges for eid in pair)
    merges = [pair for pair in potential_merges if count[pair[0]] == 1 and count[pair[1]] == 1]

    for eid_dest, eid_additional in merges:
        ee.merge_entities(eid_dest, eid_additional)
