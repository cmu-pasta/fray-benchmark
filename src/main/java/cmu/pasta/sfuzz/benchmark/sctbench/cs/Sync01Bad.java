package cmu.pasta.sfuzz.benchmark.sctbench.cs;

// Translated from: https://github.com/mc-imperial/sctbench/blob/d59ab26ddaedcd575ffb6a1f5e9711f7d6d2d9f2/benchmarks/concurrent-software-benchmarks/sync01_bad.c

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.Condition;

public class Sync01Bad {
    static final int N = 1;
    
    static int num;
    
    static Lock m = new ReentrantLock();
    static Condition empty = m.newCondition();
    static Condition full = m.newCondition();
    
    static void thread1() {
        m.lock();
        try {
            while (num > 0) {
                empty.await();  // BAD: deadlock
            }
            num++;
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            m.unlock();
            full.signal();
        }
    }
    
    static void thread2() {
        m.lock();
        try {
            while (num == 0) {
                full.await();
            }
            // num--;
            // System.out.println("consume ....");
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            m.unlock();
            empty.signal();
        }
    }
    
    public static void main(String[] args) {
        num = 1;
        
        Thread t1 = new Thread(() -> thread1());
        Thread t2 = new Thread(() -> thread2());
        
        t1.start();
        t2.start();
        
        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}