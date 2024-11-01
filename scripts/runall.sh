# python3 -m fray_benchmark jacontebe runJPF --name eval-1 --cpu 8
# python3 -m fray_benchmark jacontebe runRR --name eval-1 --cpu 8
# python3 -m fray_benchmark jacontebe run --name eval-1 --scheduler random --cpu 8
# python3 -m fray_benchmark sctbench runJPF --name eval-1 --cpu 8
# python3 -m fray_benchmark sctbench runRR --name eval-1 --cpu 8
# python3 -m fray_benchmark sctbench run --name eval-1 --scheduler random --cpu 8
python3 -m fray_benchmark run fray sctbench --name e-1 --scheduler random --cpu 32
python3 -m fray_benchmark run fray jacontebe --name e-1 --scheduler random --cpu 32
python3 -m fray_benchmark run fray sctbench --name e-1 --scheduler random --cpu 32
python3 -m fray_benchmark run fray jacontebe --name e-1 --scheduler random --cpu 32
# python3 -m fray_benchmark run jpf sctbench --name perf-1 --cpu 32
# python3 -m fray_benchmark run jpf jacontebe --name perf-1 --cpu 32
# python3 -m fray_benchmark run rr jacontebe --name perf-1 --cpu 32
# python3 -m fray_benchmark run rr sctbench --name perf-1 --cpu 32
