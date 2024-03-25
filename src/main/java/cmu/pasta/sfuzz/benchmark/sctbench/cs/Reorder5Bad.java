package cmu.pasta.sfuzz.benchmark.sctbench.cs;

// Translated from: https://github.com/mc-imperial/sctbench/blob/d59ab26ddaedcd575ffb6a1f5e9711f7d6d2d9f2/benchmarks/concurrent-software-benchmarks/reorder_5_bad.c

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class Reorder5Bad {

  static int iSet = 4;
  static int iCheck = 1;

  static int a = 0;
  static int b = 0;

  public static void main(String[] args) {
    int i;

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
      int finalI = i;
      setPool[i] = new Thread(() -> setThread(finalI));
      setPool[i].start();
    }

    for (i = 0; i < iCheck; i++) {
      int finalI = i;
      checkPool[i] = new Thread(() -> checkThread(finalI));
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

  static void setThread(int param) {
    a = 1;
    b = -1;
  }

  static void checkThread(int param) {
    if (!(a == 0 && b == 0) && !(a == 1 && b == -1)) {
      System.err.println("Bug found!");
      assert false;
    }
  }
}