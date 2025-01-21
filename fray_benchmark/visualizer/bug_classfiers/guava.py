def guava_bug_classify(stdout: str, run_folder: str) -> str:
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
