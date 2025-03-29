import os
import subprocess

from .benchmark_base import UnitTestBenchmark
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases


class CuratorRecipesBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.target_dir = os.path.join(ARTIFACTS_PATH, "curator")
        super().__init__(
            "curator-recipes",
            [
                os.path.join(
                    self.target_dir, "curator-recipes/target/curator-recipes-5.8.1-SNAPSHOT.jar"),
                os.path.join(
                    self.target_dir, "curator-recipes/target/curator-recipes-5.8.1-SNAPSHOT-tests.jar"),
                os.path.join(self.target_dir,
                             "curator-recipes/target/dependency/*.jar"),
            ], load_test_cases(os.path.join(ASSETS_PATH, "curator.txt")),
            {},
            False)

    def build(self) -> None:
        subprocess.call([
            "./mvnw",
            "install",
            "-DskipTests",
        ], cwd=self.target_dir)
        subprocess.call([
            "./mvnw",
            "dependency:copy-dependencies",
        ], cwd=self.target_dir)


class CuratorFrameworkBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.target_dir = os.path.join(ARTIFACTS_PATH, "curator")
        super().__init__(
            "curator-framework",
            [
                os.path.join(
                    self.target_dir, "curator-framework/target/curator-framework-5.8.1-SNAPSHOT.jar"),
                os.path.join(
                    self.target_dir, "curator-framework/target/curator-framework-5.8.1-SNAPSHOT-tests.jar"),
                os.path.join(self.target_dir,
                             "curator-framework/target/dependency/*.jar"),
            ], load_test_cases(os.path.join(ASSETS_PATH, "curator-framework.txt")),
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
            os.path.join(ASSETS_PATH, "curator.patch")
        ], cwd=self.target_dir)
        subprocess.call([
            "./mvnw",
            "install",
            "-DskipTests",
        ], cwd=self.target_dir)
        subprocess.call([
            "./mvnw",
            "dependency:copy-dependencies",
        ], cwd=self.target_dir)
