#!/usr/bin/env python3
"""
convert_to_pacbio_bam.py

This is an unofficial script to convert a FASTA or FASTQ file with reads
to a flnc.bam generated with IsoSeq3


Author: Jorge Mestre Tomas
"""

import argparse
import os
import re
import subprocess
import sys


print("""
   ____                          _     _          ____            ____  _         ____    _    __  __ 
  / ___|___  _ ____   _____ _ __| |_  | |_ ___   |  _ \ __ _  ___| __ )(_) ___   | __ )  / \  |  \/  |
 | |   / _ \| '_ \ \ / / _ \ '__| __| | __/ _ \  | |_) / _` |/ __|  _ \| |/ _ \  |  _ \ / _ \ | |\/| |
 | |__| (_) | | | \ V /  __/ |  | |_  | || (_) | |  __/ (_| | (__| |_) | | (_) | | |_) / ___ \| |  | |
  \____\___/|_| |_|\_/ \___|_|   \__|  \__\___/  |_|   \__,_|\___|____/|_|\___/  |____/_/   \_\_|  |_|
                                                                                                      
""")

# Parser
parser = argparse.ArgumentParser(prog="convert_to_pacbio_bam.py", description="Reformats FASTA and FASTQ files to PacBio BAM files")
parser.add_argument('reads', help='\tRead sequences in FASTA or FASTQ format')
parser.add_argument('bam', help='\t\tIsoSeq3 real BAM to use as template')
parser.add_argument('output', help='\t\tOutput path and prefix for converted BAM file (".converted.bam" suffix will be added")')
parser.add_argument("--keep_files", action="store_true", help="\t\tIf used the program will not delete intermediate files", )

args = parser.parse_args()

if not os.path.exists(args.reads):
        print("ERROR: reads file does not exist. Provide a valid path", file=sys.stderr)
        sys.exit(1)

if not os.path.exists(args.bam):
        print("ERROR: bam file does not exist. Provide a valid path", file=sys.stderr)
        sys.exit(1)

out_bam = args.output + ".converted.bam"
if os.path.exists(out_bam):
        print("WARNING: output file already exist. Overwriting!", file=sys.stderr)

real_sam = args.bam[:-3] + "sam"
out_sam = args.output + ".converted.sam"

# BAM to SAM with SAMtools
print("Converting BAM to SAM")
cmd = "samtools view -h {bam} > {sam}\n".format(bam = args.bam, sam = real_sam)
if subprocess.check_call(cmd, shell=True) != 0:
    print("ERROR running samtools BAM to SAM: {0}".format(cmd), file=sys.stderr)
    sys.exit(1)

# Read FASTA or FASTQ reads
print("Reading query sequences")
seqs = []
saveFASTQ = False
saveFASTA = False
read = ""
with open(args.reads, "r") as f_reads:
    for line in f_reads:
        # Read FASTA format
        if line.startswith(">"):
            if saveFASTA:
                seqs.append((id, read))
                read = ""
            id = "/".join(line[1:].split())
            saveFASTA = True
        elif saveFASTA:
            read = read + line.strip()

        # Read FASTQ format
        elif line.startswith("@"):
            id = "/".join(line[1:].split())
            saveFASTQ = True
        elif saveFASTQ:
            seqs.append((id, line.strip()))
            saveFASTQ = False

if saveFASTA:
    seqs.append((id, read))
        
f_reads.close()

# Covert to IsoSeq3 BAM
print("Converting to SAM format")
converted_sam = open(out_sam, "w")
f_sam = open(real_sam, "r")

line = f_sam.readline()
while line.startswith("@"):
    converted_sam.write(line)
    line = f_sam.readline()

while seqs:
    if not line.startswith("@"):
        id, read = seqs.pop(0)
        line = line.split()
        line[0] = id
        line[9] = read # Consensus sequence
        line[10] = "~"*len(read) # Qual Values: All ~ 
        line = "\t".join(line)
        line = re.sub("(qe:.{1}:)[0-9]+", r"\g<1>"+str(len(read)), line)  # Read length)

        converted_sam.write(line + "\n") # Write converted read

    line = f_sam.readline()
    if not line:
        f_sam.close()
        f_sam = open(real_sam, "r")
        line = f_sam.readline()

f_sam.close()
converted_sam.close()

# SAM to BAM
print("Converting SAM to BAM")
cmd = "samtools view -b  {sam} > {bam}".format(sam = out_sam, bam = out_bam)
if subprocess.check_call(cmd, shell=True) != 0:
    print("ERROR running samtools SAM to BAM: {0}".format(cmd), file=sys.stderr)
    sys.exit(1)

if not args.keep_files:
    os.remove(real_sam)
    os.remove(out_sam)

print("Completed")
