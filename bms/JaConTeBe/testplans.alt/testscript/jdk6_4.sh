#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=jdk6_4
class_to_run=Test4813150
run $*
