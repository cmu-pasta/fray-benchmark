for i in $(seq 0 19); do
    python3 -m fray_benchmark runOne /usr0/home/aoli/repos/fray-benchmark/output/perf-1/jacontebe/random/iter-$i/4
done
