import subprocess
import os
path_out = "/home/ESLT0068/WorkFlow/Test/era1978_1980/era1979"
#subprocess.call(["bash","./scheduler_NCL.sh"])
#subprocess.call(["bash","./scheduler_NCL.sh","/home/ESLT0068/WorkFlow/Test/era1978_1980/era1979/"])
subprocess.call(["bash","./subdir/scheduler_NCL.sh","{}/".format(path_out)])
