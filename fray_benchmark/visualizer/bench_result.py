import os
import re
import shutil
from typing import List
import matplotlib.axis
import numpy as np

import matplotlib
import matplotlib.axes
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import json
from . import sns_config


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
        self.fray_error_pattern = re.compile(
            r"Error found at iter: (\d+).+Elapsed time: (\d+)"
        )
        self.fray_total_iter_pattern = re.compile(
            r"Run finished. Total iter: (\d+)"
        )
        self.jpf_time_pattern = re.compile(
            r"ms time:\s+(\d+)"
        )
        self.jpf_iter_pattern = re.compile(
            r",end=(\d+)"
        )

        self.user_time_pattern = re.compile(r"real (\d+\.\d+)")
        # self.sys_time_pattern = re.compile(r"sys (\d+\.\d+)")

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
        if "maxSeqNo must be greater or equal to " in stdout:
            return "TP(#13571)"
        if "vs maxMergeCount=" in stdout:
            return "TP(#13593)"
        if "FATAL src/Task.cc:1429:compute_trap_reasons" in stdout:
            return "Run failure"
        return None


    def kafka_bug_classify(self, stdout: str):
        if "DeadlockException" in stdout:
            if "onThreadParkNanos" in stdout or "onLatchAwaitTimeout" in stdout or "onConditionAwaitNanos" in stdout:
                print(run_folder)
                return "FP(Time)"
        if "DefaultStateUpdaterTest.shouldRecordMetrics" in stdout:
            # ignore
            return "TP(?90)"
        if "83/report" in stdout:
            return "TP(KAFKA-17162)"
        if "[FATAL src/Task.cc:1429:compute_trap_reasons()]" in stdout:
            return "Run failure"
        if "Condition not met within timeout" in stdout or "KafkaStreamsTest.shouldThrowOnCleanupWhileShuttingDownStreamClosedWithCloseOptionLeaveGroupFalse" in stdout:
            return "TP(Time)"
        if "shouldThrowIfAddingTasksWithSameId" in stdout:
            return "TP(KAFKA-17114)"
        if "Deadlock" in stdout and ("DefaultStateUpdater" in stdout or "DefaultTaskManager" in stdout):
            return "TP(KAFKA-17112)"
        if "StreamThreadTest$StateListenerStub.onChange" in stdout:
            return "TP(KAFKA-17354)"
        if "GlobalStreamThreadTest.shouldThrowStreamsExceptionOnStartupIfThereIsAStreamsException" in stdout:
            return "TP(KAFKA-17113)"
        if "DefaultTaskExecutorTest.shouldNotFlushOnException" in stdout:
            return "TP(?261)"
        if "StreamThreadTest.shouldReinitializeRevivedTasksInAnyState" in stdout:
            return "TP(KAFKA-17112)"
        if "DefaultTaskExecutorTest.shouldUnassignTaskWhenRequired" in stdout:
            return "TP(KAFKA-17371)"
        if "KafkaStreamsTest.shouldNotAddThreadWhenError" in stdout:
            return "TP(KAFKA-17379)"
        if "DefaultTaskExecutorTest.shouldSetUncaughtStreamsException" in stdout:
            return "TP(KAFKA-17394)"
        if "DefaultStateUpdaterTest.shouldAddFailedTasksToQueueWhenUncaughtExceptionIsThrown" in stdout:
            return "TP(KAFKA-17114)"
        if "GlobalStreamThreadTest.shouldThrowStreamsExceptionOnStartupIfExceptionOccurred" in stdout:
            return "TP(KAFKA-17113)"
        if "DefaultTaskExecutorTest.shouldUnassignTaskWhenNotProgressing" in stdout:
            return "TP(KAFKA-17394)"
        if "DefaultStateUpdaterTest.shouldGetTasksFromRestoredActiveTasks" in stdout or "DefaultStateUpdaterTest.verifyGetTasks" in stdout:
            return "TP(KAFKA-17402)"
        if "DefaultTaskManagerTest.shouldBlockOnAwait" in stdout:
            return "TP(KAFKA-17929)"
        if "DefaultStateUpdaterTest.shouldResume" in stdout or "DefaultStateUpdaterTest.shouldPause" in stdout or "DefaultStateUpdaterTest.shouldUpdate" in stdout or\
            "DefaultTaskExecutorTest.shouldPunctuate" in stdout or "Wanted but not invoked:" in stdout or "Wanted *at least* " in stdout:
            return "TP(KAFKA-17946)"
        # cannot reproduce
        if "shouldNotFailWhenCreatingTaskDirectoryInParallel" in stdout:
            return "TP(?157)"
        if "KafkaStreamsTest.should" in stdout and "AssertionFailedError: expected: <false> but was: <true>" in stdout:
            return "TP(Time)"
        if "KafkaStreamsTest.shouldThrowOnCleanupWhileShuttingDown" in stdout:
            return "TP(Time)"
        if "StreamThreadTest.shouldRecoverFromInvalidOffsetExceptionOnRestoreAndFinishRestore" in stdout:
            return "TP(Time)"
        if "StreamThreadTest.should" in stdout:
            return "TP(Time)"
        # if "DefaultTaskExecutorTest.shouldProcessTasks" in stdout:
        #     return "TP(Time)"
        print(stdout)
        return None

    def guava_bug_classify(self, stdout: str, run_folder: str) -> str:
        if "DeadlockException" in stdout:
            if "onThreadParkNanos" in stdout or "onLatchAwaitTimeout" in stdout or "onConditionAwaitNanos" in stdout:
                print(run_folder)
                return "FP(Time)"
        folder_id = int(run_folder.split("/")[-1])
        if folder_id <= 1194 and folder_id >= 1190:
            return "Run failure"
        if (folder_id <= 1115 and folder_id >= 1084) or \
              (folder_id == 108) or \
                (folder_id <= 1194 and folder_id >= 1135) or \
                (folder_id <= 86 and folder_id >= 74) or \
                    (folder_id == 94):
            return "TP(#7319)"
        if run_folder.endswith("/1123"):
            return "Run failure"
        if "timeout" in stdout or folder_id == 1128 or "GeneratedMonitorTest" in stdout:
            return "TP(Time)"
        if "ClosingFuture" in stdout:
            return "TP(Time)"
        if "/rr/" in run_folder:
            return "Run failure"
        if "QueuesTest" in stdout:
            return "TP(Time)"
        # print(stdout)
        # exit(0)
        return "N/A"
        pass

    def bug_classify(self, run_folder: str, stdout: str):
        if self.benchmark == "lucene":
            return self.lucene_bug_classify(stdout)
        if self.benchmark == "kafka":
            return self.kafka_bug_classify(stdout)
        if self.benchmark == "guava":
            result = self.guava_bug_classify(stdout, run_folder)
            # if "Time" in result:
            #     print(stdout)
            return result
        return "N/A"

    def read_time(self, path: str) -> float:
        time_path = os.path.join(path, "time.txt")
        if not os.path.exists(time_path):
            return 0
        with open(time_path) as f:
            text = f.read()
            match = self.user_time_pattern.search(text)
            user_time = float(match.group(1))
            # match = self.sys_time_pattern.search(text)
            # sys_time = float(match.group(1))
            return user_time
            # return user_time + sys_time

    def gather_time_stats(self):
        result_folder = os.path.join(self.path, "results")
        os.makedirs(result_folder, exist_ok=True)
        timed_op_summary = {}
        wait_time = []
        caller_list = []
        total = 0
        for folder in sorted(os.listdir(self.path)):
            if folder == "results":
                continue
            total += 1
            run_folder = os.path.join(self.path, folder)
            lines = open(os.path.join(run_folder, "timed-operations.txt")).readlines()
            if len(lines) < 3:
                continue
            timed_op_result = lines[0].strip()
            wait_time_result = lines[1].strip().split(",")
            callers = lines[2].strip().split(",")
            caller_list.extend(callers)
            for time in wait_time_result:
                wait_time.append(int(time))
            op_names = set()
            for timed_op in timed_op_result.split(","):
                if not timed_op:
                    continue
                op_name = timed_op
                if "Condition" in timed_op:
                    op_name = "Condition"
                if "Park" in timed_op:
                    op_name = "Park"
                if "onLock" in timed_op:
                    op_name = "Lock"
                op_names.add(op_name)
            for op_name in op_names:
                if op_name not in timed_op_summary:
                    timed_op_summary[op_name] = 0
                timed_op_summary[op_name] += 1
        timed_op_summary["total"] = total
        json.dump(timed_op_summary, open(os.path.join(result_folder, "timed-operations.json"), "w"))
        return timed_op_summary, wait_time, caller_list


    def to_csv(self):
        result_folder = os.path.join(self.path, "results")
        if os.path.exists(result_folder):
            shutil.rmtree(result_folder)
        os.makedirs(result_folder)
        summary_file = open(os.path.join(result_folder, "summary.csv"), "w")
        for folder in sorted(os.listdir(self.path)):
            if folder == "results":
                continue
            run_folder = os.path.join(self.path, folder)
            if self.tech == "rr" or self.tech == "jpf":
                stdout = open(os.path.join(
                    run_folder, "stdout.txt")).read()
            else:
                stdout = open(os.path.join(run_folder, "report", "fray.log")).read()
            total_iteration = -1
            first_bug_iter = -1
            first_bug_time = -1
            jpf_error = False
            if self.tech != "jpf":
                stdout = stdout.split("\n")
                for line in reversed(stdout):
                    if line.startswith("Starting iteration"):
                        total_iteration = int(line.split(" ")[-1].strip()) + 1
                        break
                    match = self.fray_total_iter_pattern.search(line)
                    if match:
                        total_iteration = int(match.groups()[0])
                        break
                for line in stdout:
                    match = self.fray_error_pattern.search(line)
                    if match:
                        first_bug_iter, first_bug_time = [int(x) for x in match.groups()]
                        if self.tech != "rr":
                            first_bug_iter += 1
                        break
            elif self.tech == "jpf":
                if "UnsupportedOperationException" in stdout or \
                    "NoSuchMethodException" in stdout or "FileNotFoundException" in stdout or\
                        "Null charset name" in stdout or "NoSuchMethodError" in stdout or\
                            "JPF out of memory" in stdout or\
                                "java.lang.NullPointerException: Calling 'startsWith(Ljava/lang/String;)Z' on null object" in stdout:
                        jpf_error = True
                stdout = stdout.split("\n")
                for line in reversed(stdout):
                    line = line.strip()
                    if line.startswith("paths ="):
                        total_iteration = int(line.split("=")[-1].strip())
                        break
                for line in stdout:
                    time_match = self.jpf_time_pattern.search(line)
                    if time_match:
                        first_bug_time = time_match.group(1)
                    iter_match = self.jpf_iter_pattern.search(line)
                    if iter_match:
                        first_bug_iter = int(iter_match.group(1)) + 1
                        break
            bug_type = "N/A"
            if jpf_error:
                error_result = "Failure"
            elif first_bug_iter == -1:
                error_result = "NoError"
            else:
                error_result = "Error"
            stdout = "\n".join(stdout)
            if "Error found" in stdout:
                bug_type = self.bug_classify(run_folder, stdout)
                error_result = "Error"
            summary_file.write(
                f"{self.benchmark}-{folder},{self.trial},{error_result},{bug_type},{first_bug_time},{first_bug_iter},{self.read_time(run_folder)},{total_iteration}\n")

    def load_csv(self) -> pd.DataFrame:
        result_folder = os.path.join(self.path, "results")
        if not os.path.exists(result_folder):
            print(f"Folder {result_folder} not found")
            raise Exception("No results folder found")
        df = pd.read_csv(
            os.path.join(result_folder, "summary.csv"), names=["id", "trial", "error", "type", "bug_time", "bug_iter", "total_time", "total_iter"]
        )
        return df


class BenchmarkSuite:
    def __init__(self, paths: List[str]):
        self.benchmarks: List[BenchResult] = []
        for path in paths:
            self.path = os.path.abspath(path)
            for tech in os.listdir(self.path):
                # if "java" not in tech:
                #     continue
                tech_folder = os.path.join(self.path, tech)
                if os.path.exists(os.path.join(tech_folder, "iter-0")):
                    for i in range(1):
                        trial_folder = os.path.join(tech_folder, f"iter-{i}")
                        self.benchmarks.append(BenchResult(trial_folder, True))
                    # for trial in os.listdir(tech_folder):
                    #     trial_folder = os.path.join(tech_folder, trial)
                    #     self.benchmarks.append(BenchResult(trial_folder, True))
                else:
                    self.benchmarks.append(BenchResult(tech_folder, False))
    def to_timed_stats(self):
        for bench in self.benchmarks:
            timed_op_result, wait_time_result, callers = bench.gather_time_stats()
            print(set(callers))
            percentaged = {}
            for key in timed_op_result:
                if key == "total":
                    continue
                print(key, timed_op_result[key])
                percentaged[key] = timed_op_result[key] / timed_op_result["total"]
            axis = sns.barplot(x=list(percentaged.keys()), y=list(percentaged.values()))
            axis.set_title(f"{bench.benchmark}")
            axis.set_xlabel("Operation")
            axis.set_ylabel("Percentage")
            plt.show()
            axis = sns.histplot(wait_time_result, log_scale=True)
            axis.set_title(f"{bench.benchmark}")
            axis.set_xlabel("Timeout (ms)")

    def to_aggregated_dataframe(self) -> pd.DataFrame:
        data = []
        for bench in self.benchmarks:
            # bench.to_csv()
            df = bench.load_csv()
            df["Technique"] = self.name_remap(bench.tech)
            data.append(df)
        df = pd.concat(data, ignore_index=True)
        return df

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
        return name.upper()

    def generate_bug_table(self):
        df = self.to_aggregated_dataframe()
        df = df.replace(r'^TP\(Time\)', 'Time', regex=True)
        df = df.replace(r'^TP\(.+', 'TP', regex=True)
        df = df.replace(r'^FP\(Time\)', 'Time (FP)', regex=True)
        pivot_df = df.pivot_table(values='id', index='Technique', columns='error', aggfunc='count', fill_value=0).reset_index().set_index("Technique")
        error_data = df.pivot_table(values="id", index='Technique', columns='type', aggfunc='count', fill_value=0).reset_index().set_index("Technique")
        result = pd.concat([pivot_df, error_data], axis=1).fillna(0).astype(int).reset_index()
        if "Time (FP)" not in result:
            result["Time (FP)"] = 0
        if "Time" not in result:
            result["Time"] = 0
        result["Test Run"] = result["Time (FP)"] + result["Time"] + result["NoError"] + result["TP"]
        result["Failure"] = result["TP"]
        result['Time (FP)'] = result.apply(lambda row: f"{row['Time'] + row['Time (FP)']} ({row['Time (FP)']})", axis=1)
        result.drop(columns=["Time", "TP", "NoError", "Error"], inplace=True)
        return result[["Technique", "Test Run", "Failure", "Time (FP)"]]

    def generate_search_space_table(self) -> matplotlib.axis.Axis:
        df = self.to_aggregated_dataframe()
        df = df[df["error"] == "Error"]
        return self.generate_aggregated_plot(df, "bug_iter")

    def generate_aggregated_plot(self, df: pd.DataFrame, column: str) -> matplotlib.axis.Axis:
        df = df.groupby(['Technique', 'id'])[column].mean().reset_index()
        fray_key = "$\\textsc{Fray}$-Random"
        all_bms_sorted = df[df["Technique"] == fray_key].sort_values(by=column)["id"].to_list()
        for id in df["id"].to_list():
            if id not in all_bms_sorted:
                all_bms_sorted.append(id)
        all_bms_sorted = list(dict.fromkeys(all_bms_sorted))

        ylim = df[column].max() + (1000 if column == "bug_iter" else 3000)
        sct_list = []
        jc_list = []
        for key in all_bms_sorted:
            if "sctbench" in key:
                sct_list.append(key)
            else:
                jc_list.append(key)
        print(sct_list)
        print(jc_list)
        all_bms_sorted = sct_list + jc_list
        xlim = len(all_bms_sorted) + 0.5
        df['id'] = df['id'].apply(lambda value: all_bms_sorted.index(value))
        fig, ax = plt.subplots()
        for key, grp in df.groupby(['id']):
            ax.plot(grp['id'], grp[column], linestyle='-', color='#42f5d7', zorder=1)
        sns.scatterplot(data=df, x="id", y=column, hue="Technique", style="Technique", ax=ax, zorder=2, s=80, alpha=0.9, markers=['s', "^", "P"])
        ax.fill_between([-1, len(sct_list) - 0.5], y1=[ylim, ylim], alpha=0.3, facecolor=sns_config.colors[-1], linewidth=0.0, label="SCTBench")
        ax.fill_between([len(sct_list) - 0.5, xlim], y1=[ylim, ylim], alpha=0.3, linewidth=0.0, facecolor=sns_config.colors[-2], label="JaConTeBe")
        # ax.legend([f1, f2], ["SCTBench", "JaConTeBe"])
        if column == "exec":
            ax.set_xlabel("Program (Total 53 from SCTBench and JaConTeBe)")
        else:
            ax.set_xlabel("Bug (Total 53 from SCTBench and JaConTeBe)")

        if column == "exec":
            ax.set_ylabel("Executions per second")
        else:
            ax.set_ylabel("Executions to find bug")
        ax.set_yscale("log")
        ticks = [0.1, 1, 10, 100, 1000]
        tick_labels = ["0.1", "1", "10", "100", "1000"]
        if column == "bug_iter":
            ticks = ticks[1:]
            tick_labels = tick_labels[1:]
        ax.set_yticks(ticks)
        ax.set_yticklabels(tick_labels)
        ax.legend(title="", bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncols=5, mode="expand", borderaxespad=0., labelspacing=0.0,
                      handlelength=1.0, facecolor='white', edgecolor='black')
        ax.set(xlim=(-1, xlim))
        ax.set(ylim=(ticks[0]-0.5, ylim))

        ax.set_xticklabels([])
        return ax
        pass

    def generate_exec_speed_table(self) -> matplotlib.axis.Axis:
        df = self.to_aggregated_dataframe()
        df = df[df["error"] != "Failure"]
        df["exec"] = df["total_iter"] / df["total_time"]
        df = df.sort_values(by="exec")
        df_reduced = df[['id', 'trial', 'Technique', 'exec']]
        df_pivot = df_reduced.pivot_table(index=['id', 'trial'], columns='Technique', values='exec').reset_index()
        fray_key = "$\\textsc{Fray}$-Random"
        candidate_key = "JPF-Random"
        df_pivot.dropna(subset=[fray_key, candidate_key], inplace=True)
        return self.generate_aggregated_plot(df, "exec")

    def generate_bug_over_time_fig(self, measurement: str) -> matplotlib.axes.Axes:
        df = self.to_aggregated_dataframe()
        total_bugs =df["id"].nunique()
        df = df[df["error"] == "Error"]
        df_grouped = df
        df_grouped['sum'] = df_grouped.groupby(['Technique', 'trial'])[
            'bug_time'].rank(method='max')
        df_grouped['sum'] = df_grouped['sum'].astype(float)
        # df_grouped = df_grouped.drop(["type", "bug_iter", "error", "id"], axis=1)
        df_grouped = df_grouped.groupby(
            ['bug_time', 'trial', 'Technique'], as_index=False)['sum'].max()
        unique_combinations = df_grouped[['Technique', 'trial']].drop_duplicates()
        new_rows = pd.DataFrame(
            {'bug_time': 0, 'trial': unique_combinations['trial'], 'Technique': unique_combinations['Technique'], 'sum': 0})
        df_grouped = pd.concat([new_rows, df_grouped], ignore_index=True)
        min_time = df_grouped['bug_time'].min()
        max_time = 600 * 1000
        # # Function to interpolate 'sum' within each group efficiently
        def interpolate_sum(group):
            time_index = np.arange(min_time, max_time, 1)
            group = group.set_index('bug_time').reindex(time_index)
            group['sum'] = group['sum'].ffill()
            group['Technique'] = group['Technique'].ffill()
            group['trial'] = group['trial'].ffill()
            time_index = np.arange(min_time, max_time+1, 100)
            group = group.reset_index().rename(columns={'index': 'bug_time'})
            # Reindex the group to include all time points
            group = group.set_index('bug_time').reindex(time_index)
            group = group.reset_index().rename(columns={'index': 'bug_time'})
            group['bug_time'] = group["bug_time"] / 1000
            return group
        df_grouped = df_grouped.groupby(['trial', 'Technique']).apply(interpolate_sum).reset_index(drop=True)
        ax = sns.lineplot(data=df_grouped, x="bug_time", y="sum", hue="Technique",
                          linewidth=2, errorbar='sd', estimator='mean', err_style='band', style="Technique")
        ax.plot([0, df_grouped['bug_time'].max() + 1], [total_bugs, total_bugs], "r-.", label="Total Bugs")
        ax.set_xscale("log")
        ticks = [0.1, 1, 10, 100, 600]
        tick_labels = ["0.1", "1", "10", "100", "600"]
        ax.set_xticks(ticks)
        ax.set_xticklabels(tick_labels)

        ax.set_xlabel('Seconds')
        ax.set_ylabel('Cumulative \# of Bugs')
        ax.legend(title="", bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncols=4, mode="expand", borderaxespad=0.)
        return ax