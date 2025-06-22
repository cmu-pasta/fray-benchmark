#!/usr/bin/env bash

python3 -m fray_benchmark run rr sctbench --name kickthetire --iterations 1 --perf-mode --cpu 12 --timeout 60
python3 -m fray_benchmark run fray sctbench --name kickthetire --scheduler random --iterations 1 --perf-mode --cpu 12 --timeout 60
python3 -m fray_benchmark run jpf sctbench --name kickthetire --iterations 1 --perf-mode --cpu 12 --timeout 60