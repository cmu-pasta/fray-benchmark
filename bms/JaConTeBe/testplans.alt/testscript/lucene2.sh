#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=lucene2

class_to_run=org.apache.lucene.Test1544
run $*

#delete generated files
rm -rf TestDoug2*
