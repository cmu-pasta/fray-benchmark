#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=dbcp3
class_to_run=org.apache.commons.dbcp.datasources.Dbcp369
run $*
