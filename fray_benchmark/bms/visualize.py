import os
import shutil
import re


class BenchResult():
    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        components = path.split("/")
        self.tech = components[-1]
        self.benchmark = components[-2]
        self.no_error_pattern = re.compile(r"No Error: (\d+\.\d+)")
        self.error_found_pattern = re.compile(r"Error Found: (\d+\.\d+)")

    def load(self):
        result_folder = os.path.join(self.path, "results")
        if os.path.exists(result_folder):
            shutil.rmtree(result_folder)
        os.makedirs(result_folder)
        summary_file = open(os.path.join(result_folder, "summary.csv"), "w")
        for folder in os.listdir(self.path):
            if folder == "results":
                continue
            run_folder = os.path.join(self.path, folder)
            with open(os.path.join(run_folder, "report.txt")) as f:

                # summary_file.write(f"{folder},{f.read()}")
                pass

