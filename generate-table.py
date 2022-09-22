import os
import sys
import pandas as pd

os.system("sh git-history.sh")

csv1 = pd.read_csv('log.csv', sep=',', names=['commit id', 'author', 'date', 'title','changed_files','lines added','lines deleted'], skip_blank_lines=True, lineterminator='\n')
csv2 = pd.read_csv('log2.csv', sep=',', names=['commit id','filenames'], skip_blank_lines=True, lineterminator='\n')
m = pd.merge(csv1, csv2, on='commit id', how='inner')
m.to_csv('merged.csv', header=False, index=False)
