import os
import subprocess

from .benchmark_base import UnitTestBenchmark
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases


class KafkaCoreBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.bench_dir = os.path.join(ARTIFACTS_PATH, "kafka")
        super().__init__(
            "kafkacore",
            [
                os.path.join(self.bench_dir,
                             "core/build/libs/*.jar"),
                os.path.join(self.bench_dir,
                             "core/build/dependant-testlibs/*.jar"),
            ], load_test_cases(os.path.join(ASSETS_PATH, f"kafkacore.txt")),
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
            os.path.join(ASSETS_PATH, f"kafka.patch")
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
            "copyDependantTestLibs",
        ], cwd=self.bench_dir)
