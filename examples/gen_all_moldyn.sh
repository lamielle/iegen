#!/usr/bin/env sh

./waf install

IEGEN=./iegen/bin/iegen

OUT_DIR=$HOME/RTRTcode/trunk/src/drivers/moldyn

#-----no_trans-----
VERSION=notrans_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
$IEGEN examples/moldyn_full.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c

#-----cpack_only-----
VERSION=cpack_only_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
$IEGEN examples/moldyn_full_cpack_only.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c

#-----cpack_align-----
VERSION=cpack_align_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
$IEGEN examples/moldyn_full_cpack_align.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c

#-----cpack_align_ptrupdate-----
VERSION=cpack_align_ptrupdate_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
$IEGEN examples/moldyn_full_cpack_align_ptrupdate.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c

#-----cpack_align_ptrupdate_lexmin-----
VERSION=cpack_align_ptrupdate_lexmin_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
$IEGEN examples/moldyn_full_cpack_align_ptrupdate_lexmin.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c

#-----cpack_align_ptrupdate_lexmin_ptrupdate-----
VERSION=cpack_align_ptrupdate_lexmin_ptrupdate_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
$IEGEN examples/moldyn_full_cpack_align_ptrupdate_lexmin_ptrupdate.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c

#-----cpack_align_ptrupdate_lexmin_ptrupdate_fst-----
VERSION=cpack_align_ptrupdate_lexmin_ptrupdate_fst_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
$IEGEN examples/moldyn_full_cpack_align_ptrupdate_lexmin_ptrupdate_fst.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c

#-----cpack_align_ptrupdate_lexmin_ptrupdate_fst_spo-----
VERSION=cpack_align_ptrupdate_lexmin_ptrupdate_fst_spo_gen
echo
echo "-----Generating version ${VERSION}-----"
echo
$IEGEN examples/moldyn_full_cpack_align_ptrupdate_lexmin_ptrupdate_fst_sparseloop.spec --inspector-name=inspector_${VERSION} --executor-name=executor_${VERSION} -o $OUT_DIR/moldyn_full_${VERSION}.c
