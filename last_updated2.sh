#!/bin/bas
# current script
#git ls-tree -r master --name-only | grep -E '.*\.(rst|py)' | while read filename; do
#  echo "$(git log -1 --date=short --format="%ad" -- $filename) $filename";
#done | sort -r | tr  " " ","  > file.csv

git ls-tree -r master --name-only | grep -E '.*\.(rst|py)' | 
