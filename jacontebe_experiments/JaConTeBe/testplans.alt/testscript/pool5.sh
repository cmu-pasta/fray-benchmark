#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=pool5

class_to_run=org.apache.commons.pool.Test46
run $*