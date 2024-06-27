#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

from .benchmark_base import MainMethodBenchmark
from ..configs import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases

class SCTBenchBenchmark(MainMethodBenchmark):
    def __init__(self) -> None:
        self.bench_dir = os.path.join(ARTIFACTS_PATH, "SCTBench")
        super().__init__(
            "sctbench",
            [
                os.path.join(self.bench_dir, "build/libs/*.jar"),
            ],
            load_test_cases(os.path.join(ASSETS_PATH, "sctbench.txt")),
            {}
            )

    def build(self) -> None:
        subprocess.call([
            "./gradlew",
            "jar",
        ], cwd=self.bench_dir)
