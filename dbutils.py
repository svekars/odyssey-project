import sqlite3
from sqlite3 import Error

def connect_db(dfile: str) -> sqlite3.Connection:
    """
    Connect to the database
    """
    db_connect = None
    try:
        db_connect = sqlite3.connect(dfile)
    except sqlite3.Error as error:
        print(error)
    return db_connect

def execute_statement(db_connect: sqlite3.Connection, table_statement: str) -> None:
    try:
        cursor = db_connect.cursor()
        cursor.execute(table_statement)
        db_connect.commit()
    except sqlite3.Error as error:
        print(error)

if __name__ == "__main__":
    connect_db("test.db")
