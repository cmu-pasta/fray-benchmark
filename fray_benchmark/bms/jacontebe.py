import os
import subprocess
import re

from ..objects.execution_config import RunConfig, Executor
from ..commons import ARTIFACTS_PATH, ASSETS_PATH
from .benchmark_base import BenchmarkBase
from ..utils import load_test_cases
from typing import List, Dict, Iterator


class JaConTeBe(BenchmarkBase):
    def __init__(self) -> None:
        self.bench_dir = os.path.join(ARTIFACTS_PATH, "JaConTeBe")
        self.test_cases = load_test_cases(
            os.path.join(ASSETS_PATH, "jacontebe.txt"))
        super().__init__("jacontebe")

    def get_test_cases(self, tool_type: str) -> Iterator[RunConfig]:
        target_pattern = re.compile(r"target = ([a-zA-Z0-9_.-]*)")
        cp_pattern = re.compile(r"classpath = ([a-zA-Z0-9_.-:-]*)")
        for test_case in self.test_cases:
            with open(os.path.join(self.bench_dir, "testplans.alt", "jpfscripts", f"{test_case}.jpf")) as f:
                run_config = f.read()
                target_match = target_pattern.search(run_config)
                cp_match = cp_pattern.search(run_config)
                if target_match and cp_match:
                    class_to_run = target_match.group(1)
                    classpaths = cp_match.group(1).split(":")[1:]
                    args = []
                    if tool_type != "rr" and tool_type != "java":
                        args.append("-mo")
                    if "Groovy5198" in class_to_run:
                        args.extend(["-tn", "2", "-l", "1"])
                    yield RunConfig(
                        Executor(
                            class_to_run,
                            "main",
                            args,
                            [
                                os.path.join(self.bench_dir,
                                             "build", test_case) + "/",
                                *map(lambda x: os.path.join(self.bench_dir, x), classpaths),
                            ],
                            {}
                        ),
                        False,
                        False,
                        False,
                        -1,
                    )

    def build(self) -> None:
        for test_case in self.test_cases:
            print(self.bench_dir)
            subprocess.call([
                "./scripts/install.sh",
                "orig",
                test_case
            ], cwd=self.bench_dir)
