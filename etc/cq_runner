import argparse
import os
import sys

from rdflib import Graph


def run_cq_tests(
        folder_with_cqs: str,
        ontology_path: str) -> bool:
    cqs_match_ontology = True
    ontology = Graph()
    ontology.parse(source=ontology_path)
    for root, subfolder_paths, file_names in os.walk(folder_with_cqs):
        for file_name in file_names:
            if 'sparql' in file_name:
                input_file_path = os.path.join(folder_with_cqs, file_name)
                input_file = open(input_file_path, 'r')
                input_file_content = input_file.read()
                results = ontology.query(input_file_content)
                if len(results) == 0:
                    print('Competency question failed', file_name)
                    cqs_match_ontology = False
    return cqs_match_ontology


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run tests tests')
    parser.add_argument('--folder_with_competency_questions', help='Path to folder with competency questions', metavar='HYGIENE')
    parser.add_argument('--ontology_path', help='Path to ontology file', metavar='ONTOLOGY')
    args = parser.parse_args()
    
    cqs_match_ontology = \
        run_cq_tests(
            folder_with_cqs=args.folder_with_competency_questions,
            ontology_path=args.ontology_path)
    
    if cqs_match_ontology:
        sys.exit(0)
    sys.exit(-1)
