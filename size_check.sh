# find files with certain size
find . -type f -size -1840M -exec ls -lh {} \;
# delete files with certain size
find . -type f -size -1840M -exec rm {} \;
# check number of files
ls -1 | wc -l
