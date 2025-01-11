package org.pastalab.fray.benchmark.time;

import java.util.concurrent.atomic.AtomicBoolean;

// Adopted from Kafka
public class WaitFinishTimeout {
    public static void main(String[] args) throws InterruptedException {
        AtomicBoolean flag = new AtomicBoolean(false);
        Thread t = new Thread(() -> {
            flag.set(true);
        });
        t.start();
        Thread.sleep(1000);
        assert(flag.get());
    }
}
