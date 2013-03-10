import sys, csv, re, sqlite3

# Need an alphabet
betty= "abcdefghijklmnopqrstuvwxyz"

# Need a connection to the database
conn = sqlite3.connect('processed.db')
c    = conn.cursor()
# (Only need to use this one once)
try:
  letterlist = ""
  letterdefs = ""
  for letter in betty:
    letterlist += "c" + letter + ","
    letterdefs += "c" + letter + " INTEGER,"
  c.execute("CREATE TABLE word (" + letterdefs + "usage INTEGER, word TEXT PRIMARY KEY)")
  for letter in betty:
    c.execute("CREATE INDEX c" + letter + "INDEX ON word (c" + letter +")")
except:
  c.execute("DELETE FROM word")

# Use the first argument as the file we need to open
with open(sys.argv[1], 'r') as f:
  # The files are in tab-delimited format
  # It is a simple: word \t commonality \n
  r = csv.reader(f, delimiter="\t")
  for data in r:
    word  = data[0]
    if not word:
      continue
    query = "INSERT INTO word (" + letterlist + "usage,word) values ("
    # build letter counts
    for letter in betty:
      query += str(word.count(letter)) + ","
    query += str(data[1]) + ",'" + word + "')"
    c.execute(query)

# and save it all, or it was all for naught
conn.commit()
conn.close()
