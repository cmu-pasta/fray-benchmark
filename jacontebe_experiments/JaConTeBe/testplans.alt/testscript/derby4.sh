#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=derby4
class_to_run="org.junit.runner.JUnitCore  org.apache.derby.impl.services.reflect.Derby764"
run $*

