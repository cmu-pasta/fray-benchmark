# Fray Artifact Evaluation

This repository contains the benchmark applications as well as the scripts to run them.

# 

This repository is used to evaluate the results of the paper . We would like to claim reusable, results reproduced, and artifact available badges for the paper. 

This document only includes the instructions to run the evaluation. The documentation of the Fray project is available in the [Fray repository](https://github.com/cmu-pasta/fray/docs).

# Requirements

## JPF and Fray

- You can run evaluation on any Linux and macOS system
- We provide a pre-configured container image that includes all the dependencies and tools to run the evaluation.
  - `podman run -it --privileged  localhost/fray-benchmark bash`
- You may also use nix to build the project manually.

## RR (Record and Replay)

- Linux baremetal machine with Linux kernel version 4.7 or higher
  - If you do not have a Linux system or running the evaluation in a VM, you cannot evaluate the results with RR.
  - You need to set `kernel.perf_event_paranoid` to `1` or lower to use RR.
    - You can do this by running the following command:
      ```bash
      echo 'kernel.perf_event_paranoid=1' | sudo tee '/etc/sysctl.d/51-enable-perf-events.conf'
      ```
    - If you are using NixOS, you can set the `kernel.perf_event_paranoid` option in your `configuration.nix` file:
      ```nix
      boot.kernel.sysctl."kernel.perf_event_paranoid" = 1;
      ```
- Intel CPU is recommended for better performance
  - For AMD CPU, you need [extra configuration](https://github.com/rr-debugger/rr/wiki/Zen)

# Build the Project


- First you need to enable the devshell `nix develop`. 
  - If you run this command in the container, you may ignore the error: `error: remounting /nix/store writable: Invalid argument`.
- Next run the following command to build all projects `./scripts/build.sh`.


## Run the Evaluation

- You may use the following script to run all benchmarks `./scripts/runall.sh`.

- You can also run a single benchmark by using the following command:

```bash
Usage: python -m fray_benchmark run [OPTIONS] {jpf|rr|fray|java} {kafka|s
                                    ctbench|jacontebe|lucene|lincheck|guava}

Options:
  --scheduler [pct3|pct15|pos|surw|random]
  --name TEXT
  -t, --timeout INTEGER
  --cpu INTEGER
  --perf-mode
  --iterations INTEGER
  --help                          Show this message and exit.
```


## Analyze Result


- All results will be saved in the `output` directory.
- If you run the `runall.sh` script, you can find the RQ1 and RQ2 results in the `output/benchmark` directory and the RQ3, and RQ4 results in the `output/realworld` directory.
  - `{benchmark_name}/{technique}/iter-0/{testcase}/` contains the output of each technique for each testcase.
- We provide a jupyter notebook to analyze the results. You can run the notebook by using the following command `uv run --with jupyter jupyter lab`.

### RQ1


### Note

1. RR is very sensitive to the kernel version, CPU architecture, and the system configuration. Different systems may produce different results. 

2. We have been improving Fray for the past few months, you may see better results for Fray for some benchmarks. 



<!-- # Structure

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
``` -->
