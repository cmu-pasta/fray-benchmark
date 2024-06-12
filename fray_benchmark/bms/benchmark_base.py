#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import List, Iterator, Tuple
from ..utils import resolve_classpaths

class BenchmarkBase(object):

    def __init__(self, name: str) -> None:
        self.name = name

    def build(self) -> None:
        pass

    def generate_test_commands(self, config: List[str], out_dir: str, debug_jvm:  bool) -> Iterator[Tuple[List[str], str]]:
        test_index = 0
        for args in self.get_test_cases():
            log_path = f"{out_dir}/{test_index}"
            os.makedirs(log_path)
            args.extend([
                "-o", f"{out_dir}/{test_index}",
                "--logger", "json",
                "--iter", "-1",
                "-s", "10000000"
                ])
            args.extend(config)
            test_index += 1
            command = [
                "./gradlew",
                "runFray",
                f"-PtestClass=org.junit.platform.console.ConsoleLauncher",
                f"-PtestMethod=main",
                f"-PextraArgs={' '.join(args)}",
            ]
            if debug_jvm:
                command.append("--debug-jvm")
            yield command, log_path

    def get_test_cases(self, output_base: str) -> Iterator[List[str]]:
        return iter([])

    def get_extra_args(self) -> List[str]:
        return []

class UnitTestBenchmark(BenchmarkBase):
    def __init__(self, name: str, classpath: List[str], test_cases: List[str]) -> None:
        super().__init__(name)
        self.test_cases = test_cases
        self.classpath = ';'.join(map(lambda cp: f"-cp;{cp}", resolve_classpaths(classpath)))

    def get_test_cases(self) -> Iterator[List[str]]:
        for test_case in self.test_cases:
            yield [
                "-a", f"execute;-m;{test_case};{self.classpath}",
                ]