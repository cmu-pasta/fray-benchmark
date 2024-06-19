#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import click
import shutil
import subprocess
from datetime import datetime
from multiprocessing import Pool
from .configs import BENCHMARKS, SCHEDULERS, FRAY_PATH, OUTPUT_PATH
from .bms.benchmark_base import BenchmarkBase
from .utils import run_command


@click.group(name="mode")
@click.argument("application", type=click.Choice(list(BENCHMARKS.keys())))
@click.pass_context
def main(ctx, application: str):
    ctx.obj = BENCHMARKS[application]


@main.command(name="build")
@click.pass_obj
def build(app: BenchmarkBase):
    app.build()


@main.command(name="run")
@click.pass_obj
@click.option("--scheduler", type=click.Choice(list(SCHEDULERS.keys())), default="pct3")
@click.option("--name", type=str, default=datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
@click.option("--debug-jvm", type=bool, is_flag=True, show_default=True, default=False)
@click.option("--timeout", "-t", type=int, default=10 * 60)
@click.option("--cpu", type=int, default = os.cpu_count())
def run(app: BenchmarkBase, scheduler: str, name: str, debug_jvm: bool, timeout: int, cpu: int):
    out_dir = os.path.join(OUTPUT_PATH, name, scheduler)
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    with Pool(processes=cpu) as pool:
        pool.starmap(run_command, map(lambda it: (*it, timeout), app.generate_test_commands(SCHEDULERS[scheduler], out_dir, debug_jvm)))

@main.command(name="runSingle")
@click.argument("path", type=str)
@click.option("--debug-jvm", type=bool, is_flag=True, show_default=True, default=False)
def run(path: str, debug_jvm: bool):
    out_dir = os.path.join("/tmp/replay")
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    subprocess.call([
        './gradlew',
        "runFray",
        "-PconfigPath=" + os.path.join(path, "config.json"),
        "-PextraArgs=" + " ".join([
            "--scheduler=pct",
            "--logger=csv",
            "--iter",
            "-100",
        ],),
        "--debug-jvm"
    ], cwd=FRAY_PATH)

@main.command(name="replay")
@click.argument("path", type=str)
@click.argument("replay", type=str)
@click.option("--debug-jvm", type=bool, is_flag=True, show_default=True, default=False)
def run(path: str, replay: str, debug_jvm: bool):
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
            f'--path={os.path.join(path, "report", f"schedule_simplified_{replay}.csv")}',
            "--logger=csv",
        ],),
        "--debug-jvm"
    ], cwd=FRAY_PATH)

if __name__ == '__main__':
    main(None, None)

