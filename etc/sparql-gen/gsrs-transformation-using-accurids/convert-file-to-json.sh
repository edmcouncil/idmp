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

# Convert the public_data to valid json
./jq -c -s '.' public_data > public_data.json