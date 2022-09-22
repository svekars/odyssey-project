echo "commit id,author,date,title,changed files,lines added,lines deleted" > log.csv 
git log --date=short --pretty=format:'@%h,"%an",%ad,"%s",' --shortstat | tr "\n" " " | tr "@" "\n" >> log.csv
sed -i '' 's/ files changed//g;s/ file changed//g;s/ insertions(+)//g;s/ insertion(+)//g;s/ deletions(-)//g;s/ deletion(-)//g' log.csv
sed -i '' '/^$/d' log.csv
#sed -i '' 's/$/,/g' log.csv
sed -i '' 's/  //g' log.csv
sed -i '' 's/, /,/g' log.csv
sed -i '' 's/"Train neural nets to play video games"/Train neural nets to play video games/g' log.csv
