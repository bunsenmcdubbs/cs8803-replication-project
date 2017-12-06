import requests

WIKIDATA_API_URL = 'https://wikidata.org/w/api.php'

_search_entity_action = lambda term: {
    'action': 'wbsearchentities',
    'language': 'en',
    'strictlanguage': True,
    'type': 'item',
    'limit': 1, # We'll only be using the first result
    'format': 'json',
    'search': term
}

_get_entity_action = lambda eid: {
    'action': 'wbgetentities',
    'languages': 'en',
    'props': 'labels|descriptions|aliases',
    'format': 'json',
    'ids': eid if isinstance(eid, str) else '|'.join(eid)
}

_search_cache = {} # keyed by search term, value is json response
_get_cache = {} # keyed by id, value is json response

search_cache_misses = 0
search_cache_hits = 0

def search(term):
    global search_cache_misses, search_cache_hits
    if term is None or len(term) == 0:
        raise ValueError()
    if term not in _search_cache:
        search_cache_misses += 1
        r = requests.get(WIKIDATA_API_URL, params=_search_entity_action(term))
        try:
            _search_cache[term] = r.json()['search'][0]
        except IndexError:
            _search_cache[term] = None
    else:
        search_cache_hits += 1
    return _search_cache[term]

# TODO support multiple entity_id retrievals
def get(entity_id):
    if entity_id is None or len(entity_id) == 0:
        raise ValueError()
    if entity_id not in _get_cache:
        r = requests.get(WIKIDATA_API_URL, params=_get_entity_action(entity_id))
        try:
            _get_cache[entity_id] = list(r.json()['entities'].values())[0]
        except Error:
            _get_cache[entity_id] = None
    return _get_cache[entity_id]

def get_id(term):
    try:
        return search(term)['id']
    except (KeyError, TypeError):
        pass
    return None

def clear_search_cache():
    global search_cache_misses, search_cache_hits
    _search_cache = {}
    search_cache_misses = 0
    search_cache_hits = 0

def clear_entity_cache():
    _get_cache = {}

def clear_cache():
    clear_search_cache()
    clear_entity_cache()
