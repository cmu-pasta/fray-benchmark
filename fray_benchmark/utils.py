import os
import re
import time
from typing import List
import subprocess


def run_fray(command: List[str], log_path: str, cwd: str, timeout: int):
    print(f"Running {log_path}")
    print(f"Running {cwd}")
    with open(os.path.join(log_path, "command.txt"), "w") as f:
        f.write(" ".join(command))
    try:
        subprocess.call(command, cwd=cwd, stdout=open(os.path.join(log_path, "stdout.txt"), "w"), stderr=open(os.path.join(log_path, "stderr.txt"), "w"), timeout=timeout)
    except subprocess.TimeoutExpired:
        pass


def run_rr(command: List[str], log_path: str, timeout: int):
    print(f"Running {log_path}")
    start_time = time.time()
    command = ["rr", "record", "--chaos"] + command
    with open(os.path.join(log_path, "command.txt"), "w") as f:
        f.write(" ".join(command))
    with open(os.path.join(log_path, "stdout.txt"), "w") as stdout:
        iter = 0
        while (time.time() - start_time) < timeout:
            stdout.write(f"Iteration: {iter}")
            proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if proc.returncode != 0:
                stdout.write(f"Error: {proc.returncode}")
                stdout.write(proc.stdout.decode("utf-8"))
                stdout.write(proc.stderr.decode("utf-8"))
                break
            iter += 1


def load_test_cases(file_path: str) -> List[str]:
    with open(file_path) as f:
        return list(filter(str.__len__, map(str.strip, f.readlines())))

def resolve_classpaths(classpaths: List[str]) -> List[str]:
    resolved_paths = []
    for path in classpaths:
        if '*' in path:
            dir_path = os.path.dirname(path)
            pattern = os.path.basename(path).replace('*', '.*')
            regex = re.compile(pattern)

            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                for entry in os.listdir(dir_path):
                    if regex.match(entry):
                        resolved_paths.append(os.path.join(dir_path, entry))
        else:
            resolved_paths.append(os.path.abspath(path))
    return resolved_paths