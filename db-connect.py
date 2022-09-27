import csv
import sqlite3

def connect_db(dfile):
    """
    Connect to the database
    """
    db_connect = None
    try:
        db_connect = sqlite3.connect(dfile)
        return db_connect
    except Error as error:
        print(error)

    return db_connect

create_table_statement = '''DROP TABLE IF EXISTS commit_history;
                CREATE TABLE commit_history(
                commit_id TEXT,
                author TEXT,
                date DATE,
                title TEXT,
                number_of_changed_files INT,
                lines_added INT,
                lines deleted INT,
                filename TEXT);
                '''

def create_table(connect_db, create_table_statement):
     """
     Create a table if it does not extist
     """
     cursor = connect_db.cursor()
     cursor.execute(create_table_statement)

def import_csv():
     f = open('merged.csv')
     cursor = connect_db.cursor()
     contents = csv.reader(f)
     ins = "INSERT INTO commit_history (commit id,author,date,title,changed files,lines added,lines deleted, filenames) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
     cursor.executemany(ins, contents)
     connect_db.commit()

def test():
     select_all = "SELECT * FROM commit_history"
     rows = cursor.execute(select_all).fetchall()
     for r in rows:
        print(r)
     connect_db.close()

if __name__ == '__main__':
    connect_db("test.db")
    create_table(connect_db, create_table_statement)
    import_csv()
    test()


