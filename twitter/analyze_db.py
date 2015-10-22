from constants import DB_USER, DB_PASSWD, DB_HOST, DB_NAME
import mysql.connector
config = {
              'user': DB_USER,
              'password': DB_PASSWD,
              'host': DB_HOST,
              'database': DB_NAME,
            }

db = mysql.connector.connect(**config)
cur = db.cursor()
myset = {}
cur.execute("select text from Tweet limit 1000")


for tweet in cur.fetchall():
    for word in tweet[0].split(" "):
        if word in myset:
            myset[word] = myset[word]+1
        else:
            myset[word] = 1

print("total unique words is:", len(myset))
sorted_list = sorted(myset.items(), key=lambda x: x[1])

m=150
for k,v in reversed(sorted_list):
    print(k,v)
    m -= 1
    if m<=0:
        break






