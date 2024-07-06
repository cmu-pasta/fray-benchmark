#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from typing import List, Iterator, Tuple, Dict

from ..commons import FRAY_PATH, RR_PATH, JPF_PATH, HELPER_PATH
from ..utils import resolve_classpaths
from ..objects.execution_config import RunConfig, Executor


class BenchmarkBase(object):

    def __init__(self, name: str) -> None:
        self.name = name

    def build(self) -> None:
        pass

    def generate_rr_test_commands(self, out_dir: str) -> Iterator[Tuple[List[str], str, str]]:
        test_index = 0
        for config_data in self.get_test_cases():
            log_path = f"{out_dir}/{test_index}"
            test_index += 1
            os.makedirs(log_path, exist_ok=True)
            with open(f"{log_path}/config.json", "w") as f:
                f.write(config_data.to_json())
            command = ["java", "-ea", f"-javaagent:{HELPER_PATH}/assertion-handler-agent/AssertionHandlerAgent.jar"]
            command.extend([f"-cp", ':'.join(config_data.executor.classpaths)])
            for property_key, property_value in config_data.executor.properties.items():
                command.extend(["-D", f"{property_key}={property_value}"])
            command.append(config_data.executor.clazz)
            command.extend(config_data.executor.args)
            command = ["./build/bin/rr", "record", "--chaos", "-o", f"{log_path}/trace"] + command
            yield command, log_path, RR_PATH

    def generate_jpf_test_commands(self, out_dir: str) -> Iterator[Tuple[List[str], str, str]]:
        test_index = 0
        for config_data in self.get_test_cases():
            log_path = f"{out_dir}/{test_index}"
            test_index += 1
            os.makedirs(log_path, exist_ok=True)
            with open(f"{log_path}/config.json", "w") as f:
                f.write(config_data.to_json())
            command = ["./bin/jpf"]
            command.append(f"+classpath={':'.join(config_data.executor.classpaths)}")
            command.append(config_data.executor.clazz)
            command.extend(config_data.executor.args)
            yield command, log_path, JPF_PATH

    def generate_fray_test_commands(self, config: List[str], out_dir: str, debug_jvm:  bool) -> Iterator[Tuple[List[str], str, str]]:
        test_index = 0
        for config_data in self.get_test_cases():
            log_path = f"{out_dir}/{test_index}"
            os.makedirs(log_path, exist_ok=True)
            with open(f"{log_path}/config.json", "w") as f:
                f.write(config_data.to_json())
            args = [
                "-o", f"{log_path}/report",
                "--logger", "json",
                "--iter", "-1",
            ]
            args.extend(config)
            test_index += 1
            command = [
                "./gradlew",
                "runFray",
                f"-PconfigPath={log_path}/config.json",
                f"-PextraArgs={' '.join(args)}",
            ]
            if debug_jvm:
                command.append("--debug-jvm")
            yield command, log_path, FRAY_PATH

    def get_test_cases(self) -> Iterator[RunConfig]:
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

    def get_test_cases(self) -> Iterator[RunConfig]:
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
                1000000
            )


class UnitTestBenchmark(BenchmarkBase):
    def __init__(self, name: str, classpath: List[str], test_cases: List[str], properties: Dict[str, str], is_junit4: bool) -> None:
        super().__init__(name)
        self.test_cases = test_cases
        self.classpath = resolve_classpaths(classpath)
        self.properties = properties
        self.is_junit4 = is_junit4

    def get_test_cases(self) -> Iterator[RunConfig]:
        for test_case in self.test_cases:
            yield RunConfig(
                Executor(
                    "cmu.pasta.fray.examples.JUnitRunnerKt",
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
                1000000
            )