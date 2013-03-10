# custom query built to solve letterpress problems
import sys, sqlite3

numargs = len(sys.argv)
if 1 > numargs:
  print "need a list of letters to search with"
  sys.exit(-1)

if "-help" == sys.argv[1]:
  print "query.py letterpress_grid [usage_threshold]"
  sys.exit(0)

# Need an alphabet
betty   = "abcdefghijklmnopqrstuvwxyz"
# which letters are we looking for?
haveletters = sys.argv[1]

# Need a connection to the database
conn        = sqlite3.connect('processed.db')
c           = conn.cursor()

# search for them words
query = "SELECT word from word WHERE "
for letter in betty:
  query += "c" + letter + " <= " + str(haveletters.count(letter)) + " AND "

if numargs > 2:
  query += "usage >= " + sys.argv[2] + " AND "

query = query[:-5]
print query

for row in c.execute(query):
  print row

# and save it all, or it was all for naught
conn.commit()
conn.close()
