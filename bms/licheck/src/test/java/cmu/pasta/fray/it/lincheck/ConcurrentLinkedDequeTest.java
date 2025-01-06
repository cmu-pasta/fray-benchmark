package cmu.pasta.fray.it.lincheck;

import java.util.concurrent.ConcurrentLinkedDeque;

import static org.junit.jupiter.api.Assertions.assertFalse;

public class ConcurrentLinkedDequeTest {
    public static int t1Value = 0;
    public static int t2Value = 0;

    public static void main(String[] args) throws InterruptedException {
        t1Value = 0;
        t2Value = 0;
        ConcurrentLinkedDeque<Integer> deque = new ConcurrentLinkedDeque<>();
        Thread t1 = new Thread(() -> {
            deque.addLast(-6);
            t1Value = deque.peekFirst();
        });
        Thread t2 = new Thread(() -> {
            deque.addFirst(-8);
            t2Value = deque.pollLast();
        });
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        assertFalse(t1Value == -8 && t2Value == -8);
    }
}
