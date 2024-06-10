#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=jdk7_3
class_to_run=asm.FutureTaskModifier
run

class_to_run=Test7132378
Opt="-Xbootclasspath/p:classes"
run $*

#remove generated "classes" directory
rm -rf classes
