#!/usr/bin/env sh

./waf install

IEGEN=./iegen/bin/iegen

OUT_DIR=$HOME/RTRTcode/trunk/src/drivers/spmv

VERSIONS="
notrans
cpack
cacheblock
"

exit_on_error() {
#Stop running if the program didn't exit with a 0 return value↲
if [ $1 != 0 ]; then
  echo "---------- Command exited with a non-zero exit code ($1), quitting... ----------"↲
  exit 1
fi
}

#Generate each version
for VERSION in $VERSIONS
do
  echo
  echo "-----Generating version ${VERSION}-----"
  echo
  command="$IEGEN examples/spmv_$VERSION.spec --inspector-name=inspector_${VERSION}_gen --executor-name=executor_${VERSION}_gen -o $OUT_DIR/iegen_${VERSION}_gen.c"
  echo $command
  $command
  exit_on_error $?
done
