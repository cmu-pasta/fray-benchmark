package org.pastalab.fray.benchmark.time;

import java.util.concurrent.atomic.AtomicBoolean;

public class WaitDoneInfLoop {
    public static void main(String[] args) throws InterruptedException {
        AtomicBoolean isRunning = new AtomicBoolean(true);
        AtomicBoolean jobDone = new AtomicBoolean(false);
        Thread t = new Thread(() -> {
            while (isRunning.get()) {
                // do some work
                jobDone.set(true);
            }
        });

        t.start();
        while (!jobDone.get()) {
            Thread.sleep(1000);
        }
        isRunning.set(false);
    }
}
