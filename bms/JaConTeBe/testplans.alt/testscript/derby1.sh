#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=derby1
class_to_run=Derby4129
run $*
#delete generated files
rm -rf DB
rm derby.log
