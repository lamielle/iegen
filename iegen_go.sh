#!/bin/sh

#Build this on a 32-bit machine!
#CLooG doesn't like our 64-bit setup

echo "--------------------------------------------------"
echo " CHECKING OUT IEGen"
echo "--------------------------------------------------"

svn co svn+ssh://europa.cs.colostate.edu/s/bach/e/proj/rtrt/SVNRepository/RTRTcode/trunk/iegen/

echo "--------------------------------------------------"
echo " Extracting Polylib and CLooG"
echo "--------------------------------------------------"

tar -xvf cloog-0.14.0.tar.gz
tar -xvf polylib-5.22.3.tar.gz
mkdir polylib
mkdir cloog

echo "--------------------------------------------------"
echo " BUILDING Polylib"
echo "--------------------------------------------------"

cd polylib-5.22.3
./configure --prefix=$PWD/../polylib
make
make tests
make install

echo "--------------------------------------------------"
echo " BUILDING CLooG"
echo "--------------------------------------------------"

cd ../cloog-0.14.0
cd cloog-0.14.0
./configure --prefix=$PWD/../cloog --with-polylib=$PWD/../polylib
make
make install
cd ..
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD/cloog/lib:$PWD/polylib/lib

echo "--------------------------------------------------"
echo " BUILDING IEGen"
echo "--------------------------------------------------"

cd iegen
./waf configure --prefix=$PWD --cloog-loc=$PWD/../cloog --polylib=$PWD/../polylib
./waf build
./waf install

echo "--------------------------------------------------"
echo " Running moldyn.spec"
echo "--------------------------------------------------"

export PYTHONPATH=$PWD:$PYTHONPATH
./examples/moldyn.spec
