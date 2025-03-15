def lucene_bug_classify(stdout: str):
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
