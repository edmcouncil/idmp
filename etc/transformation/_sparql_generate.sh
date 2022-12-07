# Downloading the sparql-generate
# TODO: Use sparql-generate image directly
if [ ! -f sparql-generate-$sparql_generate_version.jar ]; then
  echo "Downloading sparql-generate version $sparql_generate_version"
  download_url="https://github.com/sparql-generate/sparql-generate/releases/download/$sparql_generate_version/sparql-generate-$sparql_generate_version.jar"
  $docker_cmd $java_docker_image sh -c "wget -q $download_url"
fi
