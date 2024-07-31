# Fray Benchmark

This repository contains the benchmark applications as well as the scripts to run them.

# Structure

- `bms` contains the source code for each benchmark application.
- `tools` contains the source code for JPF and RR.


To run understand how to use benchmark scripts you can start with

```
python -m fray_benchmark --help

```

```
Usage: python -m fray_benchmark [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  build
  replay
  run
  runOne
  runSingle
```

To run a single benchmark application you can use the following command:

```
Usage: python -m fray_benchmark run [OPTIONS] {jpf|rr|fray} {lucene|solr|jacon
                                    tebe|guava|kafka|lincheck|sctbench|apachec
                                    ommon}

Options:
  --scheduler [pct3|pct15|pos|random]
  --name TEXT
  -t, --timeout INTEGER
  --cpu INTEGER
  --perf-mode
  --iterations INTEGER
  --help                          Show this message and exit.
```