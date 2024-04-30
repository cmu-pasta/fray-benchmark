#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=derby2
class_to_run=Derby5560
run $*

