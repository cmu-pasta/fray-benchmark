import os
import re
import time
import shutil
from typing import List
import subprocess


def run_fray(command: List[str], log_path: str, cwd: str, timeout: int):
    print(f"Running {log_path}")
    with open(os.path.join(log_path, "command.txt"), "w") as f:
        f.write(" ".join(command))
    error_found = False
    try:
        start_time = time.time()
        proc = subprocess.run(command, cwd=cwd, stdout=open(os.path.join(log_path, "stdout.txt"), "w"), stderr=open(os.path.join(log_path, "stderr.txt"), "w"), timeout=timeout)
        error_found = proc.returncode != 0
    except subprocess.TimeoutExpired:
        pass
    with open(os.path.join(log_path, "report.txt"), "w") as report:
        if error_found != 0:
            report.write(f"Error Found: {time.time() - start_time}\n")
        else:
            report.write(f"No Error: {time.time() - start_time}\n")



def run_jpf(command: List[str], log_path: str, cwd: str, timeout: int):
    print(f"Running {log_path}")
    with open(os.path.join(log_path, "command.txt"), "w") as f:
        f.write(" ".join(command))
    try:
        stdout_path = os.path.join(log_path, "stdout.txt")
        start_time = time.time()
        subprocess.run(command, cwd=cwd, stdout=open(stdout_path, "w"), stderr=open(os.path.join(log_path, "stderr.txt"), "w"), timeout=timeout)
    except subprocess.TimeoutExpired:
        pass
    with open(os.path.join(log_path, "report.txt"), "w") as report:
        end_time = time.time()
        with open(stdout_path, "r") as f:
            data = f.read()
            if "==== error 1" in data and "UnsupportedOperationException" not in data:
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
        iter_num = 0
        error_found = False
        while (time.time() - start_time) < timeout:
            stdout.write(f"Iteration: {iter_num}\n")
            if os.path.exists(trace_dir):
                shutil.rmtree(trace_dir)
            try:
                proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, timeout=timeout - (time.time() - start_time))
            except subprocess.TimeoutExpired:
                break
            if proc.returncode != 0:
                error_found = True
                break
            iter_num += 1
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
            resolved_paths.append(os.path.abspath(path))
    return resolved_paths