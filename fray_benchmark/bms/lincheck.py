#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

from .benchmark_base import MainMethodBenchmark
from ..commons import FRAY_PATH
from ..utils import load_test_cases


class LinCheckBenchmark(MainMethodBenchmark):
    def __init__(self) -> None:
        self.bench_dir = os.path.join(FRAY_PATH, "integration-tests")
        super().__init__(
            "lincheck",
            [
                os.path.join(self.bench_dir, "build/libs/*.jar"),
                os.path.join(self.lucene_dir,
                             "lucene/core/build/dependency/*.jar"),
            ],
            load_test_cases(os.path.join(ASSETS_PATH, "lincheck.txt")),
            {}
        )

    def build(self) -> None:
        subprocess.call([
            "./gradlew",
            "jar",
        ], cwd=os.path.join(self.bench_dir, ".."))
        subprocess.call([
            "./gradlew",
            "testJar",
        ], cwd=os.path.join(self.bench_dir, ".."))
        subprocess.call([
            "./gradlew",
            "copyDependencies",
        ], cwd=os.path.join(self.bench_dir, ".."))
