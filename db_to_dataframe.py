import pandas as pd
from dbutils import connect_db
import sqlite3

dbfile = 'test.db'

def create_dataframe(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    return pd.read_sql(f"SELECT * from {table_name}", conn)

def print_dataframe() -> None:
    conn = connect_db(dbfile)
    print(create_dataframe(conn, "files"))
    print(create_dataframe(conn, "commits"))

if __name__ == "__main__":
    print_dataframe()
