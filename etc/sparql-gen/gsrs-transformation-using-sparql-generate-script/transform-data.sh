#!/bin/bash

# Download jq
OS=$(uname -s)
case $OS in
  CYGWIN* | MINGW64*)
    OS=win64.exe
    ;;
  Darwin)
    OS=osx-amd64
    ;;
  Linux)
    OS=linux64
    ;;
esac

url=https://github.com/stedolan/jq/releases/download/jq-1.6/jq-$OS
echo "Downloading jq from $url"
curl -fLO "${url}"
mv jq-$OS jq
chmod +x jq

# Run transformation
for (( i = 0; i < 14; i++))
do
    (( startIndex = i * 10000 + 1 ))
    echo "The value of \"startIndex\" is $startIndex."
    (( endIndex = (i + 1) * 10000 ))
    echo "The value of \"endIndex\" is $endIndex."
    sed -n -e ''"$startIndex"','"$endIndex"'p' public_data > temp.json
    ./jq -c -s '.' temp.json > public_data.json
    java -Xmx20g -jar sparql-generate-2.0.12.jar -l INFO -q gsrs-substances.rqg -o ./gsrs-transformed/gsrs-10000-substances-iter-$i.ttl -fo TTL
    java -Xmx20g -jar sparql-generate-2.0.12.jar -l INFO -q gsrs-identifiers.rqg -o ./gsrs-transformed/gsrs-10000-identifiers-iter-$i.ttl -fo TTL
    java -Xmx20g -jar sparql-generate-2.0.12.jar -l INFO -q gsrs-relationships.rqg -o ./gsrs-transformed/gsrs-10000-relationships-iter-$i.ttl -fo TTL
    java -Xmx20g -jar sparql-generate-2.0.12.jar -l INFO -q gsrs-names.rqg -o ./gsrs-transformed/gsrs-10000-names-iter-$i.ttl -fo TTL
done

cat ./gsrs-transformed/* > ./gsrs-transformed/gsrs-transformed.ttl
cd ./gsrs-transformed
shopt -s extglob
rm -v !("gsrs-transformed.ttl")