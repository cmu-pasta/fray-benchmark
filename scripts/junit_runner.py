#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os

# target_dir = "/Users/aoli/repos/fray-benchmark/bms/kafka-new/build"
target_dir = "/Users/aoli/repos/fray-benchmark/bms/flink/flink-runtime/target"
#  target_dir = "/Users/aoli/repos/sfuzz-benchmark/bms/solr/solr/core/build"
# target_dir = "/Users/aoli/repos/sfuzz-benchmark/bms/commons-lang/target"
#  target_dir = "/Users/aoli/repos/sfuzz-benchmark/bms/guava/guava-tests/target"
#  target_dir = "/Users/aoli/repos/sfuzz-benchmark/bms/lucene/lucene/core/build/"

dependencies = []
command = [
    "/Users/aoli/repos/fray/instrumentation/jdk/build/java-inst/bin/java",
     #  "java",
    "-ea",
    #  "-Djunit.jupiter.execution.parallel.enabled=true",
    #  "-Djunit.jupiter.execution.parallel.mode.default=concurrent",
    # "-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=*:5005",
    "-javaagent:/Users/aoli/repos/fray-benchmark/helpers/junit-analyzer/build/libs/junit-analyzer-all.jar",
    "--add-opens", "java.base/java.lang=ALL-UNNAMED",
    "--add-opens", "java.base/java.util.concurrent.atomic=ALL-UNNAMED",
    "--add-opens", "java.base/java.util=ALL-UNNAMED",
    "--add-opens", "java.base/java.io=ALL-UNNAMED",
    "--add-opens", "java.base/sun.nio.ch=ALL-UNNAMED",
    "-cp",
    "/Users/aoli/repos/fray-benchmark/helpers/junit-analyzer/build/libs/junit-analyzer-all.jar",
    "org.junit.platform.console.ConsoleLauncher",
    "execute",
    #  "-cp",
    #  f"{target_dir}/classes/java/test/",
    #  "-cp",
    #  f"{target_dir}/resources/test/",
    "-cp",
    f"{target_dir}/flink-runtime-2.0-SNAPSHOT-tests.jar",
    "-cp",
    f"{target_dir}/flink-runtime-2.0-SNAPSHOT.jar",
    # storage/api/build/libs/*.jar
    # f"{target_dir}/commons-lang3-3.15.0-SNAPSHOT-tests.jar",
    #  f"{target_dir}/libs/lucene-core-10.0.0-SNAPSHOT-test.jar",
    #  f"{target_dir}/guava-tests-HEAD-jre-SNAPSHOT.jar",
    #  f"{target_dir}/libs/lucene-core-10.0.0-SNAPSHOT.jar",
    "--scan-classpath",
    "--include-classname",
    "org.apache.flink.*",
    "--exclude-classname",
    "org.apache.flink.runtime.jobmaster.JobRecoveryITCase",
    # "--include-tag=flaky",
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
