#!/bin/bash

filename="./shuffled_1m_example.data"  # Replace with your file's name
i=1
while IFS= read -r line || [[ -n "$line" ]]; do
    if ((i > 1000)); then
        break
    fi
    line="${line%$'\n'}"  # Strip trailing newline character
    { time python3 client.py $line; } 2>> ./output.txt
    echo $i
    echo $line
    ((i++))
done < "$filename"
