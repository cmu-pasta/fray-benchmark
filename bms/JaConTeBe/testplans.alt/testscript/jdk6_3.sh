#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=jdk6_3
class_to_run=asm.LoggerModifier
run

class_to_run=Test4779253
Opt="-Xbootclasspath/p:classes"
run $*

#remove generated "classes" directory
rm -rf classes
