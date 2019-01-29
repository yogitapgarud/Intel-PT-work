#!/bin/sh

~/libexec/perf-core/perf-with-kcore record pt_ls -e intel_pt// -- ls

cd pt_ls
sudo ../script/perf-read-aux.bash
sudo ../script/perf-read-sideband.bash

sudo ../bin/ptxed $(../script/perf-get-opts.bash -k kcore_dir -m perf.data-sideband-cpu0.pevent) --pt perf.data-aux-idx0.bin > ../ls_exp1.out
