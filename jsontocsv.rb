require 'json'
require 'csv'

file = File.read('merged-fixed.json')
data_hash = JSON.parse(file)

CSV.open("your_csv.csv", "w") do |csv|
  csv << ["Optimizely UUID", "Variation ID", "Timestamp", "UTD ID", "UTD Session ID", "Referrer URL"]
  data_hash.each do |hash|
    if hash["attributes"]["list"].find { |element| element["element"]["name"] =="visitor_sessionId" } && hash["attributes"]["list"].find { |element| element["element"]["name"] =="visitor_userUtdId" }
      variation_id = if hash["variation_id"]
                       hash["variation_id"]
                     else
                       hash["experiments"]["list"].find { |element| !element["element"]["variation_id"].nil? }["element"]["variation_id"]
                     end

      session_id = hash["attributes"]["list"].find { |element| element["element"]["name"] =="visitor_sessionId" }["element"]["value"]
      utd_id = hash["attributes"]["list"].find { |element| element["element"]["name"] =="visitor_userUtdId" }["element"]["value"]
      csv << [hash["uuid"], variation_id, hash["timestamp"], utd_id, session_id, hash["referer"]]
    end
  end
end
