#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=dbcp1
class_to_run=Dbcp65
run $*
