#!/bin/bash
# compute_read_lengths.sh
# Compute reads length distribution from a FASTQ file

if [ $# -ne 1 ]; then
    echo "Usage: $0 <FASTQ file>"
    exit 1
fi

fastq_file="$1" # FASTQ file

if [ ! -f "$fastq_file" ]; then
    echo "Error: Input file not found: $fastq_file"
    exit 1
fi

awk 'NR%4 == 2 {lengths[length($0)]++} END {for (l in lengths) {print l, lengths[l]}}' "$fastq_file"