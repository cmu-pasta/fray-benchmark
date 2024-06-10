#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=jdk6_7
class_to_run=Test6582568
run $*
