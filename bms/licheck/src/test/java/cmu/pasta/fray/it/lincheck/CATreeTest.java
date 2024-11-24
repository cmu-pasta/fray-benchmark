package cmu.pasta.fray.it.lincheck;

import cmu.pasta.fray.it.catreemapavl.CATreeMapAVL;
import org.junit.jupiter.api.Test;

import java.util.Random;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class CATreeTest {

    public static void main(String[] args) throws InterruptedException {
        CATreeMapAVL<Long, Integer> map = new CATreeMapAVL<>();
        Thread t1 = new Thread(() -> {
            map.clear();
            map.put(3L, 2);
        });
        Thread t2 = new Thread(() -> {
            map.clear();
        });
        t1.start();
        t2.start();
        t1.join();
        t2.join();
    }
}
