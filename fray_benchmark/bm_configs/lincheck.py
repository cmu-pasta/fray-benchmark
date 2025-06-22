#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
from typing import Iterator

from fray_benchmark.objects.execution_config import RunConfig

from .benchmark_base import MainMethodBenchmark
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases


class LinCheckBenchmark(MainMethodBenchmark):
    def __init__(self) -> None:
        self.bench_dir = os.path.join(ARTIFACTS_PATH, "licheck")
        super().__init__(
            "lincheck",
            [
                os.path.join(self.bench_dir, "build/classes/java/main/"),
                os.path.join(self.bench_dir, "build/classes/java/test/"),
                os.path.join(self.bench_dir, "build/classes/kotlin/test/"),
                os.path.join(self.bench_dir,
                             "build/dependency/*.jar"),
            ],
            load_test_cases(os.path.join(ASSETS_PATH, "lincheck.txt")),
            {}
        )

    def build(self) -> None:
        subprocess.call([
            "./gradlew",
            "jar",
        ], cwd=self.bench_dir)
        subprocess.call([
            "./gradlew",
            "build",
        ], cwd=self.bench_dir)
        subprocess.call([
            "./gradlew",
            "copyDependencies",
        ], cwd=self.bench_dir)

    def get_test_cases(self, _tool_name: str) -> Iterator[RunConfig]:
        for test_case in super().get_test_cases(_tool_name):
            if "CATreeTest" in test_case.executor.clazz:
                test_case.max_scheduled_step = 100000
            if "LogicalOrderingAVL" in test_case.executor.clazz:
                test_case.max_scheduled_step = 10000
            yield test_case
