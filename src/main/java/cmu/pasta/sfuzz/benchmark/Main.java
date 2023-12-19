package cmu.pasta.sfuzz.benchmark;

import org.dacapo.harness.TestHarness;
public class Main {
    public static void main(String[] args) {
        System.setProperty("sun.jnu.encoding", "UTF-8");
        String DATA = "build/libs/unzipped/dacapo-23.11-chopin/dat";
        String[] runArgs = new String[]{
            "jython",
            "-index", DATA + "/lusearch/index-default",
            // "-queries", DATA + "/lusearch/queries",
            // "-output", "/tmp/lusearch.out",
            "-totalquerysets", "2048",
            // "-querySetSize", "256",
            "-threads", "4"
    };
        TestHarness.main(runArgs);
        // TestHarness.main(new String[] {"jython"});

    }
}