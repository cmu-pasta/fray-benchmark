#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

mkdir -p classes/edu/illinois/jacontebe/globalevent
#This class is compiled when install.sh was run.
cp source/edu/illinois/jacontebe/globalevent/GlobalDriver.class classes/edu/illinois/jacontebe/globalevent/GlobalDriver.class
test_name=jdk7_6
class_to_run=asm.ActivationModifier
run

class_to_run=Test8023541
Opt='-Xbootclasspath/p:classes -Djava.security.policy=source/security.policy'
run $*

#remove generated "classes" directory
rm -rf classes
rm -rf implcb
