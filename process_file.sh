#!/usr/bin/env bash
# Apply the Japanese parser to each line in the input file.

if [[ $# != 1 ]]; then
    echo "Usage: $0 input_file"
    exit 1
fi

readonly input_file=$1

while read -r line; do
    ./JapaneseParser.py "$line";
done < "$input_file"
