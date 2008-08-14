#!/usr/bin/env sh

#Simple script to update the svnignore property based on the file in misc/svnignore

#Steps:
#1) Update misc/svnignore with the files that should be ignored
#2) Run this script from the root of the project (iegen): ./misc/svnignore.sh
#3) Commit the changes to misc/svnignore and the properties on the directories: svn ci

svn propset svn:ignore -R -F misc/svnignore .
