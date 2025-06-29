import os
import subprocess

from .benchmark_base import UnitTestBenchmark
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from ..utils import load_test_cases


class LuceneBenchmark(UnitTestBenchmark):
    def __init__(self) -> None:
        self.lucene_dir = os.path.join(ARTIFACTS_PATH, "lucene")
        super().__init__(
            "lucene",
            [
                os.path.join(self.lucene_dir, "lucene/core/build/libs/*.jar"),
                os.path.join(self.lucene_dir,
                             "lucene/core/build/dependency/*.jar"),
            ], load_test_cases(os.path.join(ASSETS_PATH, "lucene.txt")),
            {
                "tests.seed": "deadbeef",
                "tests.jvmForkArgsFile": os.path.join(self.lucene_dir, "lucene/core/build/tmp/test/jvm-forking.properties"),
            },
            True)

    def build(self) -> None:
        subprocess.call([
            "git",
            "checkout",
            "."
        ], cwd=self.lucene_dir)
        subprocess.call([
            "git",
            "apply",
            os.path.join(ASSETS_PATH, "lucene.patch")
        ], cwd=self.lucene_dir)
        subprocess.call([
            "./gradlew",
            "testJar",
        ], cwd=self.lucene_dir)
        subprocess.call([
            "./gradlew",
            "copyDependencies",
        ], cwd=self.lucene_dir)
