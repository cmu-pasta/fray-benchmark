package org.pastalab.fray.timedoperationobserver

import com.sun.org.apache.xpath.internal.operations.Bool
import org.pastalab.fray.runtime.Delegate
import java.io.File
import java.time.Duration
import java.util.Date
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.concurrent.locks.Condition
import java.util.concurrent.locks.Lock

class Observer(val reportPath: String): Delegate() {
    val map = mutableMapOf<String, Boolean>()
    val registeredThread = mutableSetOf<Thread>()
    val milisList = mutableListOf<Long>()
    val sourceOfTimedOp = mutableListOf<String>()

    init {
        Runtime.getRuntime().addShutdownHook(object : Thread() {
            override fun run() {
                File(reportPath).writeText(map.keys.joinToString(",")
                        + "\n" + milisList.joinToString(",")
                        + "\n" + sourceOfTimedOp.joinToString(","))
            }
        })
    }

    override fun onThreadStart(t: Thread) {
        if (registeredThread.contains(Thread.currentThread())) {
            registeredThread.add(t)
        }
        super.onThreadStart(t)
    }

    val prefixes = listOf("org.apache.lucene", "org.apache.kafka", "com.google")
    fun log(milis: Long) {
        if (Thread.currentThread() !in registeredThread) {
            return
        }
        val stackTraces = Thread.currentThread().stackTrace

        for (i in stackTraces) {
            val prefix = prefixes.find { i.className.startsWith(it) }
            if (prefix != null) {
                sourceOfTimedOp.add("${i.className}#${i.methodName}")
                break
            }
        }
        val methodName = stackTraces[2].methodName
        map[methodName] = true
        milisList.add(milis)
    }

    override fun onConditionAwaitTime(`object`: Condition?, time: Long, unit: TimeUnit): Boolean {
        log(unit.toMillis(time))
        return super.onConditionAwaitTime(`object`, time, unit)
    }

    override fun onConditionAwaitNanos(`object`: Condition?, nanos: Long): Long {
        log(nanos / 1_000_000)
        return super.onConditionAwaitNanos(`object`, nanos)
    }

    override fun onConditionAwaitUntil(`object`: Condition?, deadline: Date?): Boolean {
        log(deadline!!.time - Date().time)
        return super.onConditionAwaitUntil(`object`, deadline)
    }

    override fun onLatchAwaitTimeout(latch: CountDownLatch?, timeout: Long, unit: TimeUnit): Boolean {
        log(unit.toMillis(timeout))
        return super.onLatchAwaitTimeout(latch, timeout, unit)
    }

    override fun onThreadParkNanos(nanos: Long) {
        log(nanos / 1_000_000)
        super.onThreadParkNanos(nanos)
    }

    override fun onThreadParkNanosWithBlocker(blocker: Any?, nanos: Long) {
        log(nanos / 1_000_000)
        super.onThreadParkNanosWithBlocker(blocker, nanos)
    }

    override fun onThreadParkUntilWithBlocker(blocker: Any?, until: Long) {
        log(until - System.currentTimeMillis())
        super.onThreadParkUntilWithBlocker(blocker, until)
    }

    override fun onThreadParkUntil(nanos: Long) {
        log(nanos / 1_000_000)
        super.onThreadParkUntil(nanos)
    }

    override fun onLockTryLockInterruptibly(l: Lock?, timeout: Long): Long {
        log(timeout)
        return super.onLockTryLockInterruptibly(l, timeout)
    }

    override fun onLockTryLockTimeout(l: Lock?, timeout: Long, unit: TimeUnit?): Boolean {
        log(unit!!.toMillis(timeout))
        return super.onLockTryLockTimeout(l, timeout, unit)
    }

    override fun onThreadSleepDuration(duration: Duration?) {
        log(duration!!.toMillis())
        super.onThreadSleepDuration(duration)
    }

    override fun onThreadSleepMillis(millis: Long) {
        log(millis)
        super.onThreadSleepMillis(millis)
    }

    override fun onThreadSleepMillisNanos(millis: Long, nanos: Int) {
        log(millis + nanos / 1_000_000)
        super.onThreadSleepMillisNanos(millis, nanos)
    }

}