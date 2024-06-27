#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from typing import List, Iterator, Tuple, Dict

from fray_benchmark.configs import FRAY_PATH
from ..utils import resolve_classpaths

class BenchmarkBase(object):

    def __init__(self, name: str) -> None:
        self.name = name

    def build(self) -> None:
        pass

    def generate_rr_test_commands(self, out_dir: str) -> Iterator[Tuple[List[str], str]]:
        test_index = 0
        for config_data in self.get_test_cases():
            log_path = f"{out_dir}/{test_index}"
            os.makedirs(log_path)
            json.dump(config_data, open(f"{log_path}/config.json", "w"), indent=4)
            command = ["java"]
            for classpath in config_data["executor"]["classpaths"]:
                command.extend(["-cp", classpath])
            for property_key, property_value in config_data["executor"]["properties"].items():
                command.extend(["-D", f"{property_key}={property_value}"])
            command.append(config_data["executor"]["clazz"])
            command.extend(config_data["executor"]["args"])
            yield command, log_path

    def generate_fray_test_commands(self, config: List[str], out_dir: str, debug_jvm:  bool) -> Iterator[Tuple[List[str], str, str]]:
        test_index = 0
        for config_data in self.get_test_cases():
            log_path = f"{out_dir}/{test_index}"
            os.makedirs(log_path)
            json.dump(config_data, open(f"{log_path}/config.json", "w"), indent=4)
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

    def get_test_cases(self, output_base: str) -> Iterator[Dict[str, str]]:
        return iter([])

    def get_extra_args(self) -> List[str]:
        return []

class MainMethodBenchmark(BenchmarkBase):
    def __init__(self, name: str, classpath: List[str], test_cases: List[str], properties: Dict[str, str]) -> None:
        super().__init__(name)
        self.test_cases = test_cases
        self.classpath = resolve_classpaths(classpath)
        self.properties = properties

    def get_test_cases(self) -> Iterator[Dict[str, str]]:
        for test_case in self.test_cases:
            yield {
                "executor": {
                    "clazz": test_case,
                    "method": "main",
                    "args": [],
                    "classpaths": self.classpath,
                    "properties": self.properties
                },
                "ignoreUnhandledExceptions": False,
                "timedOpAsYield": False,
                "interleaveMemoryOps": False,
                "maxScheduledStep": 1000000
            }


class UnitTestBenchmark(BenchmarkBase):
    def __init__(self, name: str, classpath: List[str], test_cases: List[str], properties: Dict[str, str]) -> None:
        super().__init__(name)
        self.test_cases = test_cases
        self.classpath = resolve_classpaths(classpath)
        self.properties = properties


    def get_test_cases(self) -> Iterator[Dict[str, str]]:
        for test_case in self.test_cases:
            yield {
                "executor": {
                    "clazz": "cmu.pasta.fray.examples.JUnitRunnerKt",
                    "method": "main",
                    "args": [
                        f"{test_case}",
                    ],
                    "classpaths": self.classpath,
                    "properties": self.properties
                },
                "ignoreUnhandledExceptions": False,
                "timedOpAsYield": False,
                "interleaveMemoryOps": False,
                "maxScheduledStep": 1000000
            }
