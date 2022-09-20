import csv
import sqlite3

db_connect = sqlite3.connect("test.db")

cursor = db_connect.cursor()

create_table = '''CREATE TABLE commit_history(
                ds TEXT,
                filename TEXT);
                '''

cursor.execute(create_table)

f = open('file.csv')

contents = csv.reader(f)

ins = "INSERT INTO commit_history (ds, filename) VALUES(?, ?)"

cursor.executemany(ins, contents)

select_all = "SELECT * FROM commit_history"
rows = cursor.execute(select_all).fetchall()

for r in rows:
    print(r)

db_connect.commit()

db_connect.close()

