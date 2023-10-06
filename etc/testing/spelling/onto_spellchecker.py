import argparse
import json
import logging
import re
import sys

from rdflib import Graph, Literal, URIRef
from spellchecker import SpellChecker

HTTP_REGEX = re.compile(pattern='http[^\s]+')
LOCAL_NAME_SEPARATOR = '/'


def __get_local_name_from_iri(iri: URIRef) -> str:
    local_name = str(iri).split(sep=LOCAL_NAME_SEPARATOR)[-1]
    return local_name


def check_spelling_in_ontology(new_spell_file_path: str, ontology_location: str, resource_filter: str):
    spell = SpellChecker()
    with open(file=new_spell_file_path) as new_spell_file:
        new_spell_words = json.load(new_spell_file)
    spell.word_frequency.load_words(new_spell_words)
    
    ontology = Graph()
    ontology.parse(ontology_location)
    
    local_names_in_ontology = set()
    for (subject, predicate, object) in ontology:
        if isinstance(subject, URIRef):
            local_names_in_ontology.add(__get_local_name_from_iri(iri=subject))
        if isinstance(predicate, URIRef):
            local_names_in_ontology.add(__get_local_name_from_iri(iri=predicate))
        if isinstance(object, URIRef):
            local_names_in_ontology.add(__get_local_name_from_iri(iri=object))
    spell.word_frequency.load_words(local_names_in_ontology)
    
    misspelled_words_in_triples = set()
    misspelled_words = set()
    for (subject, predicate, object) in ontology:
        if resource_filter in str(subject):
            if isinstance(object, Literal):
                literal = object
                literal_value = literal.value
                if isinstance(literal_value, str):
                    if literal.language is not None:
                        if literal.language != 'en':
                            continue
                    trunc_text = re.sub(pattern=HTTP_REGEX, repl='', string=literal_value)
                    trunc_text = re.sub(pattern=r'[a-z\-]+:[^\s]+', repl='', string=trunc_text)
                    words = spell.split_words(text=trunc_text)
                    for word in words:
                        word = word.replace("'s", "")
                        if word == word.upper():
                            continue
                        else:
                            if word.endswith('s'):
                                if word[:-1] == word[:-1].upper():
                                    continue
                        if any(char.isdigit() for char in word):
                            continue
                        if word[0].upper() == word[0]:
                            continue
                        if word not in spell and word[:-1] not in spell and not word.lower() in spell:
                            if len(word) > 2:
                                triple = '|'.join([subject, predicate, object])
                                misspelled_words_in_triples.add('|'.join([word, triple]))
                                if word not in misspelled_words:
                                    print(word, 'is possibly misspelled.')
                                misspelled_words.add(word)
    
    misspelled_words_in_triples = list(misspelled_words_in_triples)
    misspelled_words_in_triples.sort()
    for word_in_triple in misspelled_words_in_triples:
        logging.warning(msg=word_in_triple)
    
    if len(misspelled_words_in_triples) > 0:
        print('Possible spelling errors found - for the details consult spellcheck_log.log file')
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run spelling check')
    parser.add_argument('--spell', help='Path to file with new spells', metavar='SPELL')
    parser.add_argument('--ontology', help='Path to ontology file', metavar='ONTOLOGY')
    parser.add_argument('--filter', help='IRI filter', metavar='FILTER')
    args = parser.parse_args()

    logging.basicConfig(
        format='%(message)s',
        filename='spellcheck_log.log')

    check_spelling_in_ontology(new_spell_file_path=args.spell, ontology_location=args.ontology, resource_filter=args.filter)

    
# check_spelling_in_ontology(
#     new_spell_file_path='spell.json',
#     ontology_location='https://spec.pistoiaalliance.org/idmp/ontology/master/latest/QuickIDMPDev.ttl',
#     resource_filter='spec.pistoiaalliance.org')
