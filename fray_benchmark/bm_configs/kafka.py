import os
import subprocess

from .benchmark_base import UnitTestBenchmark
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases


class KafkaBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.bench_dir = os.path.join(ARTIFACTS_PATH, "kafka")
        super().__init__(
            "kafka",
            [
                os.path.join(self.bench_dir, "streams/build/classes/java/main/"),
                os.path.join(self.bench_dir, "streams/build/classes/java/test/"),
                os.path.join(self.bench_dir, "streams/build/resources/test/"),
                os.path.join(self.bench_dir, "streams/build/resources/main/"),
                os.path.join(self.bench_dir,
                             "streams/build/dependency/*.jar"),
            ], load_test_cases(os.path.join(ASSETS_PATH, f"kafka.txt")),
            {
            },
            False)

    def build(self) -> None:
        subprocess.call([
            "git",
            "checkout",
            "."
        ], cwd=self.bench_dir)
        subprocess.call([
            "git",
            "apply",
            os.path.join(ASSETS_PATH, f"{self.name}.patch")
        ], cwd=self.bench_dir)
        subprocess.call([
            "./gradlew",
            "testJar",
        ], cwd=self.bench_dir)
        subprocess.call([
            "./gradlew",
            "jar",
        ], cwd=self.bench_dir)
        subprocess.call([
            "./gradlew",
            "copyDependencies",
        ], cwd=self.bench_dir)
