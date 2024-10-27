package org.pastalab.fray.benchmark.fraybench;

import org.pastalab.fray.core.scheduler.PCTScheduler;
import org.pastalab.fray.junit.annotations.ConcurrencyTest;

public class WaitNotifyOrderTest {

    @ConcurrencyTest(
            iteration = 1000,
            scheduler = PCTScheduler.class,
            expectedException = RuntimeException.class
    )
    public void rescheduleBeforeWaitReacquireMonitorLockTest() throws InterruptedException {
        WaitNotifyOrder test = new WaitNotifyOrder();
        test.rescheduleBeforeWaitReacquireMonitorLock();
    }

}