import java.lang.instrument.Instrumentation;

public class AssertionHandlerAgent {
    public static void premain(String agentArgs, Instrumentation inst) {
        Thread.setDefaultUncaughtExceptionHandler(new Thread.UncaughtExceptionHandler() {
            @Override
            public void uncaughtException(Thread t, Throwable e) {
                if (e instanceof AssertionError) {
                    System.err.println("Assertion failed: " + e.getMessage());
                    System.exit(-1);
                }
            }
        });
    }
}
