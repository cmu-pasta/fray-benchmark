# python3 -m fray_benchmark run fray kafka --name bug-1 --scheduler random --cpu 30 --iterations 1
# python3 -m fray_benchmark run fray kafka --name bug-1 --scheduler pos --cpu 30 --iterations 1
# python3 -m fray_benchmark run fray lucene --name bug-1 --scheduler random --cpu 30 --iterations 1
# python3 -m fray_benchmark run fray lucene --name bug-1 --scheduler pos --cpu 30 --iterations 1
# python3 -m fray_benchmark run jpf guava --name bug-1 --cpu 30 --iterations 1
# python3 -m fray_benchmark run rr guava --name bug-1 --cpu 30 --iterations 1
# python3 -m fray_benchmark run jpf kafka --name bug-1 --cpu 30 --iterations 1
# python3 -m fray_benchmark run rr kafka --name bug-1 --cpu 30 --iterations 1
# python3 -m fray_benchmark run jpf lucene --name bug-1 --cpu 30 --iterations 1
# python3 -m fray_benchmark run rr lucene --name bug-1 --cpu 30 --iterations 1
# python3 -m fray_benchmark run fray lincheck --name bug-2 --cpu 10 --scheduler random --iterations 1
# python3 -m fray_benchmark run fray lincheck --name bug-2 --cpu 10 --scheduler pos --iterations 1
# python3 -m fray_benchmark run jpf lincheck --name bug-1 --cpu 10 --iterations 1
# python3 -m fray_benchmark run rr lincheck --name bug-2 --cpu 10 --iterations 1
#
# python3 -m fray_benchmark run fray jacontebe --name exec-1 --scheduler random --cpu 32 --perf-mode --timeout 600 --iterations 20
# python3 -m fray_benchmark run java jacontebe --name exec-1 --cpu 32 --perf-mode --timeout 600 --iterations 20
# python3 -m fray_benchmark run java sctbench --name exec-1 --cpu 32 --perf-mode --timeout 600 --iterations 20
# python3 -m fray_benchmark run fray lincheck --name bug-2 --cpu 10 --scheduler pct3 --iterations 1
# python3 -m fray_benchmark run fray lucene --name bug-1 --scheduler pct3 --cpu 30 --iterations 1
# python3 -m fray_benchmark run fray kafka --name bug-1 --scheduler pct3 --cpu 30 --iterations 1
# python3 -m fray_benchmark run fray guava --name bug-1 --scheduler pct3 --cpu 30 --iterations 1
# python3 -m fray_benchmark run fray sctbench --name exec-1 --scheduler random --cpu 32 --perf-mode --timeout 600 --iterations 20
# python3 -m fray_benchmark run jpf sctbench --name exec-1 --cpu 32 --perf-mode --timeout 600 --iterations 20
# python3 -m fray_benchmark run rr sctbench --name exec-1 --cpu 32 --perf-mode --timeout 600 --iterations 20
# python3 -m fray_benchmark run jpf jacontebe --name exec-1 --cpu 32 --perf-mode --timeout 600 --iterations 20
# python3 -m fray_benchmark run rr jacontebe --name exec-1 --cpu 32 --perf-mode --timeout 600 --iterations 20
# python3 -m fray_benchmark run fray guava --name bug-1 --scheduler random --cpu 30 --iterations 1
# python3 -m fray_benchmark run fray guava --name bug-1 --scheduler pos --cpu 30 --iterations 1
python3 -m fray_benchmark run fray kafka --name bug-1 --scheduler surw --cpu 30 --iterations 1
python3 -m fray_benchmark run fray lucene --name bug-1 --scheduler surw --cpu 30 --iterations 1
python3 -m fray_benchmark run fray guava --name bug-1 --scheduler surw --cpu 30 --iterations 1
python3 -m fray_benchmark run fray lincheck --name bug-1 --scheduler surw --cpu 30 --iterations 1
