import os
import re
import time
import shutil
import json
from typing import List, Dict, Any
import subprocess
from .commons import PERF_TRIALS, PERF_ITER


def run_fray(command: Dict[str, Any], log_path: str, cwd: str, timeout: int):
    print(f"Running {log_path}")
    with open(os.path.join(log_path, "command.txt"), "w") as f:
        f.write(" ".join(command))
    error_found = False
    try:
        start_time = time.time()
        proc = subprocess.run(command, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        error_found = proc.returncode != 0 and proc.returncode != 124
    except subprocess.TimeoutExpired:
        pass
    with open(os.path.join(log_path, "report.txt"), "w") as report:
        if error_found:
            report.write(f"Error Found: {time.time() - start_time}\n")
        else:
            report.write(f"No Error: {time.time() - start_time}\n")


def run_jpf(command: List[str], log_path: str, cwd: str, timeout: int):
    print(f"Running {log_path}")
    with open(os.path.join(log_path, "command.json"), "w") as f:
        json.dump(command, f)
    try:
        stdout_path = os.path.join(log_path, "stdout.txt")
        start_time = time.time()
        subprocess.run(command["command"], cwd=cwd, stdout=open(stdout_path, "w"), stderr=open(
            os.path.join(log_path, "stderr.txt"), "w"))
    except subprocess.TimeoutExpired:
        pass
    with open(os.path.join(log_path, "report.txt"), "w") as report:
        end_time = time.time()
        with open(stdout_path, "r") as f:
            data = f.read()
            if "==== error 1" in data:
                if "UnsupportedOperationException" in data or \
                    "NoSuchMethodException" in data or "FileNotFoundException" in data or\
                        "Null charset name" in data or "NoSuchMethodError" in data:
                    report.write(f"Run failed: {end_time - start_time}\n")
                else:
                    report.write(f"Error Found: {end_time - start_time}\n")
            else:
                report.write(f"No Error: {end_time - start_time}\n")


def run_rr(command: List[str], log_path: str, cwd: str, timeout: int):
    print(f"Running {log_path}")
    trace_dir = os.path.join(log_path, "trace")
    with open(os.path.join(log_path, "command.txt"), "w") as f:
        f.write(" ".join(command))
    with open(os.path.join(log_path, "report.txt"), "w") as stdout:
        start_time = time.time()
        error_found = False
        try:
            proc = subprocess.run(command, cwd=cwd, stdout=open(os.path.join(
                log_path, "stdout.txt"), "w"), stderr=open(os.path.join(log_path, "stderr.txt"), "w"), env={"RR_TIMEOUT": str(timeout)})
            error_found = proc.returncode != 0 and proc.returncode != 124
        except subprocess.TimeoutExpired:
            pass
        if error_found:
            stdout.write(f"Error Found: {time.time() - start_time}\n")
        else:
            stdout.write(f"No Error: {time.time() - start_time}\n")


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
            new_path = os.path.abspath(path)
            if path.endswith('/'):
                new_path += '/'
            resolved_paths.append(new_path)
    return resolved_paths
