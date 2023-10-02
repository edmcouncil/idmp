import argparse
import json
import re
import sys

from rdflib import Graph, Literal
from spellchecker import SpellChecker

ONTOLOGY_IRI_FILTER = 'spec.pistoiaalliance.org'
HTTP_REGEX = re.compile(pattern='http[^\s]+')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run spelling check')
    parser.add_argument('--spell', help='Path to file with new spells', metavar='SPELL')
    parser.add_argument('--ontology', help='Path to ontology file', metavar='ONTOLOGY')
    args = parser.parse_args()

    spell = SpellChecker()
    with open(file=args.spell) as new_spell_file:
        new_spell_words = json.load(new_spell_file)
    spell.word_frequency.load_words(new_spell_words)
    
    ontology = Graph()
    ontology.parse(args.ontology)
    
    bad_words_in_triples = set()
    
    for (subject, predicate, object) in ontology:
        if ONTOLOGY_IRI_FILTER in str(subject):
            if isinstance(object, Literal):
                literal = object
                literal_value = literal.value
                if isinstance(literal_value, str):
                    if literal.language is not None:
                        if literal.language != 'en':
                            continue
                    trunc_text = re.sub(pattern=HTTP_REGEX, repl='', string=literal_value)
                    words = spell.split_words(text=trunc_text)
                    for word in words:
                        word = word.replace("'s","")
                        if word == word.upper():
                            continue
                        else:
                            if word.endswith('s'):
                                if word[:-1] == word[:-1].upper():
                                    continue
                        if word[0].isnumeric():
                            continue
                        if word[0].upper() == word[0]:
                            continue
                        if word not in spell and word[:-1] not in spell and not word.lower() in spell:
                            if len(word) > 2:
                                triple = '|'.join([subject, predicate, object])
                                bad_words_in_triples.add(word + ' in triple: ' + triple)
    bad_words_in_triples = list(bad_words_in_triples)
    bad_words_in_triples.sort()
    for bad_word_in_triple in bad_words_in_triples:
        print('Possibly mispelled word', bad_word_in_triple)
    if len(bad_words_in_triples) > 0:
        sys.exit(1)
