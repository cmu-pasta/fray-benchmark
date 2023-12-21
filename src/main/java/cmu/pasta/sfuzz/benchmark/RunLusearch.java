package cmu.pasta.sfuzz.benchmark;

import org.dacapo.lusearch.Search;

public class RunLusearch {
    public static void main(String[] args) throws Exception {

        // I'm lazy so I rely on TestHarness to add classpath dynamically.
//        String cnf = "META-INF/cnf/lusearch.cnf";
//        InputStream ins = TestHarness.class.getClassLoader().getResourceAsStream(cnf);
//        Config config = Config.parse(ins);
        String DATA = "build/libs/unzipped/dacapo-23.11-chopin/dat";
//        Lusearch lusearch = new Lusearch(config, Files.createTempDirectory("foo").toFile(), new File(DATA + "/.."));
//
//        // Switch class loader.
//        lusearch.startIteration();
//        ClassLoader loader = Thread.currentThread().getContextClassLoader();
//        System.setProperty("os.name", "Linux");

        Search search = new Search();

        // We need to use reflection here because it is loaded through the context class loader.
        String[] runArgs = new String[]{
                "-index", DATA + "/lusearch/index-default",
                "-queries", DATA + "/lusearch/queries",
                "-output", "/tmp/lusearch.out",
                "-totalquerysets", "2048",
                "-querySetSize", "256",
                "-threads", "4"
        };
        search.main(runArgs);

    }
}
