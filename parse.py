import sys, csv, re

# needs at least 1000 uses after the year 2000 to be considered valid, in my eyes
threshold = 10000
year      = 2000
# store all the words in ... a dictionary!
wordlist  = dict()
# compile a regex that will prune out words with numbers in them, or punctuation
# Note for future: this will remove accented letters as well
valid     = re.compile(r'^[a-zA-Z_]*$')

# Use the first argument as the file we need to open
with open(sys.argv[1], 'r') as f:
  # The files are in tab-delimited format
  # Version 2 uses: word \t year \t # of appearances \t in # of books \n
  r = csv.reader(f, delimiter="\t")
  for data in r:
    # Only count occurences after the given year
    if int(data[1]) > year:
      # Remove words with numbers and punctuation ...
      if not valid.match(data[0]):
        continue
      # Make all the words lowercase, and amalgamate distinctions between parts of speech
      word = data[0].split("_")[0].lower()
      usage= int(data[2])
      # Increment the usage, by storing it in our dictionary
      if word not in wordlist:
        wordlist[word] = usage
      else:
        wordlist[word] += usage

# Now that we've parsed the input file, we'll save the processed file
with open("processed-" + sys.argv[1], 'w') as f:
  # Still in tab-delimited format, this time it's just: word \t usage \n
  w = csv.writer(f, delimiter="\t")
  # Since Google's Ngram project doesn't guarantee alphabetic order, we'll do that here
  for entry in sorted(wordlist.keys()):
    # But we'll only print out words that exceed the minimum number of appearances required
    if wordlist[entry] > threshold:
      # [word, usage]
      w.writerow([entry, wordlist[entry]])
