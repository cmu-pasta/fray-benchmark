import os
import shutil
import re
import pandas as pd
import seaborn as sns
import matplotlib


class BenchResult:
    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        components = path.split("/")
        self.tech = components[-1]
        self.benchmark = components[-2]
        self.error_pattern = re.compile(r"(No Error|Error Found): (\d+\.\d+)")

    def to_csv(self):
        print("to_csv")
        print(self.path)
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
                if not match:
                    continue
                error_type, value = match.groups()
                if error_type == "No Error":
                    summary_file.write(f"{folder},0,{value}\n")
                elif error_type == "Error Found":
                    summary_file.write(f"{folder},1,{value}\n")

    def load_csv(self) -> pd.DataFrame:
        result_folder = os.path.join(self.path, "results")
        if not os.path.exists(result_folder):
            raise Exception("No results folder found")
        return pd.read_csv(
            os.path.join(result_folder, "summary.csv"), names=["run", "error", "time"]
        )


class BenchmarkSuite:
    def __init__(self, path: str):
        self.benchmarks = []
        self.path = os.path.abspath(path)
        for folder in os.listdir(self.path):
            self.benchmarks.append(BenchResult(os.path.join(self.path, folder)))

    def to_aggregated_dataframe(self) -> pd.DataFrame:
        data = []
        for bench in self.benchmarks:
            df = bench.load_csv()
            df["tech"] = bench.tech
            data.append(df)
        return pd.concat(data)

    def to_aggregated_fig(self) -> matplotlib.axes.Axes:
        df = self.to_aggregated_dataframe()
        return sns.ecdfplot(df, x="time", hue="tech")
