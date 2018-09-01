#!/bin/bash
wd=$(pwd)
git clone https://github.com/smarnach/pyexiftool.git
cd pyexiftool/
python setup.py install
cd ..
mkdir exiftool
cd exiftool/
wget https://www.sno.phy.queensu.ca/~phil/exiftool/Image-ExifTool-11.09.tar.gz
gzip -dc Image-ExifTool-11.09.tar.gz | tar -xf -
cd Image-ExifTool-11.09/
perl Makefile.PL
#make test
sudo make install
cd $wd
pip install -r requirements.txt
