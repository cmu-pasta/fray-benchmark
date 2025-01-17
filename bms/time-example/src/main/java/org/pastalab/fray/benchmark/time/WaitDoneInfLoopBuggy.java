package org.pastalab.fray.benchmark.time;

import java.util.concurrent.atomic.AtomicBoolean;

public class WaitDoneInfLoopBuggy {
public static void main(String[] args) throws InterruptedException {
    AtomicBoolean isRunning = new AtomicBoolean(true);
    AtomicBoolean serviceDone = new AtomicBoolean(false);
    Thread t = new Thread(() -> {
        while (isRunning.get()) {
            // do some work
        }
        serviceDone.set(true);
    });
    t.start();
    while (!serviceDone.get()) {
        Thread.sleep(1000);
    }
    // Other code here...
    isRunning.set(false);
}
}
