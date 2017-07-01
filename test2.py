import sqlite3
conn = sqlite3.connect("qq_bot_database.db")
cu = conn.cursor()

cu.execute("select * from tips_data")
result = cu.fetchall()
for line in result:
    print line[-1]