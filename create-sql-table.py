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

def create_table(db_connect, create_table_statement):
    try:
        cursor = db_connect.cursor()
        cursor.execute(create_table_statement)
    except Error as error:
        print(error)

def main():
   db = r"test.db"
   create_table_statement = '''CREATE TABLE IF NOT EXISTS commit_history(
                commit_id TEXT,
                author TEXT,
                date DATE,
                title TEXT,
                number_of_changed_files INT,
                lines_added INT,
                lines_deleted INT,
                filename TEXT);
                '''
   connect = connect_db(db)
   create_table(connect, create_table_statement)

if __name__ == '__main__':
    main()
