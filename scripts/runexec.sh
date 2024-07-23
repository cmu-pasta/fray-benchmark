python3 -m fray_benchmark run fray sctbench --name exec-1 --scheduler random --cpu 32 --perf-mode --timeout 600 --iterations 1
python3 -m fray_benchmark run jpf sctbench --name exec-1 --cpu 32 --perf-mode --timeout 600 --iterations 1
python3 -m fray_benchmark run rr sctbench --name exec-1 --cpu 32 --perf-mode --timeout 600 --iterations 1
python3 -m fray_benchmark run fray jacontebe --name exec-1 --scheduler random --cpu 32 --perf-mode --timeout 600 --iterations 1
python3 -m fray_benchmark run jpf jacontebe --name exec-1 --cpu 32 --perf-mode --timeout 600 --iterations 1
python3 -m fray_benchmark run rr jacontebe --name exec-1 --cpu 32 --perf-mode --timeout 600 --iterations 1
