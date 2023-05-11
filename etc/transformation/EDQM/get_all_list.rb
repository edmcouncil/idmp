# This script is based on the documentation in https://standardterms.edqm.eu/api/api_doc

require "net/http"
require "json"
require "openssl"
require "base64"

EMAIL = "<!!! CHANGE ME !!!>"
KEY = "<!!! CHANGE ME !!!>"

def perform_request(url)
  uri = URI(url)
  request = Net::HTTP::Get.new(uri)

  # specify Date header
  date_now = Time.now.utc.strftime("%a, %d %b %Y %H:%M:%S GMT")
  request["Date"] = date_now

  # prepare & set the authorization header
  string_to_sign = "GET&#{uri.path}&#{uri.host}&#{date_now}"
  hash = OpenSSL::HMAC.digest("sha512", KEY, string_to_sign)
  encoded = Base64.strict_encode64(hash)
  signature = encoded.slice(-22, 22)
  # puts string_to_sign, hash, encoded, signature
  request["X-STAPI-KEY"] = "#{EMAIL}|#{signature}"

  # perform request
  response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: uri.scheme == "https") do |http|
    http.request(request)
  end

  # parse response to json
  JSON.parse(response.body)
end

klasses = perform_request("https://standardterms.edqm.eu/standardterms/api/v1/classes")
directory_name = "lists"
Dir.mkdir(directory_name) unless File.exist?(directory_name)
klasses["content"].each do |klass|
  code = klass["code"]
  url = "https://standardterms.edqm.eu/standardterms/api/v1/full_data_by_class/#{code}/1/1"
  data = perform_request(url)
  p "writing #{code} list"
  File.open("#{directory_name}/EDQM-#{code}.json", "w") do |f|
    f.write(JSON.pretty_generate(data["content"]))
  end
end

puts "All data available under ./#{directory_name}/ directory"
