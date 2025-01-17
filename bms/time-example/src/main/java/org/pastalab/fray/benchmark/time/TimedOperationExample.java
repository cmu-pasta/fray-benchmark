package org.pastalab.fray.benchmark.time;

import java.util.concurrent.ConcurrentLinkedDeque;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.BooleanSupplier;

public class TimedOperationExample {
public enum ServiceState {
    INIT,
    RUNNING,
}
public class Service extends Thread {
    public volatile ServiceState serviceState;
    private final ConcurrentLinkedDeque<Runnable> jobs;
    public boolean shouldStop;

    public Service() {
        serviceState = ServiceState.INIT;
        jobs = new ConcurrentLinkedDeque<>();
        shouldStop = false;
        // Other bootstrap code
    }

    @Override
    public void run() {
        serviceState = ServiceState.RUNNING;
        // Run jobs...
    }

    public void submitJob(Runnable job) {
        if (serviceState != ServiceState.INIT) {
            jobs.add(job);
        }
    }
}

public void testServiceStartSuccessfully() {
    Service service = new Service();
    service.start();
    AtomicBoolean jobDone = new AtomicBoolean(false);
    Runnable myJob = () -> {
        jobDone.set(true);
    };
    assert(waitForCondition(() -> service.serviceState == ServiceState.RUNNING, 1000));
    service.submitJob(myJob);
    assert(waitForCondition(() -> jobDone.get(), 1000));
}

public boolean waitForCondition(BooleanSupplier condition, long timeout) {
    long start = System.currentTimeMillis();
    while (!condition.getAsBoolean()) {
        if (System.currentTimeMillis() - start > timeout) {
            return false;
        }
    }
    return true;
}
}
