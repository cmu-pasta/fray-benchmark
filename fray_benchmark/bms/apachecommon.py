import os
import subprocess

from .benchmark_base import UnitTestBenchmark
from ..configs import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases

class ApacheCommonBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.bench_dir = os.path.join(ARTIFACTS_PATH, "commons-lang")
        super().__init__(
            "apachecommon",
            [
                os.path.join(self.bench_dir, "target/commons-lang3-3.15.0-SNAPSHOT-tests.jar"),
                os.path.join(self.bench_dir, "target/commons-lang3-3.15.0-SNAPSHOT.jar"),
                os.path.join(self.bench_dir, "target/dependency/*.jar"),
            ], load_test_cases(os.path.join(ASSETS_PATH, "apachecommon.txt")),
            {
            })

    def build(self) -> None:
        subprocess.call([
            "mvn",
            "-DskipTests",
            "package"
        ], cwd=self.bench_dir)
        subprocess.call([
            "mvn",
            "dependency:copy-dependencies"
        ], cwd=self.bench_dir)