#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import List, Iterator, Tuple, Dict
from sys import platform
import re


from ..commons import FRAY_PATH, RR_PATH, JPF_PATH, HELPER_PATH, PERF_ITER, FRAY_VERSION
from ..utils import resolve_classpaths
from ..objects.execution_config import RunConfig, Executor


class BenchmarkBase(object):

    def __init__(self, name: str) -> None:
        self.name = name

    def build(self) -> None:
        pass

    def generate_java_test_commands(self, config: List[str], out_dir: str, timeout: int, perf_mode: bool) -> Iterator[Tuple[List[str], str, str]]:
        test_index = 0
        for config_data in self.get_test_cases("java"):
            log_path = f"{out_dir}/{test_index}"
            os.makedirs(log_path, exist_ok=True)
            with open(f"{log_path}/config.json", "w") as f:
                f.write(config_data.to_json())
            test_index += 1
            command = [
                "time",
                "-p",
                "-o",
                f"{log_path}/time.txt",
                "timeout",
                "--signal=SIGTERM",
                "--kill-after=2s",
                str(timeout + 10),
                # "taskset",
                # "-c",
                # str(test_index - 1),
                f"{FRAY_PATH}/result/java-inst-jdk21/bin/java",
                "-ea",
                f"-agentpath:{FRAY_PATH}/result/native-libs/libjvmti.so",
                f"-javaagent:{FRAY_PATH}/result/libs/fray-instrumentation-agent-{FRAY_VERSION}.jar",
                "--add-opens", "java.base/java.lang=ALL-UNNAMED",
                "--add-opens", "java.base/java.util=ALL-UNNAMED",
                "--add-opens", "java.base/java.io=ALL-UNNAMED",
                "--add-opens", "java.base/java.util.concurrent.atomic=ALL-UNNAMED",
                "--add-opens", "java.base/sun.nio.ch=ALL-UNNAMED",
                "--add-opens", "java.base/java.lang.reflect=ALL-UNNAMED",
                "-cp", ":".join(resolve_classpaths([
                    f"{FRAY_PATH}/result/libs/fray-core-{FRAY_VERSION}.jar",
                ])),
                "org.pastalab.fray.core.MainKt",
                "--run-config",
                "json",
                "--config-path",
                f"{log_path}/config.json",
                "-o", f"{log_path}/report",
                "--iter", "-1",
                "--timeout", str(timeout),
                *config
            ]
            if perf_mode:
                command.append("--explore")
            command.extend(["--iter", "-1"])
            command.append("--no-fray")
            yield command, log_path, FRAY_PATH

    def generate_rr_test_commands(self, out_dir: str, timeout: int, perf_mode: bool) -> Iterator[Tuple[List[str], str, str]]:
        test_index = 0
        java21_path = os.environ.get("JDK21_HOME", "/usr/lib/jvm/java-21-openjdk-amd64")
        for config_data in self.get_test_cases("rr"):
            log_path = f"{out_dir}/{test_index}"
            test_index += 1
            os.makedirs(log_path, exist_ok=True)
            with open(f"{log_path}/config.json", "w") as f:
                f.write(config_data.to_json())
            command = [f"{java21_path}/bin/java", "-ea"]
            if self.name != "jacontebe":
                command.append(f"-javaagent:{HELPER_PATH}/assertion-handler-agent/AssertionHandlerAgent.jar")
            command.extend(["--add-opens", "java.base/java.lang=ALL-UNNAMED"])
            command.extend(["--add-opens", "java.base/java.util=ALL-UNNAMED"])
            command.extend(["--add-opens", "java.base/java.io=ALL-UNNAMED"])
            command.extend(["--add-opens", "java.base/java.util.concurrent=ALL-UNNAMED"])
            command.extend(["--add-opens", "java.base/java.util.concurrent.atomic=ALL-UNNAMED"])
            command.extend(["--add-opens", "java.base/java.lang.reflect=ALL-UNNAMED"])
            command.extend([f"-cp", ':'.join(config_data.executor.classpaths)])
            for property_key, property_value in config_data.executor.properties.items():
                command.append(f"-D{property_key}={property_value}")
            command.append(config_data.executor.clazz)
            command.extend(config_data.executor.args)


            prefix = [
                "/usr/bin/env",
                "time",
                "-p",
                "-o",
                f"{log_path}/time.txt",
                "timeout",
                "-s",
                "INT",
                str(timeout),
                f"{HELPER_PATH}/rr_runner.sh"]
            if perf_mode:
                prefix.append("-e")
            command = prefix + [
                f"{log_path}/trace",
                "./build/bin/rr", "record", "--chaos", "-o", f"{log_path}/trace"] + command
            yield command, log_path, RR_PATH

    def generate_jpf_test_commands(self, out_dir: str, timeout: int, perf_mode: bool) -> Iterator[Tuple[List[str], str, str]]:
        test_index = 0
        java11_path = os.environ.get("JDK11_HOME", "/usr/lib/jvm/java-11-openjdk-amd64")
        for config_data in self.get_test_cases("jpf"):
            log_path = f"{out_dir}/{test_index}"
            test_index += 1
            os.makedirs(log_path, exist_ok=True)
            with open(f"{log_path}/config.json", "w") as f:
                f.write(config_data.to_json())
            command = [
                "time",
                "-p",
                "-o",
                f"{log_path}/time.txt",
                "timeout",
                "-s",
                "INT",
                str(timeout),
                java11_path + "/bin/java",
                "-Xmx1024m", "-ea",
                "--add-opens", "java.base/jdk.internal.misc=ALL-UNNAMED",
                "-jar",
                JPF_PATH + "/build/RunJPF.jar",
                ]
            if perf_mode:
                command.append("+search.multiple_errors=true")
            command.append("+search.class=gov.nasa.jpf.search.RandomSearch")
            command.append("+search.RandomSearch.path_limit=10000000")
            command.append("+cg.randomize_choices=FIXED_SEED")
            command.append("+report.console.property_violation=error,statistics")
            command.append(f"+cg.seed={test_index}")
            command.append(f"+classpath={':'.join(config_data.executor.classpaths)}")
            command.append(config_data.executor.clazz)
            command.extend(config_data.executor.args)
            command = {
                "command": command,
                "env": {
                    "JAVA_HOME": os.environ.get("JDK11_HOME", "/usr/lib/jvm/java-11-openjdk-amd64"),
                    # "JVM_FLAGS": "-Xmx1024m -ea --add-opens java.base/jdk.internal.misc=ALL-UNNAMED"
                }
            }
            yield command, log_path, JPF_PATH

    def generate_fray_stats_collector_commands(self, out_dir: str) -> Iterator[Tuple[List[str], str, str]]:
        test_index = 0
        for config_data in self.get_test_cases("fray-stat"):
            log_path = f"{out_dir}/{test_index}"
            os.makedirs(log_path, exist_ok=True)
            with open(f"{log_path}/config.json", "w") as f:
                f.write(config_data.to_json())
            test_index += 1
            command = [
                f"java",
                "-ea",
                f"-javaagent:/home/aoli/lib/jacocoagent.jar=destfile=/home/aoli/tmp/jacoco2.exec",
                "--add-opens", "java.base/java.lang=ALL-UNNAMED",
                "--add-opens", "java.base/java.util=ALL-UNNAMED",
                "--add-opens", "java.base/java.io=ALL-UNNAMED",
                "--add-opens", "java.base/java.util.concurrent.atomic=ALL-UNNAMED",
                "--add-opens", "java.base/sun.nio.ch=ALL-UNNAMED",
                "--add-opens", "java.base/java.lang.reflect=ALL-UNNAMED",
            ]
            command.extend([f"-cp", ':'.join(config_data.executor.classpaths)])
            for property_key, property_value in config_data.executor.properties.items():
                command.append(f"-D{property_key}={property_value}")
            command.append(config_data.executor.clazz)
            command.extend(config_data.executor.args)
            command.append("true")
            yield command, log_path, FRAY_PATH


    def generate_lincheck_test_commands(self, config: List[str], out_dir: str, timeout: int, perf_mode: bool) -> Iterator[Tuple[List[str], str, str]]:
        test_index = 0
        for config_data in self.get_test_cases("fray"):
            log_path = f"{out_dir}/{test_index}"
            os.makedirs(log_path, exist_ok=True)
            with open(f"{log_path}/config.json", "w") as f:
                f.write(config_data.to_json())
            test_index += 1
            command = [
                "time",
                "-p",
                "-o",
                f"{log_path}/time.txt",
                "timeout",
                "-s",
                "INT",
                str(timeout + 120),
                f"{FRAY_PATH}/instrumentation/jdk/build/java-inst/bin/java",
                "-ea",
                "-Xmx4g",
                f"-agentpath:{FRAY_PATH}/jvmti/build/native-libs/libjvmti.so",
                f"-javaagent:{FRAY_PATH}/instrumentation/agent/build/libs/fray-instrumentation-agent-{FRAY_VERSION}.jar",
                "--add-opens", "java.base/java.lang=ALL-UNNAMED",
                "--add-opens", "java.base/java.util=ALL-UNNAMED",
                "--add-opens", "java.base/java.io=ALL-UNNAMED",
                "--add-opens", "java.base/java.util.concurrent.atomic=ALL-UNNAMED",
                "--add-opens", "java.base/sun.nio.ch=ALL-UNNAMED",
                "--add-opens", "java.base/java.lang.reflect=ALL-UNNAMED",
                "-cp", ":".join(resolve_classpaths([
                    f"{FRAY_PATH}/core/build/libs/fray-core-{FRAY_VERSION}.jar",
                    f"{FRAY_PATH}/junit/build/libs/fray-junit-{FRAY_VERSION}.jar",
                    f"{FRAY_PATH}/core/build/dependency/*.jar",
                    f"{FRAY_PATH}/junit/build/dependency/*.jar",
                ])),
                "org.pastalab.fray.core.MainKt",
                "--run-config",
                "json",
                "--config-path",
                f"{log_path}/config.json",
                "-o", f"{log_path}/report",
                "--iter", "-1",
                "--timeout", str(timeout),
                *config
            ]
            if perf_mode:
                command.append("--explore")
            command.extend(["--iter", "-1"])
            yield command, log_path, FRAY_PATH



    def generate_fray_test_commands(self, config: List[str], out_dir: str, timeout: int, perf_mode: bool) -> Iterator[Tuple[List[str], str, str]]:
        test_index = 0
        for config_data in self.get_test_cases("fray"):
            log_path = f"{out_dir}/{test_index}"
            os.makedirs(log_path, exist_ok=True)
            with open(f"{log_path}/config.json", "w") as f:
                f.write(config_data.to_json())
            test_index += 1

            print(f"DEBUG: config_data.executor.classpaths has {len(config_data.executor.classpaths)} entries")
            resolved = resolve_classpaths(config_data.executor.classpaths)
            print(f"DEBUG: After resolve_classpaths: {len(resolved)} entries")
            print(f"DEBUG: First 10 entries: {resolved[:10]}")
            classpath_str = ":".join(resolved)

            command = [
                f"{FRAY_PATH}/result/bin/fray",
                "-cp",
                classpath_str,
            ]

            for key, value in config_data.executor.properties.items():
                command.append(f"-J-D{key}={value}")

            command.append("-J-Dnet.bytebuddy.experimental=true")
            command.append(config_data.executor.clazz)
            command.extend(config_data.executor.args)

            command.append("--")
            command.extend(config)
            command.extend(["--iter", "-1", "--sleep-as-yield"])
            command.extend(["-o", f"{log_path}/report"])

            if perf_mode:
                command.append("--explore")

            yield command, log_path, FRAY_PATH

    def get_test_cases(self, _tool_name: str) -> Iterator[RunConfig]:
        return iter([])

class SavedBenchmark:
    def __init__(self, path: str, index: int) -> None:
        self.new_index = index
        self.path = os.path.abspath(path)

    def load_command(self) -> List[str]:
        command = open(os.path.join(self.path, "command.txt")).read().strip()
        updated_command = re.sub(r"taskset -c \d+", f"taskset -c {self.new_index}", command)
        return updated_command.split(" ")

class MainMethodBenchmark(BenchmarkBase):
    def __init__(self, name: str, classpath: List[str], test_cases: List[str], properties: Dict[str, str]) -> None:
        super().__init__(name)
        self.test_cases = test_cases
        self.classpath = resolve_classpaths(classpath)
        self.properties = properties

    def get_test_cases(self, _tool_name: str) -> Iterator[RunConfig]:
        for test_case in self.test_cases:
            yield RunConfig(
                Executor(
                    test_case,
                    "main",
                    [],
                    self.classpath,
                    self.properties
                ),
                False,
                False,
                -1
            )


class UnitTestBenchmark(BenchmarkBase):
    def __init__(self, name: str, classpath: List[str], test_cases: List[str], properties: Dict[str, str], is_junit4: bool) -> None:
        super().__init__(name)
        self.test_cases = test_cases
        self.classpath = resolve_classpaths(classpath + [
            f"{HELPER_PATH}/junit-runner/build/libs/junit-runner-1.0-SNAPSHOT.jar",
            f"{HELPER_PATH}/junit-runner/build/dependency/*.jar",
        ])
        self.properties = properties
        self.is_junit4 = is_junit4

    def generate_collector_command(self) -> List[str]:
        command = [
            "java",  # Use system Java for test discovery (no instrumentation needed)
            f"-javaagent:{HELPER_PATH}/junit-analyzer/build/libs/junit-analyzer-all.jar",
            "--add-opens", "java.base/java.lang=ALL-UNNAMED",
            "--add-opens", "java.base/java.util=ALL-UNNAMED",
            "--add-opens", "java.base/java.io=ALL-UNNAMED",
            "--add-opens", "java.base/java.util.concurrent.atomic=ALL-UNNAMED",
            "--add-opens", "java.base/sun.nio.ch=ALL-UNNAMED",
            "--add-opens", "java.base/java.lang.reflect=ALL-UNNAMED",
            "-cp", f"{HELPER_PATH}/junit-analyzer/build/libs/junit-analyzer-all.jar",
            "org.junit.platform.console.ConsoleLauncher",
            "execute",
            "--scan-classpath",
        ] + sum([["-cp", cp] for cp in self.classpath], [])
        print(" ".join(command))
        return command


    def get_test_cases(self, _tool_name: str) -> Iterator[RunConfig]:
        for test_case in self.test_cases:
            yield RunConfig(
                Executor(
                    "org.pastalab.fray.helpers.JUnitRunner",
                    "main",
                    [
                        "junit4" if self.is_junit4 else "junit5",
                        f"{test_case}",
                    ],
                    self.classpath,
                    self.properties
                ),
                False,
                False,
                -1,
            )
