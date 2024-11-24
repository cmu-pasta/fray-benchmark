package cmu.pasta.fray.it.lincheck;

import cmu.pasta.fray.it.semaphore.Semaphore;

public class AbstractQueueSynchronizerTest {


    public static void main(String[] args) throws InterruptedException {

        Semaphore sem = new Semaphore(1, true);
        Thread t1 = new Thread(() -> {
            try {
                sem.acquire();
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            try {
                sem.acquire();
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        });
        Thread t2 = new Thread(() -> {
            try {
                sem.acquire();
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            try {
                sem.acquire();
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        });
        t1.start();
        t2.start();
        sem.release();
        t1.join();
        t2.join();
    }
}
