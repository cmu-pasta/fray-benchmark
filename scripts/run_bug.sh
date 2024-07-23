# python3 -m fray_benchmark run fray kafka --name bug-1 --scheduler random --cpu 30
# python3 -m fray_benchmark run fray kafka --name bug-1 --scheduler pct15 --cpu 30
# python3 -m fray_benchmark run fray kafka --name bug-1 --scheduler pos --cpu 30
# python3 -m fray_benchmark run jpf kafka --name bug-1 --cpu 30 --iterations 1
# python3 -m fray_benchmark run rr kafka --name bug-1 --cpu 30
# python3 -m fray_benchmark run fray lucene --name bug-1 --scheduler random --cpu 30
# python3 -m fray_benchmark run fray lucene --name bug-1 --scheduler pct15 --cpu 30
# python3 -m fray_benchmark run fray lucene --name bug-1 --scheduler pos --cpu 30
# python3 -m fray_benchmark run jpf lucene --name bug-1 --cpu 30
# python3 -m fray_benchmark run rr lucene --name bug-1 --cpu 30
# python3 -m fray_benchmark run fray lincheck --name bug-2 --cpu 10 --scheduler random --iterations 1
# python3 -m fray_benchmark run fray lincheck --name bug-2 --cpu 10 --scheduler pct15 --iterations 1
# python3 -m fray_benchmark run fray lincheck --name bug-2 --cpu 10 --scheduler pos --iterations 1
# python3 -m fray_benchmark run jpf lincheck --name bug-1 --cpu 10 --iterations 1
# python3 -m fray_benchmark run rr lincheck --name bug-2 --cpu 10 --iterations 1
# python3 -m fray_benchmark run jpf lucene --name bug-1 --cpu 30 --iterations 1
# python3 -m fray_benchmark run rr lucene --name bug-1 --cpu 30
# python3 -m fray_benchmark run fray guava --name bug-1 --scheduler random --cpu 30
# python3 -m fray_benchmark run fray guava --name bug-1 --scheduler pct15 --cpu 30 --iterations 1
# python3 -m fray_benchmark run fray guava --name bug-1 --scheduler pos --cpu 30 --iterations 1
# python3 -m fray_benchmark run jpf guava --name bug-1 --cpu 30 --iterations 1
# python3 -m fray_benchmark run rr guava --name bug-1 --cpu 30 --iterations 1
