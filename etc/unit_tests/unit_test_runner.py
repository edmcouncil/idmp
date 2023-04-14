import argparse
import json
import os.path
import sys
import shutil

import yaml
import jsondiff

from rdflib import Graph
from jsondiff import diff

def get_unit_tests_config(unit_test_config_file_path: str, root_folder: str) -> dict:
    with open(os.path.join(root_folder, unit_test_config_file_path)) as file:
        config = yaml.safe_load(file)
    return config


def get_sparql_query(config: dict, root_folder: str) -> str:
    with open(os.path.join(root_folder, config['sparql_template'])) as file:
        sparql_template = file.read()
        sparql_parameters = config['parameters']
        file.close()
    sparql_query = sparql_template
    for sparql_parameter in sparql_parameters:
        sparql_parameter_value = config['parameters'][sparql_parameter]
        if config['parameters'][sparql_parameter].startswith('<') and config['parameters'][sparql_parameter].endswith('>'):
            sparql_query = sparql_query.replace(sparql_parameter, sparql_parameter_value)
        else:
            sparql_query = sparql_query.replace(sparql_parameter, '"' + sparql_parameter_value + '"')
    return sparql_query


def run_unit_test(ontology_location: str, root_folder: str, unit_test_config_file_path: str) -> bool:
    cq_tests_passed = True
    ontology = Graph()
    ontology.parse(ontology_location)
    unit_tests_config = get_unit_tests_config(unit_test_config_file_path, root_folder=root_folder)
    for unit_test_config in unit_tests_config.values():
        sparql_query = get_sparql_query(config=unit_test_config, root_folder=root_folder)
        query_result = ontology.query(sparql_query)
        query_result_as_dict = json.loads(query_result.serialize(format='json').decode())
        with open(os.path.join(root_folder, unit_test_config['expected_output'])) as file:
            expected_query_result = json.loads(file.read())
        if not query_result_as_dict == expected_query_result:
            print('Competency question', unit_test_config['sparql_template'], ' run as a unit test failed.')
			print('Difference is: ', diff(expected_query_result, query_result_as_dict, syntax='explicit'))
            cq_tests_passed = False
        else:
            print('Competency question', unit_test_config['sparql_template'], ' run as a unit test passed.')
    return cq_tests_passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run unit tests')
    parser.add_argument('--ontology_location', help='Path to ontology location')
    parser.add_argument('--root_folder', help='Path to the root folder')
    parser.add_argument('--cq_source', help='Path to the sources of cq templates')
    args = parser.parse_args()
    
    shutil.copytree(src=args.cq_source, dst=os.path.join(args.root_folder, 'cq_templates/'))
    
    cq_tests_passed = \
        run_unit_test(
            ontology_location=args.ontology_location,
            root_folder=args.root_folder,
            unit_test_config_file_path='configs/unit_tests_config.yaml')
    
    if cq_tests_passed:
        sys.exit(0)
    sys.exit(-1)
