#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=jdk7_2

class_to_run=Test7122142
run $*

