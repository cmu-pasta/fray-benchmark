package org.pastalab.fray.benchmark.fraybench.fail;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.IntStream;

public class GlobalIntStream {
    public static void intStreamTest() {
        AtomicInteger x = new AtomicInteger();
        IntStream.range(1, 10).parallel().forEach((i) -> x.compareAndSet(i-1, i+1));
        if (x.get() != 10) {
            throw new RuntimeException("x (" + x.get() + ") is not 10");
        }
    }

    public static void main(String[] args) {
        intStreamTest();
    }
}
