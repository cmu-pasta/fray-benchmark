package org.pastalab.fray.benchmark.fraybench.success;

import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

public class ThreadPoolShutdown {
    public static void threadPoolShutdown() {
        ExecutorService executorService = Executors.newFixedThreadPool(10);
        executorService.execute(new Runnable() {
            public void run() {
                System.out.println("Asynchronous task");
            }
        });
        executorService.execute(new Runnable() {
            public void run() {
                System.out.println("Asynchronous task");
            }
        });
        executorService.execute(new Runnable() {
            public void run() {
                System.out.println("Asynchronous task");
            }
        });
        executorService.shutdown();
    }

    public static void main(String[] args) {
        threadPoolShutdown();
    }
}
