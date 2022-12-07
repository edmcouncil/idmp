#!/bin/sh

. ../_env.sh
. ../_sparql_generate.sh
. _common.sh

# Perform transformation
if [ -f public_data.json ]; then
  queries=(gsrs-public-data-identifiers gsrs-public-data-names gsrs-public-data-relationships gsrs-public-data-substances)
  for query in "${queries[@]}"; do
    echo "Transforming $query.rqg"
    $docker_cmd $java_docker_image sh -c "java -Xmx20g \
      -jar sparql-generate-$sparql_generate_version.jar \
      -l INFO \
      -q $query.rqg \
      -o $query.ttl \
      -fo TTL"
  done

  result=gsrs-transformed.ttl
  rm -rf $result
  for query in "${queries[@]}"; do
    cat $query.ttl >>$result
  done
  echo "Result available in $result"

  for query in "${queries[@]}"; do
    rm -rf $query.ttl
  done
fi
