#!/usr/bin/env python3
"""
average_read_length.py

This script outputs the average read length of a FASTA or FASTQ file
author: Jorge Mestre
"""

print("COMPUTE MEAN READ LENGTH FROM FASTA FILE\n")

file_type = input("Enter file type (number):\n1. FASTA\n2.FASTQ\n> ")

n_reads = 0
total_length = 0

if file_type == "1":
    fasta = input("Enter path to the file:\n> ")
    with open(fasta, "r") as f_in:
        for line in f_in:
            if line.startswith(">"):
                n_reads += 1
            else:
                total_length += len(line.strip())

elif file_type == "2":
    fastq = input("Enter path to the file:\n> ")
    next_line = False
    with open(fastq, "r") as f_in:
        for line in f_in:
            if line.startswith("@"):
                next_line = True
                n_reads += 1
            elif next_line:
                total_length += len(line.strip())
                next_line = False

print("\nMedian read length:", round((total_length/n_reads), 3))
