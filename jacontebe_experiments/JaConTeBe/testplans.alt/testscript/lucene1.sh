#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=lucene1

class_to_run='junit.textui.TestRunner  org.apache.lucene.index.Test2783'
run $*