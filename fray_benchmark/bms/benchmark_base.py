#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import List, Iterator, Tuple, Dict
from sys import platform


from ..commons import FRAY_PATH, RR_PATH, JPF_PATH, HELPER_PATH, PERF_ITER
from ..utils import resolve_classpaths
from ..objects.execution_config import RunConfig, Executor


class BenchmarkBase(object):

    def __init__(self, name: str) -> None:
        self.name = name

    def build(self) -> None:
        pass

    def generate_rr_test_commands(self, out_dir: str, timeout: int, perf_mode: bool) -> Iterator[Tuple[List[str], str, str]]:
        test_index = 0
        for config_data in self.get_test_cases("rr"):
            log_path = f"{out_dir}/{test_index}"
            test_index += 1
            os.makedirs(log_path, exist_ok=True)
            with open(f"{log_path}/config.json", "w") as f:
                f.write(config_data.to_json())
            command = ["/usr/bin/java", "-ea", f"-javaagent:{HELPER_PATH}/assertion-handler-agent/AssertionHandlerAgent.jar"]
            command.extend(["--add-opens", "java.base/java.lang=ALL-UNNAMED"])
            command.extend(["--add-opens", "java.base/java.util=ALL-UNNAMED"])
            command.extend(["--add-opens", "java.base/java.io=ALL-UNNAMED"])
            command.extend(["--add-opens", "java.base/java.util.concurrent=ALL-UNNAMED"])
            command.extend(["--add-opens", "java.base/java.lang.reflect=ALL-UNNAMED"])
            command.extend([f"-cp", ':'.join(config_data.executor.classpaths)])
            for property_key, property_value in config_data.executor.properties.items():
                command.append(f"-D{property_key}={property_value}")
            command.append(config_data.executor.clazz)
            command.extend(config_data.executor.args)


            prefix = [
                "/usr/bin/time",
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
        for config_data in self.get_test_cases("jpf"):
            log_path = f"{out_dir}/{test_index}"
            test_index += 1
            os.makedirs(log_path, exist_ok=True)
            with open(f"{log_path}/config.json", "w") as f:
                f.write(config_data.to_json())
            command = [
                "/usr/bin/time",
                "-p",
                "-o",
                f"{log_path}/time.txt",
                "timeout",
                "-s",
                "INT",
                str(timeout),
                "./bin/jpf"]
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
                    # "JVM_FLAGS": "-Xmx1024m -ea --add-opens java.base/jdk.internal.misc=ALL-UNNAMED"
                }
            }
            yield command, log_path, JPF_PATH

    def generate_fray_test_commands(self, config: List[str], out_dir: str, timetout: int, perf_mode: bool) -> Iterator[Tuple[List[str], str, str]]:
        test_index = 0
        for config_data in self.get_test_cases("fray"):
            log_path = f"{out_dir}/{test_index}"
            os.makedirs(log_path, exist_ok=True)
            with open(f"{log_path}/config.json", "w") as f:
                f.write(config_data.to_json())
            test_index += 1
            command = [
                "/usr/bin/time",
                "-p",
                "-o",
                f"{log_path}/time.txt",
                "timeout",
                "-s",
                "INT",
                str(timetout),
                f"{FRAY_PATH}/jdk/build/java-inst/bin/java",
                "-ea",
                f"-agentpath:{FRAY_PATH}/jvmti/build//cmake/native_release/" + ("mac-aarch64/cpp/libjvmti.dylib" if platform == "darwin" else "linux-amd64/cpp/libjvmti.so"),
                f"-javaagent:{FRAY_PATH}/instrumentation/build/libs/instrumentation-1.0-SNAPSHOT-all.jar",
                "--add-opens", "java.base/java.lang=ALL-UNNAMED",
                "--add-opens", "java.base/java.util=ALL-UNNAMED",
                "--add-opens", "java.base/java.io=ALL-UNNAMED",
                "--add-opens", "java.base/java.util.concurrent.atomic=ALL-UNNAMED",
                "--add-opens", "java.base/sun.nio.ch=ALL-UNNAMED",
                "--add-opens", "java.base/java.lang.reflect=ALL-UNNAMED",
                "-cp", ":".join(resolve_classpaths([
                    f"{FRAY_PATH}/examples/build/dependency/*.jar",
                ])),
                "cmu.pasta.fray.core.MainKt",
                "--run-config",
                "json",
                "--config-path",
                f"{log_path}/config.json",
                "-o", f"{log_path}/report",
                "--logger", "json",
                "--iter", "-1",
                *config
            ]
            if perf_mode:
                command.append("--explore")
            command.extend(["--iter", "-1"])
            yield command, log_path, FRAY_PATH

    def get_test_cases(self, _tool_name: str) -> Iterator[RunConfig]:
        return iter([])

class SavedBenchmark:
    def __init__(self, path: str) -> None:
        self.path = os.path.abspath(path)

    def load_command(self) -> List[str]:
        return open(os.path.join(self.path, "command.txt")).read().strip().split(" ")

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
                False,
                -1
            )


class UnitTestBenchmark(BenchmarkBase):
    def __init__(self, name: str, classpath: List[str], test_cases: List[str], properties: Dict[str, str], is_junit4: bool) -> None:
        super().__init__(name)
        self.test_cases = test_cases
        self.classpath = resolve_classpaths(classpath + [
            f"{FRAY_PATH}/examples/build/libs/*.jar",
            f"{FRAY_PATH}/examples/build/dependency/*.jar",
        ])
        self.properties = properties
        self.is_junit4 = is_junit4

    def get_test_cases(self, _tool_name: str) -> Iterator[RunConfig]:
        for test_case in self.test_cases:
            yield RunConfig(
                Executor(
                    "cmu.pasta.fray.examples.JUnitRunner",
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
                False,
                -1,
            )