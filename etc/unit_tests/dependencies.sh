#!/bin/sh

# This script is to install common dependencies for running the unit tests.

# Build & Install the Test Runner
mvn -B package --file etc/unit_tests/pom.xml

# Install SPARQL-Generate
url=https://github.com/sparql-generate/sparql-generate/releases/download/2.0.12/sparql-generate-2.0.12.jar
sudo wget --no-verbose -m -nH -nd -O sparql-generate.jar $url

# Install Robot
sudo wget --no-verbose -m -nH -nd -P /usr/bin https://raw.githubusercontent.com/ontodev/robot/master/bin/robot
sudo wget --no-verbose -m -nH -nd -P /usr/bin https://github.com/ontodev/robot/releases/latest/download/robot.jar
sudo chmod +x /usr/bin/robot

# Prepare IDMP Ontologies
robot merge --input AboutIDMPOntologiesAndExamples.rdf --output AboutIDMPOntologiesAndExamples.ttl --catalog /home/runner/work/idmp/idmp/catalog-v001.xml
