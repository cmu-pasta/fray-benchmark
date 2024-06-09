#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=lucene1

class_to_run=org.apache.lucene.index.Test2783
run $*
