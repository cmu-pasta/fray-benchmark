#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=log4j4

class_to_run=org.apache.log4j.Test38137
run $*