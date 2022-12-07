#!/bin/sh

. ../../_env.sh
. ../../_sparql_generate.sh

# Perform transformation
if [ -f sms-substances-list.csv ]; then
  query=spor-substances
  echo "Transforming $query.rqg"
  $docker_cmd $java_docker_image sh -c "java -Xmx20g \
      -jar sparql-generate-$sparql_generate_version.jar \
      -l INFO \
      -q $query.rqg \
      -o $query.ttl \
      -fo TTL"
  echo "Result available in $query.ttl"
else
  echo "sms-substances-list.csv file not found! Read the instructions in the README.md"
  exit 1
fi
