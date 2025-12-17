import os
import subprocess

from .benchmark_base import UnitTestBenchmark
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases


class OpenSearchBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.bench_dir = os.path.join(ARTIFACTS_PATH, "opensearch")
        super().__init__(
            "opensearch",
            [
                # server main classes (production code that tests depend on)
                os.path.join(self.bench_dir, "server/build/classes/java/main/"),
                os.path.join(self.bench_dir, "server/build/resources/main/"),
                # server test classes
                os.path.join(self.bench_dir, "server/build/classes/java/test/"),
                os.path.join(self.bench_dir, "server/build/resources/test/"),
                os.path.join(self.bench_dir, "server/build/classes/java/internalClusterTest/"),
                os.path.join(self.bench_dir, "server/build/resources/internalClusterTest/"),
                # server dependencies (includes test framework jar transitively, with JNA excluded)
                os.path.join(self.bench_dir, "server/build/dependency/*.jar"),
            ],
            load_test_cases(os.path.join(ASSETS_PATH, f"opensearch.txt")),
            {
            },
            True  # JUnit 4
        )

    def build(self) -> None:
        # Use JDK 21 (OpenSearch requires Java 21+)
        java21_home = os.environ.get("JDK21_HOME", "/usr/lib/jvm/java-21-openjdk-amd64")
        env = os.environ.copy()
        env["JAVA_HOME"] = java21_home

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
        # Build server test classes (both test and internalClusterTest) and copy dependencies
        subprocess.call([
            "./gradlew",
            ":server:testClasses",
            ":server:internalClusterTestClasses",
            ":server:copyDependencies",
        ], cwd=self.bench_dir, env=env)
