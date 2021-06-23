storage_dir=$(readlink -f $PWD)
export SUEP_BASE=${storage_dir}
export IPYTHONDIR=${storage_dir}/.ipython
source coffeaenv/bin/activate 
