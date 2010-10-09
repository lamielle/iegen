#!/usr/bin/env sh

./waf install

IEGEN=./iegen/bin/iegen

OUT_DIR=$HOME/RTRTcode/trunk/src/drivers/moldyn

exit_on_error() {
#Stop running if the program didn't exit with a 0 return value↲
if [ $1 != 0 ]; then
  echo "---------- Command exited with a non-zero exit code ($1), quitting... ----------"↲
  exit 1
fi
}

#-----no_trans-----
VERSION=notrans_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
command="$IEGEN examples/moldyn_full.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c"
echo $command
$command
exit_on_error $?

#-----cpack_only-----
VERSION=cpack_only_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
command="$IEGEN examples/moldyn_full_cpack_only.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c"
echo $command
$command
exit_on_error $?

#-----cpack_align-----
VERSION=cpack_align_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
command="$IEGEN examples/moldyn_full_cpack_align.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c"
echo $command
$command
exit_on_error $?

#-----cpack_align_ptrupdate-----
VERSION=cpack_align_ptrupdate_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
command="$IEGEN examples/moldyn_full_cpack_align_ptrupdate.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c"
echo $command
$command
exit_on_error $?

#-----cpack_align_ptrupdate_lexmin-----
VERSION=cpack_align_ptrupdate_lexmin_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
command="$IEGEN examples/moldyn_full_cpack_align_ptrupdate_lexmin.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c"
echo $command
$command
exit_on_error $?

#-----cpack_align_ptrupdate_lexmin_ptrupdate-----
VERSION=cpack_align_ptrupdate_lexmin_ptrupdate_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
command="$IEGEN examples/moldyn_full_cpack_align_ptrupdate_lexmin_ptrupdate.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c"
echo $command
$command
exit_on_error $?

#-----cpack_align_ptrupdate_lexmin_ptrupdate_fst-----
VERSION=cpack_align_ptrupdate_lexmin_ptrupdate_fst_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
command="$IEGEN examples/moldyn_full_cpack_align_ptrupdate_lexmin_ptrupdate_fst.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c"
echo $command
$command
exit_on_error $?

#-----cpack_align_ptrupdate_lexmin_ptrupdate_fst_spo-----
VERSION=cpack_align_ptrupdate_lexmin_ptrupdate_fst_spo_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
command="$IEGEN examples/moldyn_full_cpack_align_ptrupdate_lexmin_ptrupdate_fst_sparseloop.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c"
echo $command
$command
exit_on_error $?
