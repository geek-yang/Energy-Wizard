# load ncl
out_path=$1
#out_path="/home/ESLT0068/WorkFlow/Test/era1978_1980/era1979/"
export path=${out_path}
#export path="/home/ESLT0068/WorkFlow/Test/era1978_1980/era1979/"
#ncl 'dir="/home/ESLT0068/WorkFlow/Test/era1978_1980/era1979/"' NCL_ERAI_div_example.ncl
#printf "${path}"
cur_dir=$(pwd)
dir_ncl=${cur_dir}'/subdir/NCL_ERAI_div_example.ncl'
ncl -Q -n ${dir_ncl}
