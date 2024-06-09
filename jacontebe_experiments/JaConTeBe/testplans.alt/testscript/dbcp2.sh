#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=dbcp2
class_to_run=Dbcp270
run $*
