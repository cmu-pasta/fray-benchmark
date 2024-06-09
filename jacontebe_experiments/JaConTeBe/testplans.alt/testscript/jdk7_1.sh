#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=jdk7_1

class_to_run=Test7045594
run $*

