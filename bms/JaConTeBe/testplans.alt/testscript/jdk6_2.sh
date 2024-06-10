#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=jdk6_2
class_to_run=Test4742723
run $*
