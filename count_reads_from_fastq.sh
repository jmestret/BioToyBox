#!/bin/bash
# count_reads_from_fastq.sh
# Count the number of reads in a FASTQ file (no header)

# Check if the input file is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <FASTQ file>"
    exit 1
fi

fastq_file="$1" # FASTQ file

# Check if the input file exists
if [ ! -f "$fastq_file" ]; then
    echo "Error: Input file not found: $fastq_file"
    exit 1
fi

# Count the number of reads (assuming 4 lines per read)
# echo $(cat $fastq_file|wc -l)/4|bc
num_lines=$(wc -l < "$fastq_file")
num_reads=$((num_lines / 4))

echo "$num_reads"