#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=log4j3

class_to_run=org.apache.log4j.helpers.Test54325
run $*