# BioToyBox

**Table of Contents**

- [Read Processing](#read-processing)
    - [Count Number of Reads from FASTQ File](#count-number-of-reads-from-fastq-file)
    - [Read Length Distribution from FASTQ File](#read-length-distribution-from-fastq-file)
    - [Average Read Length](#average-read-length)
    - [Convert2PacBioBam](#convert2pacbiobam)
- [Gene Reference and Annotation](#gene-reference-and-annotation)
    - [Get Transcript IDs from GTF File](#get-transcript-ids-from-gtf-file)
    - [Get Transcript ID and Chromosome from GTF File](#get-transcript-id-and-chromosome-from-gtf-file)
    - [Transcript Length and GC Content](#transcript-length-and-gc-content)

## Read Processing

### Count Number of Reads from FASTQ File

```bash
echo $(cat <file.fastq>|wc -l)/4|bc
```

### Read Length Distribution from FASTQ File

```bash
awk 'NR%4 == 2 {lengths[length($0)]++} END {for (l in lengths) {print l, lengths[l]}}' <file.fastq>
```

### Average Read Length

Compute average read length from FASTQ or FASTA file. Python script [here](scripts/average_read_length.py).

Use:

```python
python average_read_length.py <file_name>
```

### Convert2PacBioBam

Convert2PacBioBAM converts FASTA and FASTQ files to PacBio BAM files. To use the IsoSeq v3 pipeline, a file with the reads must be provided in PacBio BAM format, which carries quality information in a specific way. Users cannot always access the IsoSeq3 workflows because the scripts do not accept reads in FASTA or FASTQ format as input. To put a temporary patch to this problem, you can use the `convert_to_pacbio_bam.py` script. Given your reads in FASTA or FASTQ format and a real PacBio BAM file generated with `css` (also supports BAM files after using `lima` and `isoseq refine`), it will "convert" your sequences into a PacBio BAM file using the input file as a template.

#### Requirements

- Python (3.7)
- samtools

#### Usage

With the --help option you can display a complete description of the arguments:

```
usage: convert_to_pacbio_bam.py [-h] [--keep_files] reads bam output

Reformats FASTA and FASTQ files to PacBio BAM files

positional arguments:
  reads         Read sequences in FASTA or FASTQ format
  bam           PacBio real BAM to use as template
  output        Output path and prefix for converted BAM file
                (".converted.bam" suffix will be added")

optional arguments:
  -h, --help    show this help message and exit
  --keep_files  If used the program will not delete intermediate files
```

Running this tool will look as follows:

```
python convert_to_pacbio_bam.py reads.fasta PacBio.flnc.bam reads.out
```

## Gene Reference and Annotation

### Get Transcript IDs from GTF File

```bash
cat <file.gtf> | awk '$3 == "transcript" { print $12 }' | sed 's/"//' | sed 's/";//'
```

or

```bash
cat <file.gtf> | awk '$3 == "transcript" { gsub(/"/, "", $12); gsub(/;/, "", $12); print $12 }'
```

### Get Transcript ID and Chromosome from GTF File

To use the `trans_to_chrom` R function to get transcript IDs and corresponding chromosomes, follow these steps:

1. Download the R script [trans_to_chrom.R](scripts/trans_to_chrom.R) from this repository.

2. Load the script in your R environment:

   ```R
   source("path_to_trans_to_chrom.R")
   result <- trans_to_chrom("file.gtf")
   ```

The `result` variable will contain the mapping of transcripts to chromosomes.

Make sure you have the required R packages installed before using the function.

### Transcript Length and GC Content

Get transcript length and GC content of transcripts from GTF file.

1. Download the R script [gc_content_and_length.R](scripts/gc_content_and_length.R) from this repository.

2. Load the script in your R environment:

   ```R
   source("gc_content_and_length.R")
   result <- gc_content_and_length("reference.fa", "file.gtf")
   ```

Make sure you have the required R packages installed before using the function.
