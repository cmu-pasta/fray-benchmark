import os
import subprocess

from .benchmark_base import UnitTestBenchmark
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases

class Log4jBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.target_dir = os.path.join(ARTIFACTS_PATH, "ignite-3")
        super().__init__(
            "ignite",
            [
                os.path.join(
                    self.target_dir, "modules/sql-engine/build/libs/*.jar"
                ),
                os.path.join(
                    self.target_dir, "modules/sql-engine/build/classes/java/test"
                ),
                os.path.join(
                    self.target_dir, "modules/sql-engine/build/dependencies/*.jar"
                ),
            ], load_test_cases(os.path.join(ASSETS_PATH, "log4j.txt")),
            {},
            False)

    def build(self) -> None:
        subprocess.call([
            "git",
            "checkout",
            "."
        ], cwd=self.target_dir)
        subprocess.call([
            "git",
            "apply",
            os.path.join(ASSETS_PATH, "ignite.patch")
        ], cwd=self.target_dir)
        subprocess.call([
            "./gradlew",
            "jar",
        ], cwd=self.target_dir)
        subprocess.call([
            "./gradlew",
            "testJar",
        ], cwd=self.target_dir)
        subprocess.call([
            "./gradlew",
            "copyDependencies",
        ], cwd=self.target_dir)

