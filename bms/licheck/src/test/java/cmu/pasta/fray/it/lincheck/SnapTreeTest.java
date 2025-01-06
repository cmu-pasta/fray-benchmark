package cmu.pasta.fray.it.lincheck;

import cmu.pasta.fray.it.snaptree.SnapTreeMap;
import org.junit.jupiter.api.Test;

import java.util.Random;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class SnapTreeTest {

    public static void main(String[] args) throws InterruptedException {
        SnapTreeMap<Long, Integer> map = new SnapTreeMap<>();
        map.putIfAbsent(4L, 4);

        Thread t1 = new Thread(() -> {
            map.firstKey();
        });

        Thread t2 = new Thread(() -> {
            map.putIfAbsent(1L, 7);
            map.remove(4L);
        });

        Thread t3 = new Thread(() -> {
            map.putIfAbsent(5L, 6);
        });

        t1.start();
        t2.start();
        t3.start();

        t1.join();
        t2.join();
        t3.join();


    }
}
