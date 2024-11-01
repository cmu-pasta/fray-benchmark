package org.pastalab.fray.benchmark.fraybench.success;

import java.util.concurrent.atomic.AtomicBoolean;

public class SynchronizedMethod {

    private AtomicBoolean flag = new AtomicBoolean(false);
    private Boolean bugFound = false;

    public synchronized void method() {
        if (!flag.compareAndSet(false, true)) {
            bugFound = true;
        }
        flag.set(false);
    }

    public static void synchronizedMethod() {
        SynchronizedMethod test = new SynchronizedMethod();

        Thread t1 = new Thread(() -> {
            test.method();
        });
        t1.start();

        Thread t2 = new Thread(() -> {
            test.method();
        });
        t2.start();

        if (test.bugFound) {
            throw new RuntimeException("bug found");
        }
    }

    public static void main(String[] args) {
        synchronizedMethod();
    }
}
