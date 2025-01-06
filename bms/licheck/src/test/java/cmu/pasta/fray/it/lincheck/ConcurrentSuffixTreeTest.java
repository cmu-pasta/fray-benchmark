package cmu.pasta.fray.it.lincheck;

import com.googlecode.concurrenttrees.radix.node.concrete.DefaultCharArrayNodeFactory;
import com.googlecode.concurrenttrees.suffix.ConcurrentSuffixTree;

import static org.junit.jupiter.api.Assertions.assertFalse;

public class ConcurrentSuffixTreeTest {

    static boolean q1;
    static boolean q2;

    public static void main(String[] args) throws InterruptedException {
        ConcurrentSuffixTree<Integer> tree = new ConcurrentSuffixTree<>(new DefaultCharArrayNodeFactory());
        Thread t1 = new Thread(() -> {
            tree.put("baa", 5);
        });

        Thread t2 = new Thread(() -> {
            q1 = tree.getKeysContaining("baa").iterator().hasNext();
            q2 =  tree.getKeysContaining("aa").iterator().hasNext();
        });

        t1.start();
        t2.start();
        t1.join();
        t2.join();

        assertFalse(q1 && !q2);
    }
}
