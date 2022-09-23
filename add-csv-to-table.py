import csv
import sqlite3
from sqlite3 import Error

def connect_db(dfile):
    """
    Connect to the database
    """
    db_connect = None
    try:
        db_connect = sqlite3.connect(dfile)
    except Error as error:
        print(error)

    return db_connect

def import_csv(db_connect, file):
    cursor = db_connect.cursor()
    contents = csv.reader(file)
    ins = "INSERT INTO commit_history (commit_id,author,date,title,number_of_changed_files,lines_added,lines_deleted,filename) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.executemany(ins, contents)

def test():
    cursor = db_connect.cursor()
    select_all = "SELECT * FROM commit_history"
    rows = cursor.execute(select_all).fetchall()
    for r in rows:
       print(r)

def main():
   db = r"test.db"
   file = open("merged.csv")
   connect = connect_db(db)
   import_csv(connect, file)
   connect.commit()
   #test()
   connect.close()

if __name__ == '__main__':
    main()
