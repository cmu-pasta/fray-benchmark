package cmu.pasta.fray.it.lincheck;

import com.googlecode.concurrenttrees.common.KeyValuePair;
import com.googlecode.concurrenttrees.radix.ConcurrentRadixTree;
import com.googlecode.concurrenttrees.radix.node.concrete.DefaultCharArrayNodeFactory;

import java.util.Random;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class ConcurrentRadixTreeTest {
    static boolean aaInserted;
    static boolean abInserted;

    public static void main(String[] args) throws InterruptedException {
        ConcurrentRadixTree<Integer> map = new ConcurrentRadixTree<>(new DefaultCharArrayNodeFactory());
        aaInserted = false;
        abInserted = false;

        map.put("aaa", 2);
        Thread t1 = new Thread(() -> {
            map.put("aba", -6);
            Iterable<KeyValuePair<Integer>> result = map.getKeyValuePairsForKeysStartingWith("");
            for (KeyValuePair<Integer> p: result) {
                if (p.getKey().equals("aa")) {
                    aaInserted = true;
                }
                if (p.getKey().equals("ab")) {
                    abInserted = true;
                }
            }
        });

        Thread t2 = new Thread(() -> {
            map.put("ab", 4);
            map.put("aa", 5);
        });

        t1.start();
        t2.start();
        t1.join();
        t2.join();

        assertFalse(aaInserted && !abInserted);
    }
}
