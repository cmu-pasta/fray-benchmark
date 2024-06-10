#!/bin/bash
source $(cd `dirname $0`; pwd)/jacontebe.sh

test_name=jdk6_9
class_to_run=Test6648001
Opt="-ea:sun.net.www.protocol.http.AuthenticationInfo -Dhttp.auth.serializeRequests=true"
run $*
