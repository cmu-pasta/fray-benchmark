import os
import subprocess

from .benchmark_base import UnitTestBenchmark
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases


class HttpcoreBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.bench_dir = os.path.join(ARTIFACTS_PATH, "httpcore")
        self.httpcore_module = os.path.join(self.bench_dir, "httpcore")
        self.httpcore_nio_module = os.path.join(self.bench_dir, "httpcore-nio")
        super().__init__(
            "httpcore",
            [
                # httpcore module - test classes
                os.path.join(self.httpcore_module, "target/test-classes/"),
                # httpcore module - main classes
                os.path.join(self.httpcore_module, "target/classes/"),
                # httpcore module - dependencies
                os.path.join(self.httpcore_module, "target/dependency/*.jar"),
                # httpcore-nio module - test classes
                os.path.join(self.httpcore_nio_module, "target/test-classes/"),
                # httpcore-nio module - main classes
                os.path.join(self.httpcore_nio_module, "target/classes/"),
                # httpcore-nio module - dependencies
                os.path.join(self.httpcore_nio_module, "target/dependency/*.jar"),
            ],
            load_test_cases(os.path.join(ASSETS_PATH, f"httpcore.txt")),
            {
            },
            True  # JUnit 4
        )

    def build(self) -> None:
        java11_home = os.environ.get("JDK11_HOME", "/usr/lib/jvm/java-11-openjdk")
        env = os.environ.copy()
        env["JAVA_HOME"] = java11_home

        # Apply patch to update Java version from 1.5 to 1.8
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
            "mvn",
            "clean",
            "install",
            "-DskipTests",
            "-Dmaven.test.skip=true",
        ], cwd=self.bench_dir, env=env)

        subprocess.call([
            "mvn",
            "test-compile",
        ], cwd=self.bench_dir, env=env)

        # Copy dependencies for httpcore module
        subprocess.call([
            "mvn",
            "dependency:copy-dependencies",
        ], cwd=self.bench_dir, env=env)