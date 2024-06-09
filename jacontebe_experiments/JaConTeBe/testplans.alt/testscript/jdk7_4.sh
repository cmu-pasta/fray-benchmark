#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=jdk7_4

class_to_run=Test8010939
run $*

