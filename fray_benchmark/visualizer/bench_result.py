import os
import re
import shutil
from typing import List

import matplotlib
import matplotlib.axes
import pandas as pd
import seaborn as sns
import sns_config


class BenchResult:
    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        components = path.split("/")
        self.tech = components[-1]
        self.benchmark = components[-2]
        self.error_pattern = re.compile(r"(No Error|Error Found|Run Failed): (\d+\.\d+)")

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
            report = open(os.path.join(run_folder, "report.txt"))
            text = report.read()
            match = self.error_pattern.search(text)
            if not match:
                continue
            error_type, value = match.groups()
            if self.tech == "rr":
                total_iteration = int(text.strip().split("\n")[-2].split(":")[1]) + 1
            elif self.tech == "jpf":
                stdout = open(os.path.join(run_folder, "stdout.txt")).readlines()
                total_iteration = -1
                for line in reversed(stdout):
                    if line.startswith("paths ="):
                        total_iteration = int(line.split("=")[-1].strip())
                        break
                if error_type == "Error Found" and total_iteration == -1:
                    total_iteration = 1
            else:
                stdout = open(os.path.join(run_folder, "stdout.txt")).readlines()
                total_iteration = -1
                for line in reversed(stdout):
                    if line.startswith("Starting iteration"):
                        total_iteration = int(line.split(" ")[-1].strip()) + 1
                        break

            if error_type == "No Error":
                summary_file.write(f"{folder},0,{value},{total_iteration}\n")
            elif error_type == "Error Found":
                summary_file.write(f"{folder},1,{value},{total_iteration}\n")
            elif error_type == "Run Failed":
                summary_file.write(f"{folder},-1,{value},{total_iteration}\n")

    def load_csv(self) -> pd.DataFrame:
        result_folder = os.path.join(self.path, "results")
        if not os.path.exists(result_folder):
            raise Exception("No results folder found")
        return pd.read_csv(
            os.path.join(result_folder, "summary.csv"), names=["run", "error", "time", "iter"]
        )


class BenchmarkSuite:
    def __init__(self, path: str):
        self.benchmarks: List[BenchResult] = []
        self.path = os.path.abspath(path)
        for folder in os.listdir(self.path):
            self.benchmarks.append(BenchResult(
                os.path.join(self.path, folder)))

    def to_aggregated_dataframe(self) -> pd.DataFrame:
        data = []
        for bench in self.benchmarks:
            bench.to_csv()
            df = bench.load_csv()
            df["Technique"] = self.name_remap(bench.tech)
            data.append(df)
        return pd.concat(data)

    def name_remap(self, name: str) -> str:
        if name == "random":
            return "$\\textsc{Fray}$-Random"
        if name.startswith("pct"):
            return "$\\textsc{Fray}$-PCT"
        if name.startswith("pos"):
            return "$\\textsc{Fray}$-POS"
        if name == "rr":
            return "RR-Chaos"
        if name == "jpf":
            return "JPF-Random"
        # return name.upper()

    def to_aggregated_fig(self, measurement: str) -> matplotlib.axes.Axes:
        df = self.to_aggregated_dataframe()
        df = df[df["error"] == 1]
        df_grouped = df.groupby([measurement, 'Technique']).size().reset_index(name='count')
        # Pivot the dataframe to have 'time' as the index and 'tech' as columns
        df_pivot = df_grouped.pivot(index=measurement, columns='Technique', values='count').fillna(0)
        zero_row = pd.DataFrame(0, index=[0], columns=df_pivot.columns)
        df_pivot = pd.concat([zero_row, df_pivot]).sort_index()
        df_cumsum = df_pivot.cumsum()
        ax = sns.lineplot(data=df_cumsum, linewidth=2, markers=True)
        if measurement == "time":
            ax.set_xlabel('Seconds')
        else:
            ax.set_xlabel('Iterations')
        ax.set_ylabel('Cumulative \# of Bugs')
        return ax