package org.pastalab.fray.benchmark.fraybench.success;

import java.util.concurrent.atomic.AtomicBoolean;

public class ThreadJoin {
    public static void threadJoin() throws InterruptedException {
        AtomicBoolean flag = new AtomicBoolean(false);
        Thread t = new Thread(() -> {
            flag.set(true);
        });
        t.start();
        t.join();
        if (!flag.get()) {
            throw new RuntimeException("flag is false");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        threadJoin();
    }
}
