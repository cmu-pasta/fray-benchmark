#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=derby5
class_to_run=org.apache.derby.impl.store.raw.data.Derby5447
run $*

