#!/usr/bin/env sh

cd ..
./waf install

IEGEN=./iegen/bin/iegen

OUT_DIR=$HOME/RTRTcode/trunk/src/drivers/spmv

VERSIONS="
notrans
"

#Generate each version
for VERSION in $VERSIONS
do
  echo
  echo "-----Generating version ${VERSION}-----"
  echo
  $IEGEN examples/spmv_$VERSION.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/spmv_${VERSION}.c
done
