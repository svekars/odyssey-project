echo "commit id,filenames" > log2.csv 
git log --pretty="format:@%h," --name-only | tr "\n" " " | tr "@" "\n" >> log2.csv
sed -i '' '/^$/d' log2.csv
#sed -i '' 's/$/,/g' log2.csv
sed -i '' 's/, /,/g' log2.csv
sed -i '' 's/  ,/,/g' log2.csv
