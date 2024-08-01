#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Dict

import glob
import importlib
import os
import inspect
from .commons import SCRIPT_PATH
from .bms.benchmark_base import BenchmarkBase, UnitTestBenchmark, MainMethodBenchmark, SavedBenchmark
BENCHMARKS: Dict[str, BenchmarkBase] = {}

for file in glob.glob(os.path.join(SCRIPT_PATH, "bms/*.py")):
    name = os.path.splitext(os.path.basename(file))[0]
    try:
        spec = importlib.util.find_spec(f"fray_benchmark.bms.{name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for n, obj in inspect.getmembers(module):
            if isinstance(obj, type) and issubclass(obj, BenchmarkBase) and obj != BenchmarkBase and obj != UnitTestBenchmark and obj != MainMethodBenchmark and obj != SavedBenchmark:
                app = obj()  # type: ignore
                BENCHMARKS[app.name] = app
    except ImportError as e:
        continue
