#!/bin/bash

CPU_COUNT=6
FULL_EVALUATION=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --cpu)
            CPU_COUNT="$2"
            shift 2
            ;;
        --full-evaluation)
            FULL_EVALUATION=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--cpu <number>] [--full-evaluation]"
            echo "  --cpu <number>      Number of CPU cores to use (default: 6)"
            echo "  --full-evaluation   Run full evaluation with all tools and schedulers (default: false)"
            echo "                      When false, only runs fray with scheduler pos"
            echo "  -h, --help          Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

if [ "$FULL_EVALUATION" = true ]; then
    echo "Running full evaluation with all tools and schedulers using $CPU_COUNT CPU cores..."
else
    echo "Running limited evaluation with fray scheduler pos only using $CPU_COUNT CPU cores..."
fi

# Always run fray with scheduler pos (basic evaluation)
python3 -m fray_benchmark run fray kafka --name realworld --scheduler pos --iterations 1 --cpu $CPU_COUNT
python3 -m fray_benchmark run fray lucene --name realworld --scheduler pos --iterations 1 --cpu $CPU_COUNT
python3 -m fray_benchmark run fray guava --name realworld --scheduler pos --iterations 1 --cpu $CPU_COUNT
python3 -m fray_benchmark run fray lincheck --name realworld --scheduler pos --iterations 1 --cpu $CPU_COUNT

# Only run additional commands if full-evaluation is enabled
if [ "$FULL_EVALUATION" = true ]; then
    python3 -m fray_benchmark run rr kafka --name realworld --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run rr lucene --name realworld --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run rr guava --name realworld --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run fray kafka --name realworld --scheduler pct3 --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run fray lucene --name realworld --scheduler pct3 --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run fray guava --name realworld --scheduler pct3 --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run fray kafka --name realworld --scheduler pct15 --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run fray lucene --name realworld --scheduler pct15 --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run fray guava --name realworld --scheduler pct15 --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run fray kafka --name realworld --scheduler surw --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run fray lucene --name realworld --scheduler surw --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run fray guava --name realworld --scheduler surw --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run fray kafka --name realworld --scheduler random --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run fray lucene --name realworld --scheduler random --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run fray guava --name realworld --scheduler random --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run jpf kafka --name realworld --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run jpf lucene --name realworld --iterations 1 --cpu $CPU_COUNT
    python3 -m fray_benchmark run jpf guava --name realworld --iterations 1 --cpu $CPU_COUNT
fi
