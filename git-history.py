#!/usr/bin/env python3
from typing import List, Optional, Tuple
from pathlib import Path
import sqlite3
import dbutils
from db_to_dataframe import create_dataframe, print_dataframe


def run_command(cmd: str, cwd: Optional[str] = None) -> str:
    from subprocess import check_output
    import shlex
    return check_output(shlex.split(cmd), cwd=cwd).decode("utf-8")


def get_history(cwd: Optional[str] = None) -> List[List[str]]:
    lines = run_command('git log --date=short --pretty=format:''%h;"%an";%ad;"%s"'' --shortstat', cwd=cwd).split("\n")

    def parse_string(line: str) -> str:
        # Add missing deletions info
        if "deletion" not in line:
            line += ", 0 deletions(-)"
        elif "insertion" not in line:
            line = ",".join([line.split(",")[0], " 0 insertions(+)", line.split(",")[-1]])
        return line

    def do_replace(x: str) -> str:
        for pattern in ['files changed', 'file changed', 'insertions(+)', 'insertion(+)', 'deletion(-)',
                        'deletions(-)']:
            x = x.replace(f' {pattern}', '')
        return x

    title = None
    rc = []
    for line in lines:
        # Check for weird entries where subject has double quotes or similar issues
        if title is None:
            title = line.split(";", 3)
        # In the lines with stat, add 0 insertions or 0 deletions to make sure we don't break the table 
        elif "files changed" in line.replace("file changed", "files changed"):
            stats = do_replace(parse_string(line)).split(",")
        elif len(line) == 0:
            rc.append(title + stats)
            title = None
        else:
            rc.append(title + ["0", "0", "0"])
            title = line.split(";", 3)
    return rc


def get_file_names(cwd: Optional[str] = None) -> List[Tuple[str, List[Tuple[str, int, int]]]]:
    lines = run_command('git log --pretty="format:%h" --numstat', cwd=cwd).split("\n")
    rc = []
    commit_hash = ""
    files: List[Tuple[str, int, int]] = []
    for line in lines:
        if not line:
            # Git log uses empty line as separator between commits (except for oneline case)
            rc.append((commit_hash, files))
            commit_hash, files = "", []
        elif not commit_hash:
            # First line is commit short hash
            commit_hash = line
        elif len(line.split("\t")) != 3:
            # Encountered an empty commit
            assert(len(files) == 0)
            rc.append((commit_hash, files))
            commit_hash = line
        else:
            added, deleted, name = line.split("\t")
            # Special casing for binary files
            if added == "-":
                assert deleted == "-"
                files.append((name, -1, -1))
            else:
                files.append((name, int(added), int(deleted)))
    return rc


def create_db_schema(handle: sqlite3.Connection) -> None:
    delete_table = "DROP TABLE IF EXISTS commits;"
    create_table_statement = '''CREATE TABLE IF NOT EXISTS commits(
                commit_id TEXT,
                author TEXT,
                date DATE,
                title TEXT,
                number_of_changed_files INT,
                lines_added INT,
                lines_deleted INT);
                '''
    dbutils.execute_statement(handle, delete_table)
    dbutils.execute_statement(handle, create_table_statement)
    delete_table = "DROP TABLE IF EXISTS files;"
    create_table_statement = '''CREATE TABLE IF NOT EXISTS files(
                commit_id TEXT,
                file_name TEXT,
                lines_added INT,
                lines_deleted INT);
                '''
    dbutils.execute_statement(handle, delete_table)
    dbutils.execute_statement(handle, create_table_statement)


def main() -> None:
    tutorials_dir = Path.home() / "repositories" / "tutorials"
    if not tutorials_dir.exists():
        tutorials_dir = Path.home() / "git" / "pytorch" / "tutorials"
    get_history_log = get_history(tutorials_dir)
    commits_to_files = get_file_names(tutorials_dir)
    with open("commit2files.csv", "w") as f:
        f.write("CommitHash, Files\n")
        for entry in commits_to_files:
            commit_id, files = entry
            files = [x[0] for x in files]
            f.write(f'{commit_id}, "{";".join(files)}"\n')
    with open("get_history.csv", "w") as file:
        file.write("CommitHash, AuthoName, Date, Subject, FilesChanged, LinesAdded, LinesDeleted\n")
        for i in get_history_log:
            file.write(f'{";".join(i)}\n')
    db = "test.db"
    connect = dbutils.connect_db(db)
    create_db_schema(connect)
    for entry in get_history_log:
        cursor = connect.cursor()
        cursor.execute("INSERT INTO commits VALUES (?, ?, ?, ?, ?, ?, ?)", entry)
        connect.commit()
    for entry in commits_to_files:
        cursor = connect.cursor()
        commit_id, files = entry
        for (fname, lines_added, lines_deleted) in files:
            cursor.execute("INSERT INTO files VALUES (?, ?, ?, ?)", (commit_id, fname, lines_added, lines_deleted))
        connect.commit()
    create_dataframe(connect, "files")
    create_dataframe(connect, "commits")
    print_dataframe()

if __name__ == "__main__":
    main()
