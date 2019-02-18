#!/bin/sh

#installing dependencies

wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.42.tar.gz
tar -zxf pcre-8.42.tar.gz
cd pcre-8.42
./configure
make
sudo make install

wget http://zlib.net/zlib-1.2.11.tar.gz
tar -zxf zlib-1.2.11.tar.gz
cd zlib-1.2.11
./configure
make
sudo make install

wget http://www.openssl.org/source/openssl-1.0.2q.tar.gz
tar -zxf openssl-1.0.2q.tar.gz
cd openssl-1.0.2q
./Configure darwin64-x86_64-cc --prefix=/usr
make
sudo make install

#Download Nginx source
wget https://nginx.org/download/nginx-1.15.7.tar.gz
tar zxf nginx-1.15.7.tar.gz
cd nginx-1.15.7

