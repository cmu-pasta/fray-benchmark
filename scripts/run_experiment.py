import os
import glob
import subprocess
import sys
import re
import argparse
from typing import Iterator


BASE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
BM_FOLDER = os.path.join(BASE, "src/main/java/cmu/pasta/fray/benchmark/")
JC_FOLDER = os.path.join(BASE, "jacontebe_experiments")

SCHEDULERS = {
    "pct3": '--scheduler=pct --num-switch-points 3',
    "pct10": '--scheduler=pct --num-switch-points 10',
    "pct25": '--scheduler=pct --num-switch-points 25',
    #  "pct100": '--scheduler=pct --num-switch-points 100',
    "pos": '--scheduler=pos',
    "random": '--scheduler=random',
}

def find_tests() -> Iterator[str]:
    for bm in glob.glob(os.path.join(BM_FOLDER, "**/*.java"), recursive=True):
        bm = bm.replace(BM_FOLDER, "").replace("/", ".").replace(".java", "")
        # if "hard" in bm:
        print(bm)
        yield bm


def run_sct(fray_path: str, bm_name: str, args: str, interleave_memory_ops: bool = True) -> int:
    command = [
        "./gradlew",
        "examples:runSCT",
        f"-Pclasspath={BASE}/build/classes/java/main",
        f"-PmainClass={bm_name}",
        f"-PextraArgs={args}" + (" -m true" if interleave_memory_ops else ""),
    ]
    print(" ".join(command))
    output = subprocess.check_output(command, cwd=fray_path).decode("utf-8")
    time_pattern = re.compile(r"Analysis done in: (\d+) ms")
    match = time_pattern.search(output)
    if match:
        time = int(match.group(1))
    pattern = re.compile(r"Error found at iter: (\d+)")
    match = pattern.search(output)
    if match:
        return int(match.group(1)), time
    else:
        return -1, time

def run_jacontebe(fray_path: str, bm_name: str, args: str, interleave_memory_ops: bool = True) -> int:
    command = [
        f"{BASE}/scripts/run_jacontebe_target.sh",
        f"{fray_path}",
        f"{JC_FOLDER}",
        f"{bm_name}",
        f"{args}" + (" -m true" if interleave_memory_ops else ""),
    ]
    print(" ".join(command))
    try:
        output = subprocess.check_output(command, cwd=BASE).decode("utf-8")
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    time_pattern = re.compile(r"Analysis done in: (\d+) ms")
    match = time_pattern.search(output)
    if match:
        time = int(match.group(1))
    pattern = re.compile(r"Error found at iter: (\d+)")
    match = pattern.search(output)
    if match:
        return int(match.group(1)), time
    else:
        return -1, time

def main(fray_path: str, iteration: int, benchmark: str, interleave_memory_ops: bool, output: str):
    fray_path = os.path.abspath(fray_path)
    result_csv = open(output, "w")
    if benchmark == "sct":
        for bm in find_tests():
            for name, args in SCHEDULERS.items():
                print(f"Running {bm} with {name}")
                for _ in range(iteration):
                    iter, time = run_sct(fray_path, bm, args, interleave_memory_ops)
                    result_csv.write(f"{bm},{name},{iter},{time}\n")
    elif benchmark == "jc":
        bms = os.listdir(os.path.join(JC_FOLDER, "JaConTeBe/versions.alt"))
        # Filter out all JDK bugs for now
        bms = [t for t in bms if "jdk" not in t]
        for bm in bms:
            for name, args in SCHEDULERS.items():
                print(f"Running {bm} with {name}")
                for _ in range(iteration):
                    iter, time = run_jacontebe(fray_path, bm, args, interleave_memory_ops)
                    result_csv.write(f"{bm},{name},{iter},{time}\n")
    else:
        print("Benchmark should be one of 'sct' or 'jc'!")
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fray_path", type=str, help="Path to the fray project")
    parser.add_argument("output", type=str, help="Output file")
    parser.add_argument("--benchmark", type=str, help="Name of benchmark: sct or jc")
    parser.add_argument("--interleave_memory_ops", action="store_true", help="Interleave memory operations", default=False)
    parser.add_argument("--iteration", type=int, default=10, help="Number of iteration")
    main(**vars(parser.parse_args()))
