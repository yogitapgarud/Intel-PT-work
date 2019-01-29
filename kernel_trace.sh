#!/bin/sh

sudo /home/yogita/linux/tools/perf/perf-with-kcore record $1 -e intel_pt//k -- ls
cd $1
sudo ../script/perf-read-aux.bash
sudo ../script/perf-read-sideband.bash
#sudo ../bin/ptxed $(sudo ../script/perf-get-opts.bash -k kcore_dir -m perf.data-sideband-cpu3.pevent) --pt perf.data-aux-idx3.bin > ../ls_k_expr1.out
