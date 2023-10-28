#!/usr/bin/env python3
"""
average_read_length.py

This script outputs the average read length of a FASTA or FASTQ file
"""

import sys

if len(sys.argv) != 2:
    print("Usage: python average_read_length.py <file_name>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    # Open the file specified as a positional argument
    with open(file_path, 'r') as file:
        # Read the first character
        first_char = file.read(1)
        
        # Check if its FASTA or FASTQ file
        if first_char == ">":
            file_type = "fasta"
        elif first_char == "@":
            file_type = "fastq"
        else:
            print("ERROR: file must be FASTA or FASTQ file without header")
            sys.exit(1)
    
    # Explicitly close the file
    file.close()

except FileNotFoundError:
    print(f"The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

print("COMPUTE MEAN READ LENGTH FROM FASTA FILE\n")

n_reads = 0
total_length = 0

if file_type == "fasta":
    with open(file_path, "r") as f_in:
        for line in f_in:
            if line.startswith(">"):
                n_reads += 1
            else:
                total_length += len(line.strip())

elif file_type == "fastq":
    next_line = False
    with open(file_path, "r") as f_in:
        for line in f_in:
            if line.startswith("@"):
                next_line = True
                n_reads += 1
            elif next_line:
                total_length += len(line.strip())
                next_line = False

print("\nMean read length:", round((total_length/n_reads), 3))
