# Unzip & Converting the public_data to valid json
if [ ! -f public_data.json ]; then
  if [ -f public_data.gsrs ]; then
    echo "Unzipping public_data.gsrs"
    mv public_data.gsrs public_data.gz
    $docker_cmd $java_docker_image sh -c "gunzip -f public_data.gz"
  fi

  if [ -f public_data ]; then
    echo "Convert the public_data to valid json format & name it as public_data.json"
    $docker_cmd jetbrainsinfra/jq sh -c "jq -c -s '.' public_data > public_data.json"
  fi
fi

if [ ! -f public_data.json ]; then
  echo "public_data.json file not found! Read the instructions in the README.md"
  exit 1
fi
