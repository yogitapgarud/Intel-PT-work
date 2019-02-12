#!/bin/sh

sudo apt-get install vim build-essential linux-tools-generic git cmake flex bison gawk

git clone https://github.com/01org/processor-trace.git
git clone https://github.com/intelxed/mbuild.git mbuild
git clone https://github.com/intelxed/xed

cd xed
mkdir obj
cd obj
../mfile.py
sudo ../mfile.py --prefix=/usr/local install

cd processor-trace
cmake .
make
sudo make install
sudo ldconfig

https://mirrors.edge.kernel.org/pub/linux/kernel/v4.x/
tar -xf Downloads/linux-4.15.tar.xz
cd linunx-4.15
make -C tools/perf/
