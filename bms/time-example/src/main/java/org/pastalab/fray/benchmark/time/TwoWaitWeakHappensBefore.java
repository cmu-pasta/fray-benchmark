package org.pastalab.fray.benchmark.time;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

// Adopted from Guava GeneratedMonitorTest
// waitForUninterruptibly(nonfair)(10ms)UnsatisfiedBeforeAndWhileWaiting->Failure
public class TwoWaitWeakHappensBefore {
    public static void main(String[] args) throws InterruptedException {
        AtomicBoolean flag = new AtomicBoolean(true);
        CountDownLatch c = new CountDownLatch(1);
        Thread t = new Thread(() -> {
            try {
                flag.set(c.await(1, TimeUnit.MILLISECONDS));
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        });
        t.start();
        Thread.sleep(1000);
        assert(flag.get() == false);
    }
}
