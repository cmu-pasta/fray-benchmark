#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=groovy6
class_to_run=org.codehaus.groovy.ast.Groovy4292
run $*
