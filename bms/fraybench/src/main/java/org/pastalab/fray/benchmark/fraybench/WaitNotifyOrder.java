package org.pastalab.fray.benchmark.fraybench;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicBoolean;

public class WaitNotifyOrder {

    public void notifyOrder() throws InterruptedException {
        Object o = new Object();
        CountDownLatch latch = new CountDownLatch(2);
        AtomicBoolean flag = new AtomicBoolean(false);
        Thread t1 = new Thread(() -> {
            synchronized (o) {
                try {
                    latch.countDown();
                    o.wait();
                    flag.set(true);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        });
        Thread t2 = new Thread(() -> {
            synchronized (o) {
                try {
                    latch.countDown();
                    o.wait();
                    if (!flag.get()) {
                        throw new RuntimeException("flag is false");
                    }
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        });
        t1.start();
        t2.start();
        latch.await();
        synchronized (o) {
            o.notify();
            o.notify();
        }
    }


    public void rescheduleBeforeWaitReacquireMonitorLock() throws InterruptedException {
        Object o = new Object();
        CountDownLatch latch = new CountDownLatch(1);
        AtomicBoolean flag = new AtomicBoolean(false);
        Thread t = new Thread(() -> {
            synchronized (o) {
                try {
                    latch.countDown();
                    o.wait();
                    flag.set(true);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        t.start();
        latch.await(); // Wait for the thread to start
        synchronized (o) {
            o.notify();
        }
        Thread.yield();
        synchronized (o) {
            if (!flag.get()) {
                throw new RuntimeException("flag is false");
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        WaitNotifyOrder test = new WaitNotifyOrder();
//        test.rescheduleBeforeWaitReacquireMonitorLock();
        test.notifyOrder();
    }
}