import os
import subprocess

from .benchmark_base import UnitTestBenchmark
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases


class LuceneBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.bench_dir = os.path.join(ARTIFACTS_PATH, "solr")
        super().__init__(
            "solr",
            [
                os.path.join(self.bench_dir, "solr/core/build/classes/java/test/"),
                os.path.join(self.bench_dir, "solr/core/build/resources/test/"),
                os.path.join(self.bench_dir, "solr/core/libs/solr-core-10.0.0-SNAPSHOT.jar"),
                os.path.join(self.bench_dir,
                             "solr/core/build/dependency/*.jar"),
            ], load_test_cases(os.path.join(ASSETS_PATH, f"solr.txt")),
            {
                "tests.seed": "deadbeef",
                "java.security.egd": "file:/dev/./urandom",
                "test.solr.allowed.securerandom": "NativePRNG",
            },
            True)

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
