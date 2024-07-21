# python3 -m fray_benchmark run fray kafka --name bug-1 --scheduler random --cpu 30
# python3 -m fray_benchmark run fray kafka --name bug-1 --scheduler pct15 --cpu 30
# python3 -m fray_benchmark run fray kafka --name bug-1 --scheduler pos --cpu 30
# python3 -m fray_benchmark run jpf kafka --name bug-1 --cpu 30 --iterations 1
# python3 -m fray_benchmark run rr kafka --name bug-1 --cpu 30
# python3 -m fray_benchmark run fray lucene --name bug-1 --scheduler random --cpu 30
# python3 -m fray_benchmark run fray lucene --name bug-1 --scheduler pct15 --cpu 30
# python3 -m fray_benchmark run fray lucene --name bug-1 --scheduler pos --cpu 30
# python3 -m fray_benchmark run jpf lucene --name bug-1 --cpu 30 --iterations 1
# python3 -m fray_benchmark run rr lucene --name bug-1 --cpu 30
# python3 -m fray_benchmark run fray guava --name bug-1 --scheduler random --cpu 30
# python3 -m fray_benchmark run fray guava --name bug-1 --scheduler pct15 --cpu 30 --iterations 1
# python3 -m fray_benchmark run fray guava --name bug-1 --scheduler pos --cpu 30 --iterations 1
python3 -m fray_benchmark run jpf guava --name bug-1 --cpu 30 --iterations 1
# python3 -m fray_benchmark run rr guava --name bug-1 --cpu 30 --iterations 1
