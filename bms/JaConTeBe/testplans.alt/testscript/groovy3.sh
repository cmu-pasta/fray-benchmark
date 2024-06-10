#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=groovy3
class_to_run=Groovy5198
run $*
