#!/bin/sh

. _common.sh

# Downloading the sparql-generate
# TODO: Use sparql-generate image directly
if [ ! -f sparql-generate-$sparql_generate_version.jar ]; then
  echo "Downloading sparql-generate version $sparql_generate_version"
  download_url="https://github.com/sparql-generate/sparql-generate/releases/download/$sparql_generate_version/sparql-generate-$sparql_generate_version.jar"
  $docker_cmd $java_docker_image sh -c "wget -q $download_url"
fi

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

  for query in "${queries[@]}"; do
    cat $query.ttl >gsrs-transformed.ttl
  done
  echo "Result available in gsrs-transformed.ttl"

  for query in "${queries[@]}"; do
    rm -rf $query.ttl
  done
fi
