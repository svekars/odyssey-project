#!/usr/bin/env python3
from typing import List, Optional, Tuple
from pathlib import Path

def run_command(cmd: str, cwd: Optional[str] = None ) -> str:
   from subprocess import check_output
   import shlex
   return check_output(shlex.split(cmd), cwd=cwd).decode("utf-8")


def get_history(cwd: Optional[str] = None) -> List[str]:
    rc = run_command('git log --date=short --pretty=format:''%h,"%an",%ad,"%s",'' --shortstat', cwd=cwd).split("\n")
    rc = [i.replace(' files changed', '').replace(' file changed', '').replace(' insertions(+)', '').replace(' insertion(+)', '').replace(' deletion(-)', '').replace(' deletions(-)', '') for i in rc]
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

def main() -> None:
    tutorials_dir = Path.home() / "git" / "pytorch" / "tutorials"
    commits_to_files = get_file_names(tutorials_dir)
    with open("commit2files.csv", "w") as f:
        f.write("CommitHash, Files\n")
        for entry in commits_to_files:
            f.write(f'{entry[0]}, "{";".join(entry[1])}"\n')

if __name__ == "__main__":
    main()
