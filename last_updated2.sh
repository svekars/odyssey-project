#!/bin/bash
# current script
git ls-tree -r master --name-only | grep -E '.*\.(rst|py)' | while read filename; do
  echo "$(git log --date=short --format="%ad %an" -- $filename) $filename";
done | sort -r | tr  " " ","  > file.csv

