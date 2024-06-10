#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=groovy2
class_to_run=Groovy4736
run $*

rm -rf test