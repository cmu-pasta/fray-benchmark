#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=groovy1
class_to_run=Groovy3495
run $*
