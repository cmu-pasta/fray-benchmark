#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=groovy4
class_to_run=groovy.servlet.Groovy6456
run $*
