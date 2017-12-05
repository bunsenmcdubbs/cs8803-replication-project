#!/usr/bin/env python
import argparse
import json
import sys

from src.preproc.annotate import annotate
from src.preproc.convert import insert_dependencies, insert_pos
from src import util

def preprocess(infile, outfile, is_parsed=False):
    if is_parsed:
        parsed, sentences, coref_chains = util.load_from_parsed(infile)
    else:
        parsed, sentences, coref_chains = util.load_from_text(infile)

    if is_parsed:
        annotate(sentences, coref_chains, parsed['named_entity'])
        insert_dependencies(sentences, parsed['totalParse'])
        insert_pos(sentences, parsed['part_of_speech'])
    else:
        annotate(sentences, coref_chains)

    parsed['sentences'] = sentences

    json.dump(parsed, args.outfile)

if __name__=='__main__':
    argparser = argparse.ArgumentParser(description='Identify, locate, and extract entities')
    argparser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    argparser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    argparser.add_argument('--parsed', action='store_true')

    args = argparser.parse_args()
    preprocess(args.infile, args.outfile, args.parsed)
