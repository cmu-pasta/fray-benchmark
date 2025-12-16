import os
import subprocess

from .benchmark_base import UnitTestBenchmark
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases


class ConductorBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.bench_dir = os.path.join(ARTIFACTS_PATH, "conductor")
        super().__init__(
            "conductor",
            [
                os.path.join(self.bench_dir, "test-harness/build/classes/java/test/"),
                os.path.join(self.bench_dir, "test-harness/build/resources/test/"),
                os.path.join(self.bench_dir, "test-harness/build/dependency/*.jar"),
                os.path.join(self.bench_dir, "mysql-persistence/build/classes/java/test/"),
                os.path.join(self.bench_dir, "mysql-persistence/build/resources/test/"),
                os.path.join(self.bench_dir, "mysql-persistence/build/dependency/*.jar"),
            ],
            load_test_cases(os.path.join(ASSETS_PATH, f"conductor.txt")),
            {
            },
            True
        )

    def build(self) -> None:
        java17_home = os.environ.get("JDK17_HOME", "/usr/lib/jvm/java-17-openjdk-amd64")
        env = os.environ.copy()
        env["JAVA_HOME"] = java17_home

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
            ":conductor-test-harness:build",
            ":conductor-mysql-persistence:build",
            "-x", "test",
        ], cwd=self.bench_dir, env=env)
        subprocess.call([
            "./gradlew",
            ":conductor-test-harness:copyDependencies",
            ":conductor-mysql-persistence:copyDependencies",
        ], cwd=self.bench_dir, env=env)
