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
os.system('java --illegal-access=deny -jar ~/bin/parquet-tools-1.11.0.jar merge *.parquet merged.parquet > /dev/null')

print ("» Convert JSON to CSV")
os.system('java --illegal-access=deny -jar ~/bin/parquet-tools-1.11.0.jar cat -j merged.parquet > merged.json')

# parquet-tools -j outputs multiple objects, we need to merge them into one
os.system(r'''echo '[' `gawk -v RS= '{gsub(/}\n{/,"},{")} 1' merged.json` ']' > merged-fixed.json''')

# Convert JSON to CSV
os.system('ruby ~/bin/jsontocsv.rb')

print ("Done!")
