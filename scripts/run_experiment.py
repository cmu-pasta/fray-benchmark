import os
import glob
import subprocess
import sys
import re
from typing import Iterator


BASE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
BM_FOLDER = os.path.join(BASE, "src/main/java/cmu/pasta/sfuzz/benchmark/")

SCHEDULERS = {
    "pct3": '--scheduler=pct --num-switch-points 3',
    "pct10": '--scheduler=pct --num-switch-points 10',
    "pct50": '--scheduler=pct --num-switch-points 50',
    "pct100": '--scheduler=pct --num-switch-points 100',
    "pos": '--scheduler=pos',
    "random": '--scheduler=random',
}

def find_tests() -> Iterator[str]:
    for bm in glob.glob(os.path.join(BM_FOLDER, "**/*.java"), recursive=True):
        bm = bm.replace(BM_FOLDER, "").replace("/", ".").replace(".java", "")
        if "hard" in bm:
            print(bm)
            yield bm


def run(sfuzz_path: str, bm_name: str, args: str) -> int:
    command = [
        "./gradlew",
        "examples:runSCT",
        f"-Pclasspath={BASE}/build/classes/java/main",
        f"-PmainClass={bm_name}",
        f"-PextraArgs={args} -m true"
    ]
    print(" ".join(command))
    output = subprocess.check_output(command, cwd=sfuzz_path)
    pattern = re.compile(r"Error found at iter: (\d+)")
    match = pattern.search(output.decode("utf-8"))
    if match:
        return int(match.group(1))
    else:
        return -1

def main():
    result_csv = open("results_hard_mem.csv", "w")
    sfuzz_path = sys.argv[1]
    for bm in find_tests():
        for name, args in SCHEDULERS.items():
            print(f"Running {bm} with {name}")
            result = run(sfuzz_path, bm, args)
            result_csv.write(f"{bm},{name},{result}\n")

if __name__ == "__main__":
    main()
