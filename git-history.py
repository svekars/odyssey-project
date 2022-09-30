#!/usr/bin/env python3
from typing import List, Optional, Tuple
from pathlib import Path

def run_command(cmd: str, cwd: Optional[str] = None ) -> str:
   from subprocess import check_output
   import shlex
   return check_output(shlex.split(cmd), cwd=cwd).decode("utf-8")


def get_history(cwd: Optional[str] = None) -> List[str]:
    rc = run_command('git log --date=short --pretty=format:''%h,"%an",%ad,"%s",'' --shortstat', cwd=cwd).split("\n")
    # TODO: Remove "files change", ... using `__str__.replace` method
    return ["".join(rc[3*i:3*i+2]) for i in range(len(rc)//3)]


def get_file_names(cwd: Optional[str] = None) -> List[Tuple[str, List[str]]]:
    lines = run_command('git log --pretty="format:%h" --name-only', cwd=cwd).split("\n")
    rc = []
    commit_hash = ""
    files: List[str] = []
    for line in lines:
        if not line:
            # Git log uses empty line as separator between commits (except for oneline case)
            rc.append((commit_hash, files))
            commit_hash, files = "", []
        elif not commit_hash:
            # First line is commit short hash
            commit_hash = line
        else:
            # Other non-empty lines are filesnames
            files.append(line)
    return rc

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

def execute_statement(db_connect, table_statement):
    try:
        cursor = db_connect.cursor()
        cursor.execute(table_statement)
    except Error as error:
        print(error)

def main() -> None:
    tutorials_dir = Path.home() / "git" / "pytorch" / "tutorials"
    commits_to_files = get_file_names(tutorials_dir)
    with open("commit2files.csv", "w") as f:
        f.write("CommitHash, Files\n")
        for entry in commits_to_files:
            f.write(f'{entry[0]}, "{";".join(entry[1])}"\n')
    db = r"test.db"
    delete_table = '''DROP TABLE commit_history;'''
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
    upload_data = '''INSERT INTO commit_history (commit_id,author,date,title,number_of_changed_files,lines_added,lines_deleted,filename) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'''
    connect = connect_db(db)
    execute_statement(connect, delete_table)
    execute_statement(connect, create_table_statement)


if __name__ == "__main__":
    main()
