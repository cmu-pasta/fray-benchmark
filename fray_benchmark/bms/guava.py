#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
from .benchmark_base import UnitTestBenchmark
from ..configs import ARTIFACTS_PATH

class GuavaBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.guava_test_dir = os.path.join(ARTIFACTS_PATH, "guava/guava-tests")
        super().__init__(
            "guava",
            [
                os.path.join(self.guava_test_dir, "target/guava-tests-HEAD-jre-SNAPSHOT-tests.jar"),
                os.path.join(self.guava_test_dir, "target/dependency/*.jar"),
            ], [
                "com.google.common.cache.CacheLoadingTest#testConcurrentLoading"
                # "com.google.common.hash.BloomFilterTest#testNoRaceConditions",
                # "com.google.common.util.concurrent.ExecutionListTest#testExecute_idempotentConcurrently",
            ])

    def build(self) -> None:
        subprocess.call([
            "../mvnw",
            "dependency:copy-dependencies"
        ], cwd=self.guava_test_dir)
        subprocess.call([
            "../mvnw",
            "-DskipTests",
            "package"
        ], cwd=self.guava_test_dir)
