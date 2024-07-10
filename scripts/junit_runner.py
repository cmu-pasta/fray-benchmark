#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os

target_dir = "/Users/aoli/repos/sfuzz-benchmark/bms/kafka/streams/build"
#  target_dir = "/Users/aoli/repos/sfuzz-benchmark/bms/solr/solr/core/build"
# target_dir = "/Users/aoli/repos/sfuzz-benchmark/bms/commons-lang/target"
#  target_dir = "/Users/aoli/repos/sfuzz-benchmark/bms/guava/guava-tests/target"
#  target_dir = "/Users/aoli/repos/sfuzz-benchmark/bms/lucene/lucene/core/build/"

dependencies = []
command = [
    "/Users/aoli/repos/sfuzz/jdk/build/java-inst/bin/java",
     #  "java",
    "-ea",
    #  "-Djunit.jupiter.execution.parallel.enabled=true",
    #  "-Djunit.jupiter.execution.parallel.mode.default=concurrent",
    #  "-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=*:5005",
    "-javaagent:/Users/aoli/repos/sfuzz/junit-analyzer/build/libs/junit-analyzer-1.0-SNAPSHOT-all.jar",
    "--add-opens", "java.base/java.lang=ALL-UNNAMED",
    "--add-opens", "java.base/java.util.concurrent.atomic=ALL-UNNAMED",
    "--add-opens", "java.base/java.util=ALL-UNNAMED",
    "--add-opens", "java.base/java.io=ALL-UNNAMED",
    "--add-opens", "java.base/sun.nio.ch=ALL-UNNAMED",
    "-jar",
    "/Users/aoli/Downloads/junit-platform-console-standalone-1.10.2.jar",
    "execute",
    #  "-cp",
    #  f"{target_dir}/classes/java/test/",
    #  "-cp",
    #  f"{target_dir}/resources/test/",
    "-cp",
    f"{target_dir}/libs/kafka-streams-3.9.0-SNAPSHOT-test.jar",
    "-cp",
    f"{target_dir}/libs/kafka-streams-3.9.0-SNAPSHOT.jar",
    # f"{target_dir}/commons-lang3-3.15.0-SNAPSHOT-tests.jar",
    #  f"{target_dir}/libs/lucene-core-10.0.0-SNAPSHOT-test.jar",
    #  f"{target_dir}/guava-tests-HEAD-jre-SNAPSHOT.jar",
    #  f"{target_dir}/libs/lucene-core-10.0.0-SNAPSHOT.jar",
    "--scan-classpath",
    "--include-classname",
    "org.apache.kafka.streams.*",
    #  "--disable-banner",
    #  "--disable-ansi-colors",
    #  "-m",
    #  "org.apache.solr.schema.TestBulkSchemaConcurrent#test"
]

dependency_dir = f"{target_dir}/dependency"
for f in os.listdir(dependency_dir):
    print(f)
    dependencies.append(f)
    command.append("-cp")
    command.append(os.path.join(dependency_dir, f))

subprocess.call(
    command, 
)
