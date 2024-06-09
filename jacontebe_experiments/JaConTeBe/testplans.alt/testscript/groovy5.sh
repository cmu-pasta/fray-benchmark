#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=groovy5
class_to_run=groovy.util.Groovy6068
run $*
