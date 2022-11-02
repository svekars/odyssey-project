import pandas as pd
import sqlite3
from sqlite3 import connect

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

def create_dataframe() -> None:
    conn = connect_db('test.db')
    df = pd.read_sql('SELECT * FROM files', conn)
    df2 = pd.read_sql('SELECT * FROM commits', conn)
    print(df)
    print(df2)

if __name__ == "__main__":
    create_dataframe()
