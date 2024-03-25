package cmu.pasta.sfuzz.benchmark.sctbench.cs;

// Translated from: https://github.com/mc-imperial/sctbench/blob/d59ab26ddaedcd575ffb6a1f5e9711f7d6d2d9f2/benchmarks/concurrent-software-benchmarks/reorder_20_bad.c

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class Reorder20Bad {
    
    private static int iSet = 10;
    private static int iCheck = 10;

    private static int a = 0;
    private static int b = 0;

    private static Lock lock = new ReentrantLock();
    private static Condition cond = lock.newCondition();

    private static void yield() {
        lock.lock();
        try {
            cond.awaitNanos(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }

    public static void main(String[] args) {
        int i, err;

        if (args.length != 1) {
            if (args.length != 3) {
                System.err.println("./reorder <param1> <param2>");
                System.exit(-1);
            } else {
                iSet = Integer.parseInt(args[1]);
                iCheck = Integer.parseInt(args[2]);
            }
        }

        Thread[] setPool = new Thread[iSet];
        Thread[] checkPool = new Thread[iCheck];

        for (i = 0; i < iSet; i++) {
            final int idx = i;
            setPool[i] = new Thread(() -> setThread(idx));
            setPool[i].start();
        }

        for (i = 0; i < iCheck; i++) {
            final int idx = i;
            checkPool[i] = new Thread(() -> checkThread(idx));
            checkPool[i].start();
        }

        for (i = 0; i < iSet; i++) {
            try {
                setPool[i].join();
            } catch (InterruptedException e) {
                System.err.println("Thread join error: " + e);
                System.exit(-1);
            }
        }

        for (i = 0; i < iCheck; i++) {
            try {
                checkPool[i].join();
            } catch (InterruptedException e) {
                System.err.println("Thread join error: " + e);
                System.exit(-1);
            }
        }
    }

    private static void setThread(int param) {
        a = 1;
        b = -1;
    }

    private static void checkThread(int param) {
        if (!(a == 0 && b == 0) && !(a == 1 && b == -1)) {
            System.err.println("Bug found!");
            assert false;
        }
    }
}