echo "NSE,KGE,RMSE,R2,lake" > concatenated_stats.csv  # Add the header
find . -type f -name 'statistics.csv' -exec sh -c 'folder=$(basename "$(dirname "$1")"); awk "FNR == 2 {print \$0 \",\" \"$folder\"}" "$1"' _ {} \; >> concatenated_stats.csv
echo "NSE,KGE,RMSE,R2,lake" > concatenated_stats_bott.csv  # Add the header
find . -type f -name 'statistics_bott.csv' -exec sh -c 'folder=$(basename "$(dirname "$1")"); awk "FNR == 2 {print \$0 \",\" \"$folder\"}" "$1"' _ {} \; >> concatenated_stats_bott.csv

#Here's what this modified command does:
#1. find searches for all "stats.csv" files in subfolders.
#2. -exec executes the specified command for each found file.
#3.  sh -c allows you to execute a shell command.
#4. folder=$(basename "$(dirname "$1")") extracts the name of the immediate parent folder of the current "stats.csv" file using basename and dirname.
#5. awk "FNR == 2 {print \$0 \",\" \"$folder\"}" "$1" uses awk to print the second row of the file, followed by a comma, and then the folder name.
