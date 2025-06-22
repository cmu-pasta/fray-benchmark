#!/usr/bin/env bash

# Default CPU count
CPU_COUNT=12

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --cpu)
            CPU_COUNT="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [--cpu <number>]"
            echo "  --cpu <number>    Number of CPU cores to use (default: 12)"
            echo "  -h, --help        Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "Running benchmarks with $CPU_COUNT CPU cores..."

python3 -m fray_benchmark run java sctbench --name benchmark --iterations 1 --perf-mode --cpu $CPU_COUNT
python3 -m fray_benchmark run rr sctbench --name benchmark --iterations 1 --perf-mode --cpu $CPU_COUNT
python3 -m fray_benchmark run rr jacontebe --name benchmark --iterations 1 --perf-mode --cpu $CPU_COUNT
python3 -m fray_benchmark run fray sctbench --name benchmark --scheduler random --iterations 1 --perf-mode --cpu $CPU_COUNT
python3 -m fray_benchmark run fray jacontebe --name benchmark --scheduler random --iterations 1 --perf-mode --cpu $CPU_COUNT
python3 -m fray_benchmark run jpf sctbench --name benchmark --iterations 1 --perf-mode --cpu $CPU_COUNT
python3 -m fray_benchmark run jpf jacontebe --name benchmark --iterations 1 --perf-mode --cpu $CPU_COUNT