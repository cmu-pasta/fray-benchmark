#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
from datetime import datetime
from multiprocessing import Pool

import click

from .benchmarks import BENCHMARKS
from .bms.benchmark_base import BenchmarkBase, SavedBenchmark
from .commons import FRAY_PATH, OUTPUT_PATH, SCHEDULERS, RR_PATH, JPF_PATH
from .utils import run_fray, run_rr, run_jpf


@click.group(name="mode")
def main():
    pass


@main.command(name="build")
@click.argument("application", type=click.Choice(list(BENCHMARKS.keys())))
def build(application: str):
    app = BENCHMARKS[application]
    app.build()


@main.command(name="run")
@click.argument("tool", type=click.Choice(["jpf", "rr", "fray"]))
@click.argument("application", type=click.Choice(list(BENCHMARKS.keys())))
@click.option("--scheduler", type=click.Choice(list(SCHEDULERS.keys())))
@click.option("--name", type=str, default=datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
@click.option("--timeout", "-t", type=int, default=60*10)
@click.option("--cpu", type=int, default=os.cpu_count())
@click.option("--perf-mode", type=bool, is_flag=True, show_default=True, default=False)
@click.option("--iterations", type=int, default=20)
def run(tool: str, application: str, scheduler: str, name: str, timeout: int, cpu: int, iterations: int, perf_mode: bool):
    app = BENCHMARKS[application]
    for i in range(iterations):
        out_dir = os.path.join(OUTPUT_PATH, name, app.name, scheduler if tool == "fray" else tool, f"iter-{i}")
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        os.makedirs(out_dir, exist_ok=True)
        with Pool(processes=cpu) as pool:
            if tool == "rr":
                pool.starmap(run_rr, map(lambda it: (*it, timeout),
                            app.generate_rr_test_commands(out_dir, timeout, perf_mode)))
            elif tool == "jpf":
                pool.starmap(run_jpf, map(lambda it: (*it, timeout),
                            app.generate_jpf_test_commands(out_dir, timeout, perf_mode)))
            else:
                pool.starmap(run_fray, map(lambda it: (
                    *it, timeout), app.generate_fray_test_commands(SCHEDULERS[scheduler], out_dir, timeout, perf_mode)))


@main.command(name="runOne")
@click.argument("path", type=str)
@click.option("--timeout", "-t", type=int, default=10 * 60)
def run_one(path: str, timeout: int):
    saved = SavedBenchmark(path)
    tech = path.split("/")[-3]
    if tech == "rr":
        run_rr(saved.load_command(), path, RR_PATH, timeout)
    elif tech == "jpf":
        run_jpf(saved.load_command(), path, JPF_PATH, timeout)
    else:
        run_fray(saved.load_command(), path, FRAY_PATH, timeout)


@main.command(name="runSingle")
@click.argument("path", type=str)
@click.option("--debug-jvm", type=bool, is_flag=True, show_default=True, default=False)
@click.option("--no-fray", type=bool, is_flag=True, show_default=True, default=False)
def run_single(path: str, debug_jvm: bool, no_fray: bool):
    out_dir = os.path.join("/tmp/replay")
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    fray_args = [
        "--scheduler=pos",
        # "--num-switch-points=15",
        "--iter",
        "-100",
    ]
    if no_fray:
        fray_args.append("--no-fray")
    command = [
        './gradlew',
        "runFray",
        "-PconfigPath=" + os.path.join(path, "config.json"),
        "-PextraArgs=" + " ".join(fray_args),
    ]
    if debug_jvm:
        command.append("--debug-jvm")
    subprocess.call(command, cwd=FRAY_PATH)


@main.command(name="replay")
@click.argument("path", type=str)
@click.argument("replay", type=str)
@click.option("--debug-jvm", type=bool, is_flag=True, show_default=True, default=False)
def replay(path: str, replay: str, debug_jvm: bool):
    out_dir = os.path.join("/tmp/replay")
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    subprocess.call([
        './gradlew',
        "runFray",
        "-PconfigPath=" + os.path.join(path, "config.json"),
        "-PextraArgs=" + " ".join([
            "--scheduler=replay",
            f'--path={os.path.join(path, "report", f"index_{replay}")}',
        ],),
        "--debug-jvm"
    ], cwd=FRAY_PATH)


if __name__ == '__main__':
    main()
