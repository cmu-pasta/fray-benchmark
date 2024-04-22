package cmu.pasta.sfuzz.benchmark.sctbench.cs.hard;

public class Reorder100Bad {
    private static int iSet = 99;
    private static int iCheck = 1;

    private static volatile int a = 0;
    private static volatile int b = 0;

    public static void main(String[] args) {
        int i, err;
        a = 0;
        b = 0;

        Thread[] setPool = new Thread[iSet];
        Thread[] checkPool = new Thread[iCheck];

        for (i = 0; i < iSet; i++) {
            setPool[i] = new Thread(() -> {
                setThread();
            });
            setPool[i].start();
        }

        for (i = 0; i < iCheck; i++) {
            checkPool[i] = new Thread(() -> {
                checkThread();
            });
            checkPool[i].start();
        }

        for (i = 0; i < iSet; i++) {
            try {
                setPool[i].join();
            } catch (InterruptedException e) {
                System.err.println("pthread join error: " + e);
                System.exit(-1);
            }
        }

        for (i = 0; i < iCheck; i++) {
            try {
                checkPool[i].join();
            } catch (InterruptedException e) {
                System.err.println("pthread join error: " + e);
                System.exit(-1);
            }
        }
    }

    private static void setThread() {
        a = 1;
        b = -1;
    }

    private static void checkThread() {
        if (!((a == 0 && b == 0) || (a == 1 && b == -1))) {
            System.err.println("Bug found!");
            assert false;
        }
    }
}
