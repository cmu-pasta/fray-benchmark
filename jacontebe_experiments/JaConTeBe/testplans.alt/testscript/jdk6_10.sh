#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=jdk6_10
class_to_run=Test6927486
run $*

rm file1
rm file2