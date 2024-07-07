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
from .commons import FRAY_PATH, OUTPUT_PATH, SCHEDULERS, RR_PATH
from .utils import run_fray, run_rr, run_jpf


@click.group(name="mode")
@click.argument("application", type=click.Choice(list(BENCHMARKS.keys())))
@click.pass_context
def main(ctx, application: str):
    ctx.obj = BENCHMARKS[application]


@main.command(name="build")
@click.pass_obj
def build(app: BenchmarkBase):
    app.build()


@main.command(name="runRR")
@click.pass_obj
@click.option("--name", type=str, default=datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
@click.option("--timeout", "-t", type=int, default=10 * 60)
@click.option("--cpu", type=int, default=os.cpu_count())
def run_rr_command(app: BenchmarkBase, name: str, timeout: int, cpu: int):
    out_dir = os.path.join(OUTPUT_PATH, name, app.name, "rr")
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    with Pool(processes=cpu) as pool:
        pool.starmap(run_rr, map(lambda it: (*it, timeout),
                     app.generate_rr_test_commands(out_dir)))

@main.command(name="runJPF")
@click.pass_obj
@click.option("--name", type=str, default=datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
@click.option("--timeout", "-t", type=int, default=10 * 60)
@click.option("--cpu", type=int, default=os.cpu_count())
def run_jpf_command(app: BenchmarkBase, name: str, timeout: int, cpu: int):
    out_dir = os.path.join(OUTPUT_PATH, name, app.name, "jpf")
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    with Pool(processes=cpu) as pool:
        pool.starmap(run_jpf, map(lambda it: (*it, timeout),
                     app.generate_jpf_test_commands(out_dir)))


@main.command(name="run")
@click.pass_obj
@click.option("--scheduler", type=click.Choice(list(SCHEDULERS.keys())), default="pct3")
@click.option("--name", type=str, default=datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
@click.option("--debug-jvm", type=bool, is_flag=True, show_default=True, default=False)
@click.option("--timeout", "-t", type=int, default=10 * 60)
@click.option("--cpu", type=int, default=os.cpu_count())
def run(app: BenchmarkBase, scheduler: str, name: str, debug_jvm: bool, timeout: int, cpu: int):
    out_dir = os.path.join(OUTPUT_PATH, name, app.name, scheduler)
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    with Pool(processes=cpu) as pool:
        pool.starmap(run_fray, map(lambda it: (
            *it, timeout), app.generate_fray_test_commands(SCHEDULERS[scheduler], out_dir, debug_jvm)))


@main.command(name="runOne")
@click.argument("path", type=str)
@click.option("--timeout", "-t", type=int, default=10 * 60)
def run_one(path: str, timeout: int):
    saved = SavedBenchmark(path)
    tech = path.split("/")[-2]
    if tech == "rr":
        run_rr(saved.load_command(), path, RR_PATH, timeout)
    else:
        run_rr(saved.load_command(), path, FRAY_PATH, timeout)


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
        "--scheduler=pct",
        "--num-switch-points=15",
        "--logger=json",
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
            f'--path={os.path.join(path, "report", f"schedule_{replay}.json")}',
            "--logger=json",
        ],),
        "--debug-jvm"
    ], cwd=FRAY_PATH)


if __name__ == '__main__':
    main(None, None)
