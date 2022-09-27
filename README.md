# odyssey-project

# Create a CSV

To create a CSV table, complete these steps:

1. Run `git-history.py`. This script creates two files log.csv and log2.csv.
1. Run `generate-table.py`. This script creates a combined table from the two
   .csv files that includes the following fields:

   * `commit_id`
   * `author`
   * `date`
   * `title`
   * `changed_files` (# of changed files)
   * `added_lines`
   * `deleted lines`
   * `filenames`

# Upload the CSV to SQL database

* `create-sql-table.sh` - creates a table if it doesn't exist
* `add-csv-to-table.py` - adds the CSV to the created SQL table

# Visualize

A sample histogram can be generated with `visualize.py`.
