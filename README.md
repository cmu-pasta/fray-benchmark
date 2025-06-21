# Fray Artifact Evaluation

This repository contains the benchmark applications as well as the scripts to run them.

# 

This repository is used to evaluate the results of the paper . We would like to claim reusable, results reproduced, and artifact available badges for the paper. 

This document only includes the instructions to run the evaluation. The documentation of the Fray project is available in the [Fray repository](https://github.com/cmu-pasta/fray/docs).

# Requirements

## JPF and Fray

- You can run evaluation on any Linux and macOS system
- If you wish to use our prebuild version, you can download it from [here]().
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

You may skip this step if you are using our prebuilt container.

- First you need to enable the direnv by running `direnv allow`. 
- Next run the following command to build all projects `./scripts/build.sh`.




## Analyze Result


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
