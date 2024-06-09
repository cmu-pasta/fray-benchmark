#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=derby3
class_to_run=Derby5561
run $*

