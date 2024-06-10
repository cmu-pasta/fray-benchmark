#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import inspect
import importlib.util
from typing import Dict
from .bms.benchmark_base import BenchmarkBase, UnitTestBenchmark

SCHEDULERS = {
    "pct3": ['--scheduler=pct', '--num-switch-points=3'],
    "pct15": ['--scheduler=pct', '--num-switch-points=15'],
    "pos": ['--scheduler=pos'],
    "random": ['--scheduler=random'],
}

FRAY_PATH = os.environ["FRAY_PATH"]
SCRIPT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
PROJECT_PATH = os.path.join(SCRIPT_PATH, "..")
ARTIFACTS_PATH = os.path.join(PROJECT_PATH, "bms")
OUTPUT_PATH = os.path.join(PROJECT_PATH, "output")
BENCHMARKS: Dict[str, BenchmarkBase] = {}

for file in glob.glob(os.path.join(SCRIPT_PATH, "bms/*.py")):
    name = os.path.splitext(os.path.basename(file))[0]
    try:
        spec = importlib.util.find_spec(f"fray_benchmark.bms.{name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for n, obj in inspect.getmembers(module):
            if isinstance(obj, type) and issubclass(obj, BenchmarkBase) and obj != BenchmarkBase and obj != UnitTestBenchmark:
                app = obj() # type: ignore
                BENCHMARKS[app.name] = app
                print(f"Loaded benchmark {app.name}")
    except ImportError as e:
        continue
