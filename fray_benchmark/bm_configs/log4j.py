import os
import subprocess

from .benchmark_base import UnitTestBenchmark
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases

class Log4jBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.target_dir = os.path.join(ARTIFACTS_PATH, "logging-log4j2")
        super().__init__(
            "log4j",
            [
                os.path.join(
                    self.target_dir, "log4j-core-test/target/log4j-core-test-2.25.0-SNAPSHOT.jar"
                ),
                os.path.join(
                    self.target_dir, "log4j-core-test/target/test-classes/"
                ),
                os.path.join(
                    self.target_dir, "log4j-core-test/target/dependency/*.jar"
                ),
            ], load_test_cases(os.path.join(ASSETS_PATH, "log4j.txt")),
            {},
            False)

    def build(self) -> None:
        subprocess.call([
            "./mvnw",
            "install",
            "-DskipTests",
            "-Drat.skip=true",
        ], cwd=self.target_dir)
        subprocess.call([
            "./mvnw",
            "dependency:copy-dependencies",
        ], cwd=self.target_dir)

