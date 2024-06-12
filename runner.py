#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os

dependencies = []
command = [
    "/Users/aoli/repos/sfuzz/jdk/build/java-inst/bin/java",
    #  "-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=*:5005",
    "-javaagent:/Users/aoli/repos/sfuzz/junit-analyzer/build/libs/junit-analyzer-1.0-SNAPSHOT-all.jar",
    "-jar",
    "/Users/aoli/Downloads/junit-platform-console-standalone-1.10.2.jar",
    "execute", 
    "-cp",
    "./target/guava-tests-HEAD-jre-SNAPSHOT-tests.jar",
    #  "--scan-classpath"
    "-m",
    "com.google.common.util.concurrent.GeneratedMonitorTest#waitForUninterruptibly(nonfair)(+oo)/UnsatisfiedAndInterruptedBeforeWaiting->Hang",
    "--details=verbose"

]

dependency_dir = "./target/dependency"
for f in os.listdir(dependency_dir):
    print(f)
    dependencies.append(f)
    command.append("-cp")
    command.append(os.path.join(dependency_dir, f))


subprocess.call(
    command
)
