#!/bin/bash
# extract_transcript_id.sh
# Extract transcript ID from a GTF file

if [ $# -ne 1 ]; then
    echo "Usage: $0 <GTF file>"
    exit 1
fi

gtf_file="$1" # GTF file

if [ ! -f "$gtf_file" ]; then
    echo "Error: Input file not found: $gtf_file"
    exit 1
fi

#cat "$gtf_file" | awk '$3 == "transcript" { gsub(/"/, "", $12); gsub(/;/, "", $12); print $12 }'
cat "$gtf_file" | awk '$3 == "transcript" { print $12 }' | sed 's/"//' | sed 's/";//'