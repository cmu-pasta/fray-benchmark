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
        self.error_pattern = re.compile(r"(No Error|Error Found|Run failed): (\d+\.\d+)")

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
            out = self.kafka_bug_classify(stdout)
            if not out:
                print(run_folder)
                print(stdout)
                exit(0)
                return "TP"
            return out

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
            if error_type == "No Error" and float(value) >= 600:
                summary_file.write(f"{folder},NoError,{value},{total_iteration},N/A\n")
            elif error_type == "Error Found":
                bug_type = self.bug_classify(run_folder)
                if bug_type != "Run failure":
                    summary_file.write(f"{folder},{bug_type[:2]},{value},{total_iteration},{bug_type}\n")
                else:
                    summary_file.write(f"{folder},Failure,{value},{total_iteration},N/A\n")
            else:
                summary_file.write(f"{folder},Failure,{value},{total_iteration},N/A\n")

    def load_csv(self) -> pd.DataFrame:
        result_folder = os.path.join(self.path, "results")
        if not os.path.exists(result_folder):
            raise Exception("No results folder found")
        return pd.read_csv(
            os.path.join(result_folder, "summary.csv"), names=["run", "error", "time", "iter", "type"]
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
            # bench.to_csv()
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
        df = df[df["error"] == "Error"]
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