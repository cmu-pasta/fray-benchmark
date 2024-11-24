package cmu.pasta.fray.it.lincheck;
import org.jctools.maps.NonBlockingHashMapLong;
import org.junit.jupiter.api.Test;

import java.util.Random;

import static org.junit.jupiter.api.Assertions.*;

public class NonBlockingHashMapLongTest {

    public static void main(String[] args) throws InterruptedException {
        NonBlockingHashMapLong<Integer> map = new NonBlockingHashMapLong<Integer>();
        map.putIfAbsent(2, 6);

        Thread t1 = new Thread(() -> {
            map.remove(2);
        });

        Thread t2 = new Thread(() -> {
            map.replace(2, 8);
        });

        t1.start();
        t2.start();

        t1.join();
        t2.join();

        assertNotEquals(8, map.get(2));
    }
}
