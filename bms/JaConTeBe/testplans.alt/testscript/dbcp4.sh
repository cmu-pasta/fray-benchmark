#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=dbcp4
class_to_run=org.apache.commons.dbcp.Dbcp271
run $*
