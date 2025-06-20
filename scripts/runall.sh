python3 -m fray_benchmark run rr sctbench --name benchmark --iterations 1 --perf-mode
python3 -m fray_benchmark run fray sctbench --name benchmark --scheduler random --iterations 1 --perf-mode
python3 -m fray_benchmark run jpf sctbench --name benchmark --iterations 1 --perf-mode
python3 -m fray_benchmark run fray jacontebe --name benchmark --scheduler random --iterations 1 --perf-mode
python3 -m fray_benchmark run jpf jacontebe --name benchmark --iterations 1 --perf-mode   
python3 -m fray_benchmark run rr jacontebe --name benchmark --iterations 1 --perf-mode


python3 -m fray_benchmark run fray kafka --name realworld --scheduler pos --iterations 1
python3 -m fray_benchmark run jpf kafka --name realworld --iterations 1
python3 -m fray_benchmark run rr kafka --name realworld --iterations 1
python3 -m fray_benchmark run fray lucene --name realworld --scheduler pos --iterations 1
python3 -m fray_benchmark run jpf lucene --name realworld --iterations 1
python3 -m fray_benchmark run rr lucene --name realworld --iterations 1
python3 -m fray_benchmark run fray guava --name realworld --scheduler pos --iterations 1
python3 -m fray_benchmark run jpf guava --name realworld --iterations 1
python3 -m fray_benchmark run rr guava --name realworld --iterations 1
