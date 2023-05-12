# This script is based on the documentation in https://standardterms.edqm.eu/api/api_doc

require "net/http"
require "json"
require "openssl"
require "base64"

# Set credentials
EMAIL = "<!!! CHANGE ME !!!>"
KEY = "<!!! CHANGE ME !!!>"

def prepare_request(url)
  uri = URI(url)
  request = Net::HTTP::Get.new(uri)

  # Specify Date header
  date_now = Time.now.utc.strftime("%a, %d %b %Y %H:%M:%S GMT")
  request["Date"] = date_now

  # Prepare & set the authorization header
  string_to_sign = "GET&#{uri.path}&#{uri.host}&#{date_now}"
  hash = OpenSSL::HMAC.digest("sha512", KEY, string_to_sign)
  encoded = Base64.strict_encode64(hash)
  signature = encoded.slice(-22, 22)
  request["X-STAPI-KEY"] = "#{EMAIL}|#{signature}"

  [uri, request]
end

def perform_request(url)
  uri, request = prepare_request(url)

  # Perform request
  response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: uri.scheme == "https") do |http|
    http.request(request)
  end

  # Parse response to json
  begin
    JSON.parse(response.body)
  rescue JSON::ParserError => e
    puts "Failed to parse JSON response: #{e.message}"
    return nil
  end
end

def write_to_file(directory_name, code, data)
  begin
    File.write("#{directory_name}/EDQM-#{code}.json", JSON.pretty_generate(data["content"]))
  rescue => e
    puts "Failed to write to file: #{e.message}"
  end
end

# Main script
begin
  klasses = perform_request("https://standardterms.edqm.eu/standardterms/api/v1/classes")
  directory_name = "lists"
  Dir.mkdir(directory_name) unless File.exist?(directory_name)
  klasses["content"].each do |klass|
    code = klass["code"]
    url = "https://standardterms.edqm.eu/standardterms/api/v1/full_data_by_class/#{code}/1/1"
    data = perform_request(url)
    puts "writing #{code} list"
    write_to_file(directory_name, code, data) if data
  end
  puts "All data available under ./#{directory_name}/ directory"
rescue => e
  puts "An error occurred: #{e.message}"
end
