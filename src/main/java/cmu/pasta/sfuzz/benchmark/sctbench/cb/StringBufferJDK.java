package cmu.pasta.sfuzz.benchmark.sctbench.cb;

/**
* Translated from: https://github.com/mc-imperial/sctbench/tree/master/benchmarks/conc-bugs/stringbuffer-jdk1.4
*/
public class StringBufferJDK {
    private char[] value;
    private int valueLength;
    private int count;
    private final Object mutexLock = new Object();

    private static StringBufferJDK nullBuffer = new StringBufferJDK("null");

    public StringBufferJDK() {
        value = new char[16];
        valueLength = 16;
        count = 0;
    }

    public StringBufferJDK(int length) {
        value = new char[length];
        valueLength = length;
        count = 0;
    }

    public StringBufferJDK(String str) {
        int length = str.length() + 16;
        value = new char[length];
        valueLength = length;
        count = 0;
        append(str);
    }

    public int length() {
        synchronized (mutexLock) {
            return count;
        }
    }

    public void getChars(int srcBegin, int srcEnd, char[] dst, int dstBegin) {
        synchronized (mutexLock) {
            if (srcBegin < 0) {
                assert false;
            }
            if ((srcEnd < 0) || (srcEnd > count)) {
                assert false;
            }
            if (srcBegin > srcEnd) {
                assert false;
            }
            System.arraycopy(value, srcBegin, dst, dstBegin, srcEnd - srcBegin);
        }
    }

    public StringBufferJDK append(StringBufferJDK sb) {
        synchronized (mutexLock) {
            if (sb == null) {
                sb = nullBuffer;
            }

            int len = sb.length();
            int newcount = count + len;
            if (newcount > valueLength)
                expandCapacity(newcount);
            sb.getChars(0, len, value, count);
            count = newcount;
            return this;
        }
    }

    public StringBufferJDK append(String str) {
        synchronized (mutexLock) {
            if (str == null) {
                str = "null";
            }

            int len = str.length();
            int newcount = count + len;
            if (newcount > valueLength)
                expandCapacity(newcount);
            str.getChars(0, len, value, count);
            count = newcount;
            return this;
        }
    }

    public StringBufferJDK erase(int start, int end) {
        synchronized (mutexLock) {
            if (start < 0)
                assert false;
            if (end > count)
                end = count;
            if (start > end)
                assert false;

            int len = end - start;
            if (len > 0) {
                System.arraycopy(value, start + len, value, start, count - end);
                count -= len;
            }
            return this;
        }
    }

    public void print() {
        synchronized (mutexLock) {
            for (int i = 0; i < count; i++) {
                System.out.print(value[i]);
            }
            System.out.println();
        }
    }

    private void expandCapacity(int minimumCapacity) {
        int newCapacity = (valueLength + 1) * 2;
        if (newCapacity < 0) {
            newCapacity = Integer.MAX_VALUE;
        } else if (minimumCapacity > newCapacity) {
            newCapacity = minimumCapacity;
        }

        char[] newValue = new char[newCapacity];
        System.arraycopy(value, 0, newValue, 0, count);
        value = newValue;
        valueLength = newCapacity;
    }

    public static void main(String[] args) {
        StringBufferJDK buffer = new StringBufferJDK("abc");

        Thread thread = new Thread(() -> {
            buffer.erase(0, 3);
            buffer.append("abc");
        });
        thread.start();

        StringBufferJDK sb = new StringBufferJDK();
        sb.append(buffer);
    }
}