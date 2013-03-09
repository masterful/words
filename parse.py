import sys, csv, re

# needs at least 1000 uses after the year 2000 to be considered valid, in my eyes
threshold = 10000
# I only care about usages after the year 2000
year      = 2000
wordlist = dict()
valid = re.compile(r'^[a-zA-Z_]*$')

# Use the first argument as the file we need to open
with open(sys.argv[1], 'r') as f:
  r = csv.reader(f, delimiter="\t")
  for data in r:
    if int(data[1]) > year:
      #make all the words lowercase
      word = data[0].lower()
      if not valid.match(word):
        continue
      word = word.split("_")[0]
      usage= int(data[2])
      if word not in wordlist:
        wordlist[word] = usage
      else:
        wordlist[word] += usage

with open("processed-" + sys.argv[1], 'w') as f:
  w = csv.writer(f, delimiter="\t")
  for entry in sorted(wordlist.keys()):
    if wordlist[entry] > threshold:
      w.writerow([entry, wordlist[entry]])
