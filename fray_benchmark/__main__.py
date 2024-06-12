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
from typing import List


@click.group(name="mode")
@click.argument("application", type=click.Choice(list(BENCHMARKS.keys())))
@click.pass_context
def main(ctx, application: str):
    ctx.obj = BENCHMARKS[application]


@main.command(name="build")
@click.pass_obj
def build(app: BenchmarkBase):
    app.build()


def run_command(command: List[str], log_path: str):
    with open(os.path.join(log_path, "command.txt"), "w") as f:
        f.write(" ".join(command))
    subprocess.call(command, cwd=FRAY_PATH, stdout=open(os.path.join(log_path, "stdout.txt"), "w"), stderr=open(os.path.join(log_path, "stderr.txt"), "w")

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
        pool.map(run_command, app.generate_test_commands(SCHEDULERS[scheduler], out_dir, debug_jvm))


@main.command(name="replay")
@click.pass_obj
@click.option("--path", type=str)
@click.option("--debug-jvm", type=bool, is_flag=True, show_default=True, default=False)
def run(app: BenchmarkBase, path: str, debug_jvm: bool):
    out_dir = os.path.join("/tmp/replay")
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    for command, _ in app.generate_test_commands([
        "--scheduler=replay",
        f"--path={path}",
    ], out_dir, debug_jvm):
        subprocess.call(command, cwd=FRAY_PATH)

if __name__ == '__main__':
    main(None, None)

