#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=log4j2

class_to_run=com.main.Test41214
run $*