#!/bin/bash

# Create results directory if it doesn't exist
mkdir -p results

# Run gcc configurations
for config in gcc_b*_{random,fifo,lru}.cfg; do
    echo "Running $config..."
    ./sim-outorder -config $config benchmarks/cc1.alpha -O benchmarks/1stmt.i 2>&1 | tee "results/${config%.cfg}_output.txt"
    echo "----------------------------------------"
done

# Run anagram configurations
for config in anagram_b*_{random,fifo,lru}.cfg; do
    echo "Running $config..."
    ./sim-outorder -config $config benchmarks/anagram.alpha benchmarks/words < benchmarks/anagram.in 2>&1 | tee "results/${config%.cfg}_output.txt"
    echo "----------------------------------------"
done

# Run compress95 configurations
for config in compress95_b*_{random,fifo,lru}.cfg; do
    echo "Running $config..."
    ./sim-outorder -config $config benchmarks/compress95.alpha < benchmarks/compress95.in 2>&1 | tee "results/${config%.cfg}_output.txt"
    echo "----------------------------------------"
done

# Run go configurations
for config in go_b*_{random,fifo,lru}.cfg; do
    echo "Running $config..."
    ./sim-outorder -config $config benchmarks/go.alpha 50 9 benchmarks/2stone9.in 2>&1 | tee "results/${config%.cfg}_output.txt"
    echo "----------------------------------------"
done

echo "All simulations completed. Results are saved in results directory"
