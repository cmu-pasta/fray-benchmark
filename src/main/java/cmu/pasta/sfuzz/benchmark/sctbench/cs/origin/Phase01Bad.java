package cmu.pasta.sfuzz.benchmark.sctbench.cs.origin;

// Translated from: https://github.com/mc-imperial/sctbench/blob/d59ab26ddaedcd575ffb6a1f5e9711f7d6d2d9f2/benchmarks/concurrent-software-benchmarks/phase01_bad.c

import java.util.concurrent.locks.ReentrantLock;

public class Phase01Bad {
  
  static ReentrantLock x = new ReentrantLock(); 
  static ReentrantLock y = new ReentrantLock();

  static void thread1() {
    x.lock(); // BAD: deadlock
    x.unlock();  
    x.lock();
    // x.unlock();

    y.lock();
    y.unlock();
    y.lock();
    y.unlock();
  }

  public static void main(String[] args) {
    Thread t1 = new Thread(() -> thread1());
    Thread t2 = new Thread(() -> thread1());

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