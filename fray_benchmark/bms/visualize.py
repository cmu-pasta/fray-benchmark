import os
import shutil
import re
import pandas as pd


class BenchResult():
    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        components = path.split("/")
        self.tech = components[-1]
        self.benchmark = components[-2]
        self.error_pattern = re.compile(r"(No Error|Error Found): (\d+\.\d+)")

    def to_csv(self):
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
                text = f.read()
                match = self.error_pattern.search(text)
                error_type, value = match.groups()
                if error_type == "No Error":
                    summary_file.write(f"{folder},0,{value}\n")
                elif error_type == "Error Found":
                    summary_file.write(f"{folder},1,{value}\n")

    def load_csv(self) -> pd.DataFrame:
        result_folder = os.path.join(self.path, "results")
        if not os.path.exists(result_folder):
            raise Exception("No results folder found")
        return pd.read_csv(os.path.join(result_folder, "summary.csv"), columns=["run", "error", "time"])

