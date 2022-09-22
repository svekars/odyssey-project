git log --shortstat \
    | egrep "file[s]* changed" \
    | sed 's/changed, \([0-9]\+ deletions\)/changed, 0 insertions(+), \1/g' \
    | awk '{files+=$1; inserted+=$4; deleted+=$6} END {print "files changed", files, "lines inserted:", inserted, "lines deleted:", deleted}'
