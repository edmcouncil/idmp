import argparse
import json
import logging
import re
import sys

from rdflib import Graph, Literal, URIRef
from spellchecker import SpellChecker

HTTP_REGEX = re.compile(pattern='http[^\s]+')
LOCAL_NAME_SEPARATOR = '/'
HAS_LANGUAGE_PREDICATE = URIRef('ttps://www.omg.org/spec/MVF/MultipleVocabularyFacility/hasLanguage')
ENGLISH_LANGUAGE_OBJECT = URIRef('https://www.omg.org/spec/LCC/Languages/ISO639-1-LanguageCodes/English')


def __get_local_name_from_iri(iri: URIRef) -> str:
    local_name = str(iri).split(sep=LOCAL_NAME_SEPARATOR)[-1]
    return local_name


def __get_local_names(ontology: Graph) -> set:
    local_names_in_ontology = set()
    for (subject, predicate, object) in ontology:
        if isinstance(subject, URIRef):
            local_names_in_ontology.add(__get_local_name_from_iri(iri=subject))
        if isinstance(predicate, URIRef):
            local_names_in_ontology.add(__get_local_name_from_iri(iri=predicate))
        if isinstance(object, URIRef):
            local_names_in_ontology.add(__get_local_name_from_iri(iri=object))
    return local_names_in_ontology


def __check_word(
        annotation_value: str,
        word: str,
        misspelled_words_in_triples: set,
        misspelled_words: set,
        spellchecker: SpellChecker,
        triple_subject: URIRef,
        triple_predicate: URIRef):
    word = word.replace("'s", "")
    if word == word.upper():
        return
    else:
        if word.endswith('s'):
            if word[:-1] == word[:-1].upper():
                return
    if any(char.isdigit() for char in word):
        return
    if word[0].upper() == word[0]:
        return
    
    if word not in spellchecker and word[:-1] not in spellchecker and not word.lower() in spellchecker:
        if len(word) > 2:
            triple = '|'.join([triple_subject, triple_predicate, annotation_value])
            misspelled_words_in_triples.add('|'.join([word, triple]))
            if word not in misspelled_words:
                print(word, 'is possibly misspelled.')
            misspelled_words.add(word)


def __check_if_literal_is_in_scope(literal: Literal, triple_subject: URIRef, ontology: Graph) -> bool:
    if literal.language is None:
        language_objects = set(ontology.objects(subject=triple_subject, predicate=HAS_LANGUAGE_PREDICATE))
        return ENGLISH_LANGUAGE_OBJECT in language_objects
    else:
        return literal.language == 'en'


def __get_misspellings(ontology: Graph, resource_filter: str, spellchecker: SpellChecker) -> set:
    misspelled_words_in_triples = set()
    misspelled_words = set()
    for (triple_subject, triple_predicate, triple_object) in ontology:
        if resource_filter in str(triple_subject):
            if isinstance(triple_object, Literal):
                literal = triple_object
                literal_value = literal.value
                if isinstance(literal_value, str):
                    continue_search = __check_if_literal_is_in_scope(literal=literal, triple_subject=triple_subject, ontology=ontology)
                    if continue_search:
                        trunc_text = re.sub(pattern=HTTP_REGEX, repl='', string=literal_value)
                        trunc_text = re.sub(pattern=r'[a-z\-]+:[^\s]+', repl='', string=trunc_text)
                        words = spellchecker.split_words(text=trunc_text)
                        for word in words:
                            __check_word(
                                word=word,
                                misspelled_words_in_triples=misspelled_words_in_triples,
                                misspelled_words=misspelled_words,
                                spellchecker=spellchecker,
                                triple_subject=triple_subject,
                                triple_predicate=triple_predicate,
                                annotation_value=triple_object)
    return misspelled_words_in_triples


def check_spelling_in_ontology(new_spell_file_path: str, ontology_location: str, resource_filter: str):
    spell = SpellChecker()
    with open(file=new_spell_file_path) as new_spell_file:
        new_spell_words = json.load(new_spell_file)
    spell.word_frequency.load_words(new_spell_words)
    ontology = Graph()
    ontology.parse(ontology_location)
    local_names_in_ontology = __get_local_names(ontology=ontology)
    spell.word_frequency.load_words(local_names_in_ontology)
    misspelled_words_in_triples = \
        __get_misspellings(
            ontology=ontology,
            spellchecker=spell,
            resource_filter=resource_filter)
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

    check_spelling_in_ontology(
        new_spell_file_path=args.spell,
        ontology_location=args.ontology,
        resource_filter=args.filter)
