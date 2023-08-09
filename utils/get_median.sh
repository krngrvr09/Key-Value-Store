#!/bin/bash

awk '{print length}' example.data | sort -n > lengths.txt

total_lines=$(wc -l < lengths.txt)

if [ $((total_lines % 2)) -eq 1 ]; then
    median_index=$((total_lines / 2 + 1))
    median=$(sed -n "${median_index}p" lengths.txt)
else
    lower_median_index=$((total_lines / 2))
    upper_median_index=$((lower_median_index + 1))
    lower_median=$(sed -n "${lower_median_index}p" lengths.txt)
    upper_median=$(sed -n "${upper_median_index}p" lengths.txt)
    median=$(( (lower_median + upper_median) / 2 ))
fi

echo "Median length of lines: $median"

