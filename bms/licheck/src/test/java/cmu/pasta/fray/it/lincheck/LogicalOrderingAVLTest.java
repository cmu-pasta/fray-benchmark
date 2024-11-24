package cmu.pasta.fray.it.lincheck;

import cmu.pasta.fray.it.logicalorderingavl.LogicalOrderingAVL;

public class LogicalOrderingAVLTest {

    public static void main(String[] args) throws InterruptedException {
        LogicalOrderingAVL<Integer, Integer> map = new LogicalOrderingAVL<>();
        map.putIfAbsent(5, 2);
        map.put(3, 5);

        Thread t1 = new Thread(() -> {
            map.get(4);
            map.put(4, 5);
        });

        Thread t2 = new Thread(() -> {
            map.remove(5);
        });

        t1.start();
        t2.start();

        t1.join();
        t2.join();
    }
}
