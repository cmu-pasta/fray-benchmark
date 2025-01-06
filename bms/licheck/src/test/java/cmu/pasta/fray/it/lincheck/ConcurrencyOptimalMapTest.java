package cmu.pasta.fray.it.lincheck;

import cmu.pasta.fray.it.concurrencyoptimaltreemap.ConcurrencyOptimalTreeMap;

public class ConcurrencyOptimalMapTest {

    public static void main(String[] args) throws InterruptedException {
        ConcurrencyOptimalTreeMap<Integer, Integer> map = new ConcurrencyOptimalTreeMap<>();

        Thread t1 = new Thread(() -> {
            map.putIfAbsent(1, 5);
        });

        Thread t2 = new Thread(() -> {
            map.putIfAbsent(3, 1);
        });

        t1.start();
        t2.start();
        t1.join();
        t2.join();
    }
}
