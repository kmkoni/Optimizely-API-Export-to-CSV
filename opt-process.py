# Convert Optimizely API output to CSV 1.0

import sys,os,shutil,json,csv

print("Converting Optimizely API output to CSV...")
print("» Collect all Parquet files")
rdir = os.getcwd()

for root, subdirs, files in os.walk(rdir):
    for file in files:
        path = os.path.join(root, file)
        if os.path.join(root) != rdir:
            shutil.copy(path, os.path.join(rdir))

print("» Merge Parquet files")
os.system('java --illegal-access=deny -jar /usr/local/bin/parquet-tools-1.11.0.jar merge *.parquet merged.parquet > /dev/null')

print ("» Convert JSON to CSV")
os.system('java --illegal-access=deny -jar /usr/local/bin/parquet-tools-1.11.0.jar cat -j merged.parquet > merged.json')

# parquet-tools -j outputs multiple objects, we need to merge them into one
os.system(r'''echo '[' `gawk -v RS= '{gsub(/}\n{/,"},{")} 1' merged.json` ']' > merged-fixed.json''')

with open('merged-fixed.json') as json_file:
    jsondata = json.load(json_file)

data_file = open('output.csv', 'w', newline='')
csv_writer = csv.writer(data_file)
 
count = 0
for data in jsondata:
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())
 
data_file.close()    

print ("Done!")