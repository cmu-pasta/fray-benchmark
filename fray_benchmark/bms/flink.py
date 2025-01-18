import os
import subprocess

from .benchmark_base import UnitTestBenchmark
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases


class FlinkBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.target_dir = os.path.join(ARTIFACTS_PATH, "flink")
        super().__init__(
            "flink",
            [
                os.path.join(self.target_dir, "flink-runtime/target/flink-runtime-2.0-SNAPSHOT-tests.jar"),
                os.path.join(self.target_dir, "flink-runtime/target/flink-runtime-2.0-SNAPSHOT.jar"),
                os.path.join(self.target_dir,
                             "flink-runtime/target/dependency/*.jar"),
            ], load_test_cases(os.path.join(ASSETS_PATH, "flink.txt")),
            {},
            False)

    def build(self) -> None:
        subprocess.call([
            "./mvnw",
            "package",
            "-DskipTests",
        ], cwd=self.target_dir)
        subprocess.call([
            "../mvnw",
            "jar:jar",
        ], cwd=os.path.join(self.target_dir, "flink-runtime"))
        subprocess.call([
            "../mvnw",
            "jar:test-jar",
        ], cwd=os.path.join(self.target_dir, "flink-runtime"))
        subprocess.call([
            "../mvnw",
            "dependency:copy-dependencies",
            "-DincludeScope=test",
        ], cwd=os.path.join(self.target_dir, "flink-runtime"))
