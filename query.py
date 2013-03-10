import sys, sqlite3

numargs = len(sys.argv)
if 1 > numargs:
  print "need a list of letters to search with"
  sys.exit(-1)

if "-help" == sys.argv[1]:
  print "query.py search_letters|- [not_letters [usage_threshold]]"
  sys.exit(0)

# Need an alphabet
betty   = "abcdefghijklmnopqrstuvwxyz"
# which letters are we looking for?
haveletters = sys.argv[1]
notletters  = sys.argv[2] if numargs > 2 else ""

# Need a connection to the database
conn        = sqlite3.connect('processed.db')
c           = conn.cursor()

# search for them words
query = "SELECT word from word WHERE "
for letter in betty:
  if haveletters.count(letter) < 1:
    continue
  query += "c" + letter + " >= " + str(haveletters.count(letter)) + " AND "

for letter in notletters:
  query += "c" + letter + " = 0 AND "

if len(haveletters) or len(notletters):
  query = query[:-5]

if numargs > 3:
  query += " AND usage >= " + sys.argv[3]

print query

for row in c.execute(query):
  print row[0]

# and save it all, or it was all for naught
conn.commit()
conn.close()
