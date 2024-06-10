#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=jdk6_11
class_to_run=Test6934356
run $*
