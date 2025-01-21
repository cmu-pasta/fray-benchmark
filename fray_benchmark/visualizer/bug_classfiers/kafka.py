def kafka_bug_classify(stdout: str):
    if "shouldThrowOnCleanupWhileShuttingDownStreamClosedWithCloseOptionLeaveGroupFalse" in stdout:
        return "TP(KAFKA-18418)"
    if "DeadlockException" in stdout:
        if "onThreadParkNanos" in stdout or "onLatchAwaitTimeout" in stdout or "onConditionAwaitNanos" in stdout:
            return "FP(Time)"
    if "DefaultStateUpdaterTest.shouldRecordMetrics" in stdout:
        # ignore
        return "TP(?90)"
    if "83/report" in stdout:
        return "TP(KAFKA-17162)"
    if "[FATAL src/Task.cc:1429:compute_trap_reasons()]" in stdout:
        return "Run failure"
    if "Condition not met within timeout" in stdout:
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
        return "TP(KAFKA-18418)"
    if "KafkaStreamsTest.shouldThrowOnCleanupWhileShuttingDown" in stdout:
        return "TP(KAFKA-18418)"
    if "StreamThreadTest.shouldRecoverFromInvalidOffsetExceptionOnRestoreAndFinishRestore" in stdout:
        return "TP(Time)"
    if "StreamThreadTest.should" in stdout:
        return "TP(Time)"
    # if "DefaultTaskExecutorTest.shouldProcessTasks" in stdout:
    #     return "TP(Time)"
    print(stdout)
    return None