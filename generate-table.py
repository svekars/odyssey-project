import os
import sys
import pandas as pd

os.system("sh git-history.sh")

csv_log2 = pd.read_csv('log2.csv')
ndf = pd.DataFrame(csv_log2.filename.astype(str).str.split(' ').tolist(), index=csv_log2.commit_id).stack()
ndf = ndf.reset_index([0, 'commit_id'])
ndf.columns = ['commit_id', 'filename']
ndf.to_csv('log3.csv', index=False)

csv1 = pd.read_csv('log.csv', sep=',', names=['commit_id', 'author', 'date', 'title','changed_files','lines_added','lines_deleted'], skip_blank_lines=True, lineterminator='\n')
csv2 = pd.read_csv('log3.csv', sep=',', names=['commit_id','filename'], lineterminator='\n')
m = pd.merge(csv1, csv2, left_on='commit_id', right_on='commit_id', how='right')
m.to_csv('merged.csv', header=False, index=False)
