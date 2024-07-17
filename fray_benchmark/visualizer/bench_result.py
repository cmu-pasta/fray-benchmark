import os
import re
import shutil
from typing import List
import numpy as np

import matplotlib
import matplotlib.axes
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import sns_config


class BenchResult:
    def __init__(self, path: str, has_trial: bool):
        self.path = os.path.abspath(path)
        components = path.split("/")
        if has_trial:
            self.trial = components[-1]
            self.tech = components[-2]
            self.benchmark = components[-3]
        else:
            self.trial = "iter-1"
            self.tech = components[-1]
            self.benchmark = components[-2]
        self.error_pattern = re.compile(
            r"(No Error|Error Found|Run failed): (\d+\.\d+)")
        self.user_time_pattern = re.compile(r"user (\d+\.\d+)")
        self.sys_time_pattern = re.compile(r"sys (\d+\.\d+)")

    def lucene_bug_classify(self, stdout: str):
        if "DeadlockException" in stdout:
            if "onThreadParkNanos" in stdout:
                return "FP(Time)"
        if "AssertionError: JVM fork arguments are not present" in stdout:
            return "Run failure"
        if "testTimeLimitingBulkScorer" in stdout:
            return "TP(Time)"
        if "TestRateLimiter" in stdout:
            return "TP(Time)"
        if "testTimeoutLargeNumberOfMerges" in stdout:
            return "TP(Time)"
        if "TestConcurrentMergeScheduler.testIntraMergeThreadPoolIsLimitedByMaxThreads" in stdout:
            return "TP(Time)"
        if "java.lang.RuntimeException: unclosed IndexInput" in stdout:
            return "TP(#13552)"
        if "testSubclassConcurrentMergeScheduler" in stdout:
            return "TP(#13547)"
        if "testMultiThreadedSnapshotting" in stdout:
            return "TP(#13571)"
        if "testMaxMergeCount" in stdout:
            return "TP(?890)"
        if "FATAL src/Task.cc:1429:compute_trap_reasons" in stdout:
            return "Run failure"
        print(stdout)
        exit(0)

    def kafka_bug_classify(self, stdout: str):
        if "DefaultStateUpdaterTest.shouldRecordMetrics" in stdout:
            return "TP(?90)"
        if "[FATAL src/Task.cc:1429:compute_trap_reasons()]" in stdout:
            return "Run failure"
        if "Condition not met within timeout" in stdout:
            return "TP(Time)"
        if "shouldReturnFalseOnCloseWithCloseOptionWithLeaveGroupTrueWhenThreadsHaventTerminated" in stdout:
            return "TP(Time)"
        if "shouldThrowIfAddingTasksWithSameId" in stdout:
            return "TP(KAFKA-17114)"
        if "DefaultTaskExecutorTest.shouldSetTaskTimeoutOnTimeoutException" in stdout:
            return "TP(Time)"
        if "Deadlock" in stdout and ("DefaultStateUpdater" in stdout or "DefaultTaskManager" in stdout):
            return "TP(KAFKA-17112)"
        if "KafkaStreamsTest.shouldNotBlockInCloseWithCloseOptionLeaveGroupFalseForZeroDuration" in stdout:
            return "TP(?186)"
        if "shouldRecoverFromInvalidOffsetExceptionOnRestoreAndFinishRestore" in stdout:
            return "TP(Time)"
        if "KafkaStreamsTest.shouldThrowOnCleanupWhileShuttingDownStreamClosedWithCloseOptionLeaveGroupTrue" in stdout:
            return "TP(?207)"
        if "StreamThreadTest$StateListenerStub.onChange" in stdout:
            return "TP(?63)"
        if "KafkaStreamsTest.shouldNotBlockInCloseWithCloseOptionLeaveGroupTrueForZeroDuration" in stdout:
            return "TP(Time)"
        if "KafkaStreamsTest.shouldReturnFalseOnCloseWithCloseOptionWithLeaveGroupFalseWhenThreadsHaventTerminated" in stdout:
            return "TP(?216)"
        if "StreamThreadTest.shouldNotEnforceRebalanceWhenCurrentlyRebalancing" in stdout:
            return "TP(Time)"
        if "KafkaStreamsTest.shouldThrowOnCleanupWhileShuttingDownStreamClosedWithCloseOptionLeaveGroupFalse" in stdout:
            return "TP(?159)"
        if "DefaultTaskExecutorTest.shouldPunctuateSystemTime" in stdout:
            return "TP(Time)"
        if "GlobalStreamThreadTest.shouldThrowStreamsExceptionOnStartupIfThereIsAStreamsException" in stdout:
            return "TP(?275)"
        if "KafkaStreamsTest.shouldThrowOnCleanupWhileShuttingDown" in stdout:
            return "TP(?196)"
        if "DefaultStateUpdaterTest.shouldRestoreActiveStatefulTasksAndUpdateStandbyTasks" in stdout:
            return "TP(?152)"
        if "DefaultTaskExecutorTest.shouldNotFlushOnException" in stdout:
            return "TP(?261)"
        if "StreamThreadTest.shouldOnlyCompleteShutdownAfterRebalanceNotInProgress" in stdout:
            return "TP(Time)"
        if "StreamThreadTest.shouldReinitializeRevivedTasksInAnyState" in stdout:
            return "TP(?72)"
        if "DefaultTaskExecutorTest.shouldUnassignTaskWhenRequired" in stdout:
            return "TP(?251)"
        if "DefaultStateUpdaterTest.shouldRestoreActiveStatefulTaskThenUpdateStandbyTaskAndAgainRestoreActiveStatefulTask" in stdout:
            return "TP(?134)"
        if "DefaultTaskExecutorTest.shouldRespectPunctuationDisabledByTaskExecutionMetadata" in stdout:
            return "TP(?257)"
        if "KafkaStreamsTest.shouldNotBlockInCloseForZeroDuration" in stdout:
            return "TP(?166)"
        if "KafkaStreamsTest.shouldNotAddThreadWhenError" in stdout:
            return "TP(?218)"
        if "DefaultTaskExecutorTest.shouldSetUncaughtStreamsException" in stdout:
            return "TP(?249)"
        if "DefaultStateUpdaterTest.shouldAddFailedTasksToQueueWhenUncaughtExceptionIsThrown" in stdout:
            return "TP(?96)"
        if "DefaultTaskExecutorTest.shouldShutdownTaskExecutor" in stdout:
            return "TP(?255)"
        if "GlobalStreamThreadTest.shouldThrowStreamsExceptionOnStartupIfExceptionOccurred" in stdout:
            return "TP(?276)"
        if "DefaultTaskExecutorTest.shouldClearTaskTimeoutOnProcessed" in stdout:
            return "TP(Time)"
        if "DefaultTaskExecutorTest.shouldUnassignTaskWhenNotProgressing" in stdout:
            return "TP(?260)"
        if "KafkaStreamsTest.shouldReturnFalseOnCloseWhenThreadsHaventTerminated" in stdout:
            return "TP(?176)"
        if "DefaultStateUpdaterTest.shouldGetTasksFromRestoredActiveTasks" in stdout:
            return "TP(?92)"
        if "shouldNotFailWhenCreatingTaskDirectoryInParallel" in stdout:
            return "TP(?157)"
        if "DefaultTaskExecutorTest.shouldProcessTasks" in stdout:
            return "TP(?253)"
        return None
        # print(stdout)
        # exit(0)

    def bug_classify(self, run_folder: str):
        stdout = open(os.path.join(run_folder, "stdout.txt")).read()
        if self.benchmark == "lucene":
            return self.lucene_bug_classify(stdout)
        if self.benchmark == "kafka":
            return self.kafka_bug_classify(stdout)
        return "N/A"

    def read_time(self, path: str) -> float:
        time_path = os.path.join(path, "time.txt")
        if not os.path.exists(time_path):
            return 0
        with open(time_path) as f:
            text = f.read()
            match = self.user_time_pattern.search(text)
            user_time = float(match.group(1))
            match = self.sys_time_pattern.search(text)
            sys_time = float(match.group(1))
            return user_time + sys_time

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
                total_iteration = int(
                    text.strip().split("\n")[-2].split(":")[1]) + 1
            elif self.tech == "jpf":
                stdout = open(os.path.join(
                    run_folder, "stdout.txt")).readlines()
                total_iteration = -1
                for line in reversed(stdout):
                    if line.startswith("paths ="):
                        total_iteration = int(line.split("=")[-1].strip())
                        break
                if error_type == "Error Found" and total_iteration == -1:
                    total_iteration = 1
            else:
                stdout = open(os.path.join(
                    run_folder, "stdout.txt")).readlines()
                total_iteration = -1
                for line in reversed(stdout):
                    if line.startswith("Starting iteration"):
                        total_iteration = int(line.split(" ")[-1].strip()) + 1
                        break
            bug_type = "N/A"

            if error_type == "No Error" and float(value) >= 600:
                error_result = "NoError"
            elif error_type == "Error Found":
                error_result = "Error"
                bug_type = self.bug_classify(run_folder)
                if bug_type == "Run failure":
                    bug_type = "N/A"
                    error_result = "Failure"
                else:
                    if "Time" in bug_type:
                        if "FP" in bug_type:
                            bug_type = "Time (FP)"
                        else:
                            bug_type = "Time"
                    else:
                        bug_type = "TP"
            else:
                error_result = "Failure"
            summary_file.write(
                f"{self.trial},{self.read_time(run_folder)},{folder},{error_result},{total_iteration},{bug_type}\n")

    def load_csv(self) -> pd.DataFrame:
        result_folder = os.path.join(self.path, "results")
        if not os.path.exists(result_folder):
            raise Exception("No results folder found")
        return pd.read_csv(
            os.path.join(result_folder, "summary.csv"), names=["trial", "time", "id", "error", "iter", "type"]
        )


class BenchmarkSuite:
    def __init__(self, path: str):
        self.benchmarks: List[BenchResult] = []
        self.path = os.path.abspath(path)
        for tech in os.listdir(self.path):
            tech_folder = os.path.join(self.path, tech)
            if os.path.exists(os.path.join(tech_folder, "iter-0")):
                for i in range(4):
                    trial_folder = os.path.join(tech_folder, f"iter-{i}")
                    self.benchmarks.append(BenchResult(trial_folder, True))
                # for trial in os.listdir(tech_folder):
                #     trial_folder = os.path.join(tech_folder, trial)
                #     self.benchmarks.append(BenchResult(trial_folder, True))
            else:
                print(tech_folder)
                self.benchmarks.append(BenchResult(tech_folder, False))

    def to_aggregated_dataframe(self) -> pd.DataFrame:
        data = []
        for bench in self.benchmarks:
            bench.to_csv()
            df = bench.load_csv()
            df["Technique"] = self.name_remap(bench.tech)
            data.append(df)
        return pd.concat(data, ignore_index=True)

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

    def generate_bug_table(self):
        df = self.to_aggregated_dataframe()
        pivot_df = df.pivot_table(values='id', index='Technique', columns='error', aggfunc='count', fill_value=0).reset_index().set_index("Technique")
        error_data = df.pivot_table(values="id", index='Technique', columns='type', aggfunc='count', fill_value=0).reset_index().set_index("Technique")
        result = pd.concat([pivot_df, error_data], axis=1).fillna(0).astype(int).reset_index()
        if "Time (FP)" not in result:
            result["Time (FP)"] = 0
        result['Time (FP)'] = result.apply(lambda row: f"{row['Time'] + row['Time (FP)']} ({row['Time (FP)']})", axis=1)
        result.drop(columns=["Time"], inplace=True)
        return result.rename(columns={
            "NoError": "Success",
            "Failure": "Failure",
            "TP": "TP",
        }).drop(columns=["Error"])

    def generate_search_space_table(self):
        df = self.to_aggregated_dataframe()
        df = df[df["error"] == "Error"]
        df = df.groupby(['Technique', 'id'])['iter'].mean().reset_index()
        fig, ax = plt.subplots()
        for key, grp in df.groupby(['id']):
            ax.plot(grp['id'], grp['iter'], linestyle='-', color='#42f5d7', zorder=1)
        sns.scatterplot(data=df, x="id", y="iter", hue="Technique", style="Technique", ax=ax, zorder=2, s=50)
        ax.set_yscale("log")
        ax.set_xlabel("Bug ID")
        ax.set_ylabel("Executions to find bug")
        ax.legend(title="")
        ax.set_xticklabels([])
        return ax

    def generate_exec_speed_table(self):
        df = self.to_aggregated_dataframe()
        df = df[df["error"] != "Failure"]
        df["exec"] = df["iter"] / df["time"]
        df = df.groupby(['Technique', 'id'])['exec'].mean().reset_index()
        fig, ax = plt.subplots()
        for key, grp in df.groupby(['id']):
            ax.plot(grp['id'], grp['exec'], linestyle='-', color='#42f5d7', zorder=1)
        sns.scatterplot(data=df, x="id", y="exec", hue="Technique", style="Technique", ax=ax, zorder=2, s=50)
        ax.set_yscale("log")
        ax.set_xlabel("Bug ID")
        ax.set_ylabel("\# Execution Per Second")
        ax.legend(title="")
        ax.set_xticklabels([])
        return ax

    def to_aggregated_fig(self, measurement: str) -> matplotlib.axes.Axes:
        df = self.to_aggregated_dataframe()
        df = df[df["error"] == "Error"]
        df['time'] = df['time'].astype(float)
        df_grouped = df
        df_grouped['sum'] = df_grouped.groupby(['Technique', 'trial'])[
            'time'].rank(method='max')
        df_grouped['sum'] = df_grouped['sum'].astype(float)
        df_grouped = df_grouped.drop(["type", "iter", "error", "id"], axis=1)
        df_grouped = df_grouped.groupby(
            ['time', 'trial', 'Technique'], as_index=False)['sum'].max()
        unique_combinations = df_grouped[['Technique', 'trial']].drop_duplicates()
        new_rows = pd.DataFrame(
            {'time': 0, 'trial': unique_combinations['trial'], 'Technique': unique_combinations['Technique'], 'sum': 0})
        df_grouped = pd.concat([new_rows, df_grouped], ignore_index=True)
        display(df_grouped[df_grouped['time'] == df_grouped['time'].max()])

        # # Function to interpolate 'sum' within each group efficiently
        def interpolate_sum(group):
            time_index = np.arange(df_grouped['time'].min(), df_grouped['time'].max(), 0.01)
            group = group.set_index('time').reindex(time_index)
            group['sum'] = group['sum'].ffill()
            group['Technique'] = group['Technique'].ffill()
            group['trial'] = group['trial'].ffill()
            time_index = np.arange(df_grouped['time'].min(), df_grouped['time'].max()+1, 1)
            group = group.reset_index().rename(columns={'index': 'time'})
            # Reindex the group to include all time points
            group = group.set_index('time').reindex(time_index)
            group = group.reset_index().rename(columns={'index': 'time'})
            return group
        df_grouped = df_grouped.groupby(['trial', 'Technique']).apply(interpolate_sum).reset_index(drop=True)
        ax = sns.lineplot(data=df_grouped, x="time", y="sum", hue="Technique",
                          linewidth=2, markers=True, errorbar='sd', estimator='mean', err_style='band')
        ax.set_xlabel('Seconds')
        ax.set_ylabel('Cumulative \# of Bugs')
        ax.legend(title="")
        return ax